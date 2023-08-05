import pytest
import sdfspu.csv_data as cd


@pytest.fixture
def data():
    return cd.DataObject()


def test_object_type(data):
    assert isinstance(data, cd.DataObject)


def test_info_msg(data):
    assert isinstance(data.info_msg(), str)


# TODO tests for DataObject methods

# def test_read_csv(data):
#     assert False

# def test_print_fields_usage():
#     assert False


# TODO tests for other functions in csv_data

# def test_csv_file_to_dict_list():
#     assert False


# def test_csv_from_url_to_dict_list():
#     assert False


# def test_write_dict_to_csv():
#     assert False


# def test_write_dict_list_to_csv():
#     assert False


# def test_key_homogenised_dict_list():
#     assert False


# def test_add_field_to_dict_list():
#     assert False


# def test_divide_duplicates():
#     assert False
