'''module responsable for tests'''
import question_b.version_compare as question_b


def test_int_int():
    #int-int
    assert 'lower' in question_b.version_compare(1, 2)
    assert 'greater' in question_b.version_compare(2, 1)
    assert 'equal' in question_b.version_compare(1, 1)
def test_float_float():
    #float-float
    assert 'lower' in question_b.version_compare(1.1, 2.1)
    assert 'greater' in question_b.version_compare(2.1, 1.1)
    assert 'equal' in question_b.version_compare(1.1, 1.1)
def test_srting_string():
    #string-string
    assert 'lower' in question_b.version_compare('1.1', '2.1')
    assert 'greater' in question_b.version_compare('2.1', '1.1')
    assert 'equal' in question_b.version_compare('1.1', '1.1')
def test_int_float():
    #int-float
    assert 'lower' in question_b.version_compare(1, 2.1)
    assert 'greater' in question_b.version_compare(2, 1.1)
    assert 'equal' in question_b.version_compare(1, 1.0)
def test_float_int():
    #float-int
    assert 'lower' in question_b.version_compare(1.1, 2)
    assert 'greater' in question_b.version_compare(2.1, 1)
    assert 'equal' in question_b.version_compare(1.0, 1)
def test_int_string():
    #int-string
    assert 'lower' in question_b.version_compare(1, '2')
    assert 'greater' in question_b.version_compare(2, '1')
    assert 'equal' in question_b.version_compare(1, '1')
def test_string_int():
    #string-int
    assert 'lower' in question_b.version_compare('1', 2)
    assert 'greater' in question_b.version_compare('2', 1)
    assert 'equal' in question_b.version_compare('1', 1)
def test_float_string():
    #float-string
    assert 'lower' in question_b.version_compare(1.1, '2')
    assert 'greater' in question_b.version_compare(2.1, '1')
    assert 'equal' in question_b.version_compare(1.0, '1')
def test_string_float():
    #string-float
    assert 'lower' in question_b.version_compare('1', 2.0)
    assert 'greater' in question_b.version_compare('2', 1.1)
    assert 'equal' in question_b.version_compare('1', 1.0)
