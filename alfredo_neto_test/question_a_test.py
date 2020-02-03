'''module responsable for tests'''
import question_a.program as program

def test_true_intersection():
    assert True == program.has_intersection(1, 5, 2, 6)

def test_false_intersection():
    assert False == program.has_intersection(1, 5, 6, 8)