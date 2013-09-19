from __future__ import division

from table_maker import *
    
def test_join_columns_with_plusminus():

    test_values = np.arange(10)*1.
    test_errors = np.sin(np.arange(10))
    
    expected = np.array( [str(round(x,3))+r"$\pm$"+str(round(y,3)) for
                          x, y in zip(test_values, test_errors)] )

    actual = join_columns_with_plusminus(test_values, test_errors, 3)

    assert (expected == actual).all()
    
