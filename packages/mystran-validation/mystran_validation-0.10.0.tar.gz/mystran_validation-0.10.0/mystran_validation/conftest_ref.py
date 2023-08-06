# content of conftest.pybreakpoint()
import ast
import configparser
import numbers
import os
import shlex
import shutil
import subprocess
import traceback
from pathlib import Path
import warnings
import tempfile
from collections import defaultdict
import pandas as pd
import pytest
from femap_neutral_parser import Parser as NeuParser

from mystran_validation import assert_frame_equal, background, acopy, cleandir
from mystran_validation.utils import slugify
from mystran_validation.parsers import subset
from mystran_validation.parsers.nastran_op2 import Parser as OP2Parser


# =============================================================================
# test collection
# =============================================================================
ROOTDIR = None


def pytest_collection_modifyitems(items):
    """add CARDs to marks"""
    for item in items:
        bulk_file = item.spec["bulk"]
        with open(bulk_file, "r") as fh:
            lines = fh.readlines()
        words = set(
            [
                l.split(" ")[0].strip()
                for l in lines
                if not l.startswith("$")
                and not l.startswith("+")
                and not l.startswith("PARAM,")
                and not l.startswith("CORD,")
            ]
        ) - set(
            [
                "",
                " ",
                "PARAM",
                "CEND",
                "ENDDATA",
                "NASTRAN",
                "ID",
                "GRID",
                "SUBCASE",
                "TIME",
                "BEGIN",
                "SOL",
                "INIT",
            ]
        )
        for tag in words:
            item.add_marker(getattr(pytest.mark, tag))
        # ---------------------------------------------------------------------
        # user-defined marks
        marks = item.spec.get("marks", ())
        if marks:
            marks = [m.strip() for m in marks.split(",")]
            for mark in marks:
                item.add_marker(getattr(pytest.mark, mark))


def pytest_collect_file(parent, path):
    global ROOTDIR
    if ROOTDIR is None:  # set rootdir for centralized dumping
        ROOTDIR = Path(path.dirpath())
    _path = Path(path)
    if _path.suffix == ".ini" and _path.name.startswith("test"):
        return IniTestFile.from_parent(parent, fspath=path)


class IniTestFile(pytest.File):
    bulkfile = None
    rootdir = None
    rootname = None
    mystran_run_status = {}
    reference = {}
    op2s = {}

    def collect(self):
        config = configparser.ConfigParser()
        config.read(self.fspath)
        # ---------------------------------------------------------------------
        # prepare paths
        self.rootdir = Path(self.fspath).parent
        self.rootname = Path(self.fspath).stem
        # ---------------------------------------------------------------------
        # clean working dir
        wdir = self.rootdir / (".out_" + self.rootname)
        cleandir(wdir)
        for name in config.sections():
            spec = dict(config[name].items())
            spec["test-config"] = Path(self.fspath)
            # =================================================================
            # building and yielding atomic test [name]
            # =================================================================
            bulkfile = self.rootdir / spec["bulk"]
            if self.bulkfile:
                if bulkfile != self.bulkfile:
                    raise ValueError(f"{name}: One class, one bulk, one output!")
            else:
                self.bulkfile = bulkfile
            spec["workingdir"] = wdir
            spec["bulk"] = bulkfile
            ref = spec["reference"]
            # -----------------------------------------------------------------
            # if ref is obviously a file
            if Path(ref).suffix.lower() in (".op2", ".neu"):
                spec["reference"] = self.rootdir / spec["reference"]
            # -----------------------------------------------------------------
            # if ref a sing value
            else:
                ref = float(ref)
                spec["reference"] = ref
            spec["rtol"] = float(spec.get("rtol", 1e-05))
            spec["atol"] = float(spec.get("atol", 1e-08))
            spec["shortdesc"] = spec.get("shortdesc", "")
            spec["output"] = spec["workingdir"] / (bulkfile.stem + ".NEU")
            yield IniItem.from_parent(self, name=name, spec=spec)


class IniItem(pytest.Item):
    """Atomic test. This is where one single [test] is performed"""

    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.spec = spec

    def run_mystran(self):
        """run bulkfile"""
        target = shutil.copy(self.spec["bulk"], self.spec["workingdir"])
        cmd = f"{os.getenv('MYSTRAN_BIN')} {target}"
        status = subprocess.check_output(
            shlex.split(cmd),
            stderr=subprocess.STDOUT,
        )
        if "fatal" in status.decode().lower():
            # retrieve Error
            target = Path(target)
            error_file = target.parent / (target.stem + ".ERR")
            f06_file = target.parent / (target.stem + ".F06")
            with open(error_file, "r") as fh:
                lines = fh.readlines()
            errors = []
            _parsing_error = False
            for l in lines:
                l = l.strip()
                if _parsing_error:
                    if l.startswith("*"):
                        errors.append(tuple(_parsing_error))
                        _parsing_error = False
                    _parsing_error.append(l)
                if l.startswith("*ERROR"):
                    _parsing_error = [l]
            if _parsing_error:
                errors.append(tuple(_parsing_error))
            errors = ["\n".join(err) for err in errors]
            raise MystranException(errors[0])
        # ---------------------------------------------------------------------
        # get actual results
        neu = NeuParser(self.spec["output"])
        self.parent.actual = neu
        self.parent.actual.info(doprint=False)  # pre-digest data
        self.parent.actual_available_vectors = sorted(
            self.parent.actual._output_vectors.keys()
        )
        return status

    def expected(self, vector, filters=None, axis=None, raw=False):
        """build reference (expected) DataFrame"""
        if not filters:
            filters = {}
        df_expected = None
        # ---------------------------------------------------------------------
        # reference is a numerical value
        if isinstance(self.spec["reference"], numbers.Number):
            if axis is None:
                raise ValueError("param `axis` must be specified for manual checking")
            _data = filters.copy()
            _data.update({axis: [self.spec["reference"]]})
            df_expected = pd.DataFrame(_data)
            df_expected.set_index(list(filters.keys()), inplace=True)
            df_expected = df_expected[axis].to_frame()
        # ---------------------------------------------------------------------
        # reference is a ref file
        elif self.spec["reference"].suffix.lower() == ".op2":
            op2 = self.parent.op2s[self.spec["reference"]]
            df_expected = op2.get(vector=vector, raw=raw, **filters)
        else:
            raise ValueError("reference {self.spec['reference']} not understood")
        return df_expected

    def actual(self, vector, filters=None, axis=None):
        """build actual DataFrame"""
        if not filters:
            filters = {}
        # ---------------------------------------------------------------------
        # as of femap_neutral_parser 0.8, vectos have been renamed
        compat = {
            "reactions": "spc_forces",
        }
        if vector in compat:
            warnings.warn(
                f"``{vector}`` is deprecated. Use ``{compat[vector]}`` instead"
            )
        vector = compat.get(vector, vector)
        # -----------------------------------------------------------------
        # get values from neutral file, and reshape it
        df_actual = self.parent.actual.get(vector, asdf=True)
        df_actual = subset(df_actual, **filters)
        if axis:
            try:
                df_actual = df_actual[axis].to_frame()
            except KeyError:
                msg = f"{axis} is not a proper column. Use one of {df_actual.columns.tolist()}"
                raise KeyError(msg)
        return df_actual

    def runtest(self):
        """trigger pytest"""
        if self.spec.get("skip"):
            pytest.skip(self.spec["skip"])
        # ---------------------------------------------------------------------
        # run Mystran only once
        if self.spec["bulk"] not in self.parent.mystran_run_status:
            # first test for this class, a few things to set up
            retmystran = self.run_mystran()
            self.parent.mystran_run_status[self.spec["bulk"]] = retmystran
        # process OP2 only once
        ref = self.spec["reference"]
        if not isinstance(ref, numbers.Number):
            if ref.suffix.lower() == ".op2" and str(ref) not in self.parent.op2s:
                self.parent.op2s[ref] = OP2Parser(str(self.spec["reference"]))
            self.op2 = self.parent.op2s[ref]  # shortcut for self
        else:
            self.op2 = None
        self.user_properties += [("bulk", str(self.spec["bulk"]))]
        self.user_properties += [("ref", str(self.spec["reference"]))]
        self.user_properties += [("output", str(self.spec["output"]))]
        self.user_properties += [("description", self.spec["description"])]
        self.user_properties += [("atol", self.spec["atol"])]
        self.user_properties += [("rtol", self.spec["rtol"])]
        self.user_properties += [("shortdesc", self.spec["shortdesc"])]
        self.user_properties += [("vector", self.spec["vector"])]
        self.user_properties += [("marks", set([m.name for m in self.own_markers]))]
        self.user_properties += [("test-config", self.spec["test-config"])]
        try:
            vector = self.spec["vector"]
            # ---------------------------------------------------------------------
            # get subset index
            filters = dict(
                SubcaseID=ast.literal_eval(self.spec.get("subcaseids", "None")),
                NodeID=ast.literal_eval(self.spec.get("nodeids", "None")),
                ElementID=ast.literal_eval(self.spec.get("elementids", "None")),
            )
            axis = self.spec.get("axis")
            filters = {k: [v] for k, v in filters.items() if v}
            # ---------------------------------------------------------------------
            # get dataframes to compare
            df_actual = self.actual(vector, filters, axis)
            df_expected = self.expected(vector, filters, axis)
            # -----------------------------------------------------------------
            # check tolerances
            rtol = self.spec["rtol"]
            atol = self.spec["atol"]
            failing, failures, aerr, rerr = assert_frame_equal(
                df_actual, df_expected, rtol=rtol, atol=atol
            )
        except Exception as exc:
            tb = traceback.format_exc()
            raise GenericException(self, exc, tb)
        else:
            if len(failures) > 0:
                # dump comparisons performed
                if (
                    os.getenv("MYSTRAN_VALIDATION_DUMP_XLSX") == "2"
                    or os.getenv("MYSTRAN_VALIDATION_DUMP_XLSX") == "1"
                    and len(failures) > 0
                ):
                    xlsx_filepath = dump(
                        df_expected,
                        df_actual,
                        wdir=self.spec["workingdir"],
                        sheetname=self.spec["vector"],
                        name=Path(self.parent.name),
                        failing=failing,
                    )
                raise IniException(
                    self, df_actual, df_expected, failures, rtol, atol, aerr, rerr
                )

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, MystranException):
            return excinfo.value
        elif isinstance(excinfo.value, IniException):
            (
                item,
                df_actual,
                df_expected,
                failures,
                rtol,
                atol,
                aerr,
                rerr,
            ) = excinfo.value.args
            df_actual = df_actual.loc[failures.index]
            df_expected = df_expected.loc[failures.index]
            # failing difference
            return "\n".join(
                [
                    f"usecase `{self.fspath}::[{self.name}]`\nexecution failed given precision requirements:\n  * {atol=}\n  * {rtol=}\n",
                    f"failing with:\n  * Absolute difference {aerr=}\n  * Relative difference {rerr=}\n",
                    f"Expected\n--------\n{df_expected}\n",
                    f"Actual\n------\n{df_actual}",
                ]
            )
        elif isinstance(excinfo.value, GenericException):
            item, exc, traceback = excinfo.value.args
            return "\n".join(
                [
                    f"usecase `{self.fspath}::[{self.name}]` raised the following exception\n",
                    f"{exc}\n",
                    f"file: {traceback}",  # get rid of "file " prefix
                ]
            )

    def reportinfo(self):
        return self.fspath, 0, f"usecase: {self.name}"


class IniException(Exception):
    pass


class MystranException(Exception):
    pass


class GenericException(Exception):
    pass


def apply_color(x, failing):
    colors = {False: "green", True: "red; font-weight: bold"}
    return failing.applymap(lambda val: "color: {}".format(colors.get(val, "")))


def highlight_columns(x):
    if x.name[0] == "Actual":
        style = f"background-color: azure"
    else:
        style = f"background-color: beige"
    return [style] * x.shape[0]


# @background
def dump(df_expected, df_actual, wdir, name, sheetname, failing, debug=False):
    full = (
        pd.concat({"Expected": df_expected, "Actual": df_actual})
        .unstack(level=0)
        .swaplevel(axis=1)
        .sort_index(axis=1)
    )
    # reshape failing to have same format as `full`
    failing = (
        pd.concat({"Expected": failing, "Actual": failing})
        .unstack(level=0)
        .swaplevel(axis=1)
        .sort_index(axis=1)
    )
    # =========================================================================
    # formatting
    # =========================================================================
    dumping_dir = ROOTDIR / "html" / "media"
    dumping_dir.mkdir(exist_ok=True, parents=True)
    target = dumping_dir / (name.stem + ".xlsx")
    mode = "a" if target.exists() else "w"
    # style dataframe
    styled = full.style.apply(apply_color, axis=None, failing=failing)
    styled = styled.apply(highlight_columns)
    with pd.ExcelWriter(target, mode=mode, engine="openpyxl") as writer:
        styled.to_excel(writer, sheet_name=sheetname)
    return target
    # formatting
    # if len(failures) == 0:
    #     return
    # cols = df_expected.columns.tolist()
    # guilty_columns
    # breakpoint()
    # writer = pd.ExcelWriter(target, mode="a")
    # workbook  = writer.book
    # worksheet = writer.sheets[sheetname]
    # red_format = workbook.add_format({'bg_color':'red'})
    # green_format = workbook.add_format({'bg_color':'green'})

    # worksheet.conditional_format('B2:B4', {'type': 'text',
    #                                       'criteria': 'containing',
    #                                        'value':     'Fail',
    #                                        'format': red_format})

    # worksheet.conditional_format('B2:B4', {'type': 'text',
    #                                       'criteria': 'containing',
    #                                        'value':   'Pass',
    #                                        'format':  green_format})
    # writer.save()
