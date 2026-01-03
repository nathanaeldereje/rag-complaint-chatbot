import pytest

def test_environment_is_ready():
    """
    A simple smoke test to verify that pytest is working 
    and the CI pipeline can run successfully.
    """
    assert True

def test_math_sanity():
    """
    Verifies basic arithmetic to ensure the test runner isn't broken.
    """
    assert 1 + 1 == 2