import zipfile
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn


def _outputdir():
    return Path(BuiltIn().get_variable_value("${OUTPUTDIR}"))


def open_browser(url="about:blank"):
    pass


def close_browser():
    pass


def create_trace():
    trace_path = _outputdir() / "browser" / "trace-1.zip"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(trace_path), "w") as zf:
        zf.writestr("trace.json", "{}")


def create_trace_in_subdir():
    trace_path = _outputdir() / "browser" / "traces" / "sometrace.zip"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(trace_path), "w") as zf:
        zf.writestr("trace.json", "{}")


def do_nothing():
    pass
