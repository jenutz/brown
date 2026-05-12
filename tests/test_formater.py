import pytest
import os
import sys
from io import StringIO
import pycodestyle
from brown import format_code


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def get_test_cases():
    files = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".py") and not f.endswith("_exp.py")]
    return files

@pytest.mark.parametrize("filename", get_test_cases())
def test_benchmarks(filename):
    input_path = os.path.join(FIXTURE_DIR, filename)
    expected_path = os.path.join(FIXTURE_DIR, filename.replace(".py", "_exp.py"))

    with open(input_path, "r") as f:
        source = f.read()
    with open(expected_path, "r") as f:
        expected = f.read()

    formatted = format_code(source, indent=4)

    assert formatted == expected, f"Failed formatting for {filename}"

@pytest.mark.parametrize("filename", get_test_cases())
def test_strict_style_compliance(filename):
    input_path = os.path.join(FIXTURE_DIR, filename)
    with open(input_path, "r") as f:
        source = f.read()
    
    formatted = format_code(source, indent=4)
    fake_file = StringIO(formatted)
    style_guide = pycodestyle.StyleGuide( quiet=False, select=['E1', 'E2', 'E3', 'W1', 'W2', 'W3'])
    
    checker = pycodestyle.Checker(
        filename=filename, 
        lines=fake_file.readlines(), 
        options=style_guide.options
    )
    
    temp_stdout = StringIO()
    sys.stdout = temp_stdout
    
    try:
        errors = checker.check_all()
    finally:
        sys.stdout = sys.__stdout__
    
    report_output = temp_stdout.getvalue()
    
    assert errors == 0, f"Violations in {filename}:\n{report_output}"