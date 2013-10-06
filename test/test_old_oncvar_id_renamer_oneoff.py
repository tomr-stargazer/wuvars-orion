from old_oncvar_id_renamer_oneoff import *

import numpy as np

def test_simple_case():

    id_column = np.arange(20)
    new_id_column = np.arange(20) + 5
    
    input_table = atpy.Table()

    input_table.add_column('ONCvar_ID', id_column)
    input_table.add_column('UKvar_ID', new_id_column)

    expected_table = atpy.Table()

    expected_table.add_column('old_ONCvar_ID', id_column)
    expected_table.add_column('UKvar_ID', new_id_column)

    assert input_table.columns.keys != expected_table.columns.keys

    renamed_input_table = renamer(input_table)

    assert renamed_input_table.columns.keys == expected_table.columns.keys

    for column in expected_table.columns.keys:

        assert (renamed_input_table[column] == expected_table[column]).all()


