from __future__ import division

from table_maker import *
    
def test_join_columns_with_plusminus():

    test_values = np.arange(10)*1.
    test_errors = np.sin(np.arange(10))
    
    expected = np.array( [str(round(x,3))+r"$\pm$"+str(round(y,3)) for
                          x, y in zip(test_values, test_errors)] )

    actual = join_columns_with_plusminus(test_values, test_errors, 3)

    assert (expected == actual).all()

def test_convert_decimal_degree_columns_to_sexagesimal():

    test_ra_decimal_degrees = [123.456,
                               98.765]
    test_dec_decimal_degrees = [+78.9,
                                -43.21]

    expected_ra = np.array(['08:13:49.44',
                            '06:35:03.60'])

    expected_dec = np.array(['+78:54:00.00',
                             '-43:12:36.00'])

    actual_ra, actual_dec = convert_decimal_degree_columns_to_sexagesimal(
        test_ra_decimal_degrees, test_dec_decimal_degrees)

    assert (expected_ra == actual_ra).all()
    assert (expected_dec == actual_dec).all()
