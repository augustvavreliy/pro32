import pytest
import sys

if __name__ == "__main__":
    # Run tests with verbose output
    exit_code = pytest.main(["-v", "-s", "tests/"])
    sys.exit(exit_code)