import badlisp
import pytest

@pytest.mark.parametrize(('input', 'expected'), [
        ('(3)', ['3']),
        ('(1,000,000)', ['1,000,000']),
        ("(hi there man)", ['hi', 'there', 'man']),
        ("(something (nested here) and (there))", 
         ['something', ['nested', 'here'], 'and', ['there']]),
])
def test_parse__good_parses(input, expected):
    assert badlisp.parse(input) == expected


@pytest.mark.parametrize(('input', 'expected'), [
        (['3'], [3]),
        (['2', '3'], [2, 3]),
        (['1', '2', '3'], [1, 2, 3])
])
def test_eval__good_evaluate(input, expected):
    assert badlisp.evaluate(input) == expected
