import importlib.util
from pathlib import Path


def load_report_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "case-studies" / "python-report-automation" / "src" / "report_automation.py"
    spec = importlib.util.spec_from_file_location("report_automation", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
