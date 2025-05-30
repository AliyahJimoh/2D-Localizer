import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from input_format import InputData


def test_invalid_yaml(tmp_path):
    """
    F-IN-01: Checks rejection of malformed YAML input files.
    """
    bad_file = tmp_path / "bad.yaml"
    bad_file.write_text("invalid: [unclosed")

    try:
        _ = InputData(input_file=str(bad_file))
    except ValueError as e:
        assert "Invalid YAML" in str(e)
    else:
        assert False, "Expected ValueError for invalid YAML"
