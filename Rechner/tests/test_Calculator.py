import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from Calculator import Schnittrechner
from utils import *

def test_calc_average():
    ects = [8, 7, 4, 3, 5, 3, 5, 3, 4, 6, 3, 3, 6, 3, 3, 3]
    grades = [3, 2, 2, 1, 4, 1, 3, 1, 3, 3, 1, 1, 3, 1, 1, 1]
    output = Schnittrechner.calculation_given(Schnittrechner, ects, grades)
    assert output == 2.2173913043478260869565217391304347826086956521739130434782608695

if __name__ == "__main__":
    test_calc_average()
    print("Everything passed")