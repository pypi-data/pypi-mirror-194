from better_json_tools import CompactEncoder
import json

def test_primitives():
    assert CompactEncoder().encode(5) == "5"
    assert CompactEncoder().encode(5.5) == "5.5"
    assert CompactEncoder().encode(True) == "true"
    assert CompactEncoder().encode(False) == "false"
    assert CompactEncoder().encode(None) == "null"
    assert CompactEncoder().encode("Test") == '"Test"'

def _test_file(fp):
    with open(fp, 'r') as f:
        f_str = f.read()
        f.seek(0)  # Reset file read
        f_obj = json.load(f)
    assert f_str == CompactEncoder().encode(f_obj)

# Testing different files
def test_files():
    _test_file('tests/data/int_lists.json')
    _test_file('tests/data/str_lists.json')
    _test_file('tests/data/dicts.json')


def test_iterencode():
    with open('tests/data/dicts.json', 'r') as f:
        f_obj = json.load(f)

    assert (
        CompactEncoder().encode(f_obj) ==
        ''.join([i for i in CompactEncoder().iterencode(f_obj)])
    )

