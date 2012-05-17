import badlisp
import pytest

@pytest.mark.parametrize(('input', 'expected'), [
        ('(3)', ['3']),
        ('(1,000,000)', ['1,000,000']),
        ("(hi there man)", ['hi', 'there', 'man']),
        ("(something (nested here) and (there))", 
         ['something', ['nested', 'here'], 'and', ['there']]),
        ('("some string")', ['"some string"']),
        ('("some \\" string")', ['"some \\" string"']), #escaped double quotes
        ('(`hi `3 `4)', ['`hi', '`3', '`4']),
        ('()', []),
        ('(3 ())', ['3', []]),
])
def test_parse(input, expected):
    assert badlisp.parse(input) == expected

@pytest.mark.parametrize(('input', 'expected'), [
    # same as in doctests
    ([1,2,3], 
     [1, 2, 3]),
    ([1, [2], [3]],
     [1, 2, 3]),
    ([1, [2, 3]],
     [1, [2, 3]])
])
def test_flatten(input, expected):
    assert badlisp.flatten(input) == expected

@pytest.mark.parametrize(('input', 'expected'), [
        ("(3)",                [3]),
        ("(1,000,000)",        [1000000]),
        ("(2 3)",              [2, 3]),
        ("(1 2 3)",            [1, 2, 3]),
        ("(1 (2))",            [1, 2]),
        ("(1 2 (3 4) 5)",      [1, 2, [3, 4], 5]),
        ("(+ 2 3)",            [5]),
        ("(- 5 2)",            [3]),
        ("(* 2 3)",            [6]),
        ("(/ 12 4)",           [3]),
        ("(< 23 4)",           [False]),
        ("(> 23 4)",           [True]),
        ("(= 5 5)",            [True]),
        ("(= 4 5)",            [False]),
        ("(^ 4 5)",            [1024]),
        ("(true)",             [True]),
        ("(true t false f 3)", [True, True, False, False, 3]),
        ("(and t t t t)",      [True]),
        ("(and t t t f)",      [False]),
        ("(or t f f f)",       [True]),
        ("(or f f f f)",       [False]),
        ("('a')",              ['a']),
        ("('a' 'b' 'c')",      ["a", "b", "c"]),
        ('("hi there")',       [['h','i',' ','t','h','e','r','e']]),
        ('("hi" "there")',     [['h','i'], ['t','h','e','r','e']]),
        ('(`hi `there)',       ['hi', 'there']),
        ('(`3 `4)',            ['3', '4']),
        ('(() () ())',         [[], [], []]),
])
def test_eval__numbers_and_arithmetic(input, expected):
    assert badlisp.evaluate(badlisp.parse(input)) == expected

@pytest.mark.parametrize(('input', 'expected'), [
        ("(hd (3 4 5 6 7))",   [3]),
        ("(tl (3 4 5 6 7))",   [4, 5, 6, 7]),
        #("(ht 3 4 5 6)",       [3, [4, 5, 6]]),
])
def test_eval__list_manip(input, expected):
    assert badlisp.evaluate(badlisp.parse(input)) == expected
