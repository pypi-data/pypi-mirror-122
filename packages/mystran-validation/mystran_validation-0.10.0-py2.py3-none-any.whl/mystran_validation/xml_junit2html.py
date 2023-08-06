import os
import logging
import xml.etree.ElementTree as ET
from collections import defaultdict
from io import StringIO
from pathlib import Path, PosixPath
import shutil
import configparser

import pkg_resources
from jinja2 import Environment, FileSystemLoader, PackageLoader

from mystran_validation.utils import slugify
from mystran_validation import get_profile, get_conf, acopy, cleandir


try:
    loader = PackageLoader("mystran_validation", "data/html_template.j2")
except ValueError:
    # probably installed using `pip install -e .`
    logging.warning("logging from FileSystem")
    tpl_folder = (pkg_resources.resource_filename("mystran_validation", "data"),)
    logging.warning(f"{tpl_folder=}")
    loader = FileSystemLoader(tpl_folder)
env = Environment(loader=loader)
env.filters["slugify"] = slugify


class TestSuite:
    """TestSuite: container for all testsuite test cases. Normally, this is only one."""

    def __init__(self, xml):
        self.meta = xml.attrib
        self.testcases = {}
        # ---------------------------------------------------------------------
        # configure XML / HTML / assets dir
        config_fpath, config = get_conf()
        for i, tc in enumerate(xml.findall("./testcase")):
            tcobject = TestCase(tc)
            if tcobject.classname not in self.testcases:
                tcparent = TestCaseParent(tcobject.classname)
                self.testcases[tcobject.classname] = tcparent
            self.testcases[tcobject.classname].add_test_case(tcobject)

    def __repr__(self):
        return "testsuite errors={errors} failures={failures} skipped={skipped} tests={tests} time={time} timestamp={timestamp}".format(
            **self.meta
        )


class TestCaseParent:
    """thin wrapper equivalent to ini file"""

    def __init__(self, classname):
        self.classname = classname
        self.testcases = []
        self.meta = {}
        self._status = defaultdict(int)
        self.marks = set()
        self.assets = defaultdict(dict)
        self.rel_assets = defaultdict(dict)
        self.test_config = configparser.ConfigParser()
        self.rootdir = None

    def get_assets(self, tcobject, section):
        cfg = dict(self.test_config[section].items())
        cfg["neutral output"] = tcobject.properties["output"]
        if section != "DEFAULT":
            # get only keys differing from "DEFAULT"
            default_cfg = dict(self.test_config[section].items())
            default_cfg["neutral output"] = tcobject.properties["output"]
            cfg = {k: v for k, v in cfg.items() if v != default_cfg[k]}
        if self.rootdir is None:
            self.rootdir = Path(tcobject.properties["test-config"]).parent
        for k in ("bulk", "reference", "neutral output"):
            if k in cfg:
                path = self.rootdir / Path(cfg[k])
                if path.exists():
                    self.assets[section][k] = path

    def copy_assets(self, section):
        """copy files and store assets as path relative to HTML file"""
        html_outdir = Path(os.environ["MYSTRAN_VALIDATION_HTML_OUTDIR"])
        assets_outdir = html_outdir / "assets" / Path(self.classname).stem / section
        cleandir(assets_outdir, parents=True)
        assets = dict(self.assets)[section]
        for k, src in assets.items():
            target = assets_outdir / src.name
            acopy(src, target)
            target = target.relative_to(html_outdir)
            self.rel_assets[section][k] = target

    def __hash__(self):
        return hash(self.classname)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.classname == other.classname

    def add_test_case(self, tcobject):
        all_assets = eval(tcobject.properties.get("assets", "{}"))
        if not self.testcases:
            # actions to perform once only
            self.test_config.read(tcobject.properties["test-config"])
            self.get_assets(tcobject, section="DEFAULT")
            self.shortdesc = tcobject.properties.pop("shortdesc", "")
            self.copy_assets("DEFAULT")
        self.get_assets(tcobject, section=tcobject.name)
        self.testcases.append(tcobject)
        self._status[tcobject.status] += 1
        self.marks |= eval(tcobject.properties.get("marks", "set()"))

    @property
    def short_classname(self):
        return "/".join(self.classname.split(".")[1:-1]) + ".ini"

    @property
    def html_status(self):
        msg = []
        for status, nb in self._status.items():
            msg.append(f'<span class="alert-{status}">{status}</span>')
        return " ".join(msg)


class TestCase:
    def __init__(self, xml):
        for k, v in xml.attrib.items():
            setattr(self, k, v)
        self.properties = {}
        for prop in xml.findall("./properties/property"):
            self.properties[prop.attrib["name"]] = prop.attrib["value"]
        # ---------------------------------------------------------------
        # skipped
        skipped = xml.find("./skipped")
        if skipped is not None:
            self.skipped = skipped.attrib
        else:
            self.skipped = None
        # ---------------------------------------------------------------
        # failed
        failure = xml.find("./failure")
        if failure is not None:
            self.failure = failure.attrib
        else:
            self.failure = None

    @property
    def status(self):
        if self.skipped:
            return "skipped"
        elif self.failure:
            return "failed"
        return "success"

    def __repr__(self):
        s = f"{self.classname}::{self.name}"
        if self.skipped:
            s += " (skipped)"
        if self.failure:
            s += " (failed)"
        return s


def parse_xml(filepath):
    """parse JUnit  XML file and return a tuple of `TestSuite` instances"""
    fpath = Path(filepath)
    assert fpath.exists()
    tree = ET.parse(filepath)
    root = tree.getroot()
    # get all testsuites
    return tuple((TestSuite(ts) for ts in root.findall("./testsuite")))


def xml2html(xmlfpath):
    tss = parse_xml(xmlfpath)
    rtemplate = env.get_template("html_template.j2")
    return rtemplate.render({"testsuites": tss})
