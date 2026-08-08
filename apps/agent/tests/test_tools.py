import pytest
from tools.solver import python_executor

def test_python_executor_success():
    code = "print(2 + 2)"
    result = python_executor(code=code)
    assert "4" in result.get("result", "")

def test_python_executor_error():
    code = "print(1 / 0)"
    result = python_executor(code=code)
    assert "error" in result
    assert "ZeroDivisionError" in result["error"]
