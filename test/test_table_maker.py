from __future__ import division

import shutil
import filecmp

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

    expected_ra = np.array(['08:13:49.440',
                            '06:35:03.600'])

    expected_dec = np.array(['+78:54:00.000',
                             '-43:12:36.000'])

    actual_ra, actual_dec = convert_decimal_degree_columns_to_sexagesimal(
        test_ra_decimal_degrees, test_dec_decimal_degrees)

    assert (expected_ra == actual_ra).all()
    assert (expected_dec == actual_dec).all()

def test_make_megeath_class_column():

    # Let's make sure that all the D's stay D's, all the P's stay P's,
    # and that all the na's transform into either na's or NDs.

    new_class_column = make_megeath_class_column()

    old_class_column = megeath2012_by_ukvar.Class

    assert (len(old_class_column[old_class_column == 'D']) ==
            len(new_class_column[new_class_column == 'D']))

    assert (len(old_class_column[old_class_column == 'P']) ==
            len(new_class_column[new_class_column == 'P']))

    assert (len(old_class_column[old_class_column == 'na']) ==
            len(new_class_column[new_class_column == 'ND']) +
            len(new_class_column[new_class_column == 'na']))

    # make sure you DID change SOMETHING
    assert (len(old_class_column[old_class_column == 'na']) !=
            len(new_class_column[new_class_column == 'na']))


    # and finally make sure you didn't swap the order of any D's or P's
    assert (old_class_column[(old_class_column == 'D') |
                             (old_class_column == 'P')] ==
            new_class_column[(new_class_column == 'D') |
                             (new_class_column == 'P')] ).all()


def test_convert_tabletabular_to_deluxetable():

    origin_file = "test/convert_tabletabular_to_deluxetable_testfile.tex"
    converted_file = "test/convert_tabletabular_to_deluxetable_testfile_converted.tex"
    expected_file = "test/convert_tabletabular_to_deluxetable_testfile_expected.tex"

    # we don't want to start with identical files
    assert filecmp.cmp(origin_file, expected_file, shallow=False) == False

    shutil.copy(origin_file, converted_file)

    convert_tabletabular_to_deluxetable(converted_file)

    assert filecmp.cmp(converted_file, expected_file, shallow=False) == True

    os.remove(converted_file)
