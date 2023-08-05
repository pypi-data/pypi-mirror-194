import csv

# import click
from requests import Session

# from requests.exceptions import ConnectionError
# from base64 import b64decode, b64encode
from .sdf_text import path_is_url
from .sdf_time import stamp_utc_now


class DataObject:
    def __init__(self):
        self.dict_list = []  # list of dictionaries; each dict is a record/row
        self.info = {
            "path_to_source": "",  # full path and filename
            "source_name": "",  # = full_path.rsplit('/', 1)[-1]
            "load_msg": "Data Loaded: None",
            "load_ok": False,
            "time_loaded": "not yet",
            "fields_usage": {0: []},
            "field_names": {"all": [], "used": [], "unused": []},
        }

    def info_msg(self):
        return "CSV Data: {} rows loaded ({} of {} fields in use)".format(
            str(len(self.dict_list)),
            len(self.info["field_names"]["used"]),
            len(self.info["field_names"]["all"]),
        )

    def read_csv(self, path_to_csv, encoding="utf-8"):
        try:
            if path_is_url(path_to_csv):
                self.dict_list = csv_from_url_to_dict_list(path_to_csv)
            else:
                self.dict_list = csv_file_to_dict_list(path_to_csv, encoding=encoding)
        except FileNotFoundError:
            self.info["load_msg"] = "Error Reading CSV: File Not Found"
            self.info["load_ok"] = False
            err_msg = "FileNotFoundError in read_csv()"
            print(err_msg)
            return False
        except UnicodeDecodeError:
            self.info["load_msg"] = "Error Reading CSV: Unicode Decode Error"
            self.info["load_ok"] = False
            err_msg = "UnicodeDecodeError in read_csv()"
            print(err_msg)
            return False

        self.info["path_to_source"] = path_to_csv
        self.info["source_name"] = path_to_csv.rsplit("/", 1)[-1]
        try:
            self.info["field_names"]["all"] = list(self.dict_list[0].keys())
        except IndexError:
            self.info["load_msg"] = "Error Reading CSV: IndexError reading dict_list[0]"
            self.info["load_ok"] = False
            print(self.info["load_msg"])
            return False

        # # Examine the CSV fields Used in the File
        # print('\nCounting how many records use each field:')
        # ...['fields_usage'] = {n: [field_names, used, n, times], ...}

        for field in self.dict_list[0].keys():
            count = 0
            for booking in self.dict_list:
                if booking[field]:
                    count += 1
            if count in self.info["fields_usage"]:
                self.info["fields_usage"][count].append(field)
            else:
                self.info["fields_usage"][count] = [field]

        for f in self.info["field_names"]["all"]:
            if f in self.info["fields_usage"][0]:
                self.info["field_names"]["unused"].append(f)
            else:
                self.info["field_names"]["used"].append(f)

        self.info["time_loaded"] = stamp_utc_now()
        self.info["load_msg"] = self.info_msg()
        self.info["load_ok"] = True
        return True

    # end def read_csv()

    def print_fields_usage(self):
        print("N rows using \t (fields)")
        for c in self.info["fields_usage"].keys():
            print("\t", c, "\t", self.info["fields_usage"][c])


# end class DataObject


def csv_file_to_dict_list(path, encoding="utf-8"):  #
    dict_list = []
    with open(path, encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row_dict in csv_reader:
            dict_list.append(row_dict)
    return dict_list


def csv_from_url_to_dict_list(path):
    dict_list = []
    with Session() as s:
        download = s.get(path)
        # print(download.headers)
        decoded_content = download.content.decode("utf-8")
        csv_reader = csv.DictReader(decoded_content.splitlines(), delimiter=",")
        for row_dict in csv_reader:
            dict_list.append(row_dict)
    return dict_list


def write_dict_to_csv(d, f):
    with open(f, "w", encoding="utf-8") as file:
        dw = csv.DictWriter(file, fieldnames=list(d.keys()))
        dw.writeheader()
        dw.writerow(d)


def write_dict_list_to_csv(dl, f):
    with open(f, "w", encoding="utf-8") as file:
        dw = csv.DictWriter(file, fieldnames=list(dl[0].keys()))
        dw.writeheader()
        for d in dl:
            dw.writerow(d)


def key_homogenised_dict_list(dict_list_in) -> list:
    """
    :param dict_list_in: dict list, maybe with field key heterogeneity
    :return: dict list where each dict has the same set of keys
    """
    try:
        key_list = list(dict_list_in[0].keys())
    except IndexError:
        return [
            {"Error": "in key_homogenised_dict_list(dict_list_in)->list"},
            {"Error": "IndexError"},
            {"Error": "key_list = list(dict_list_in[0].keys())"},
        ]

    r_dict_list = []

    # look for new keys
    for d in dict_list_in:
        for dk in d.keys():
            if dk not in key_list:
                # print('new key:', dk)
                key_list.append(dk)

    # make new dict list, applying new keys where needed
    for d in dict_list_in:
        r_dict = {}
        for dk in d.keys():
            r_dict[dk] = d[dk]
        for lk in key_list:
            if lk not in d.keys():
                r_dict[lk] = ""
        r_dict_list.append(r_dict)
    return r_dict_list


# end def key_homogenised_dict_list(dict_list_in)


def add_field_to_dict_list(dict_list, f_key, f_value=""):
    """add a new field to every dict in a dict_list, same data value in each
    :param dict_list: list of dict
    :param f_key: field key name to add
    :param f_value: (optional) data value for new field
    :return: dict_list
    """
    r_dict_list = []
    for d in dict_list:
        r_dict = {f_key: f_value}
        for dk, dv in d.items():
            r_dict[dk] = dv
        r_dict_list.append(r_dict)
    return r_dict_list


# end def add_field_to_dict_list()


def divide_duplicates(dict_list, field, mode="Move"):
    """

    :param dict_list:
    :param field: field name key in dict to look at
    :param mode: only 'Move' is implemented
    :return: dict with 'input' and 'field info' string items, plus three dict_list items
    """

    r_data = {
        "input": "dict_list length: {}, field: {}, mode: {}".format(
            len(dict_list), field, mode
        )
    }

    values_in_data = []  # list of strings
    values_duplicated = []  # list of strings
    values_ok_dict_list = []  # list of dict records

    values_missing_dict_list = []  # list of dict records
    unique_in_field_dict_list = []
    duplic_in_field_dict_list = []

    for r in dict_list:
        try:
            value = r[field]
            if not value:
                values_missing_dict_list.append(r)
            elif value in values_in_data:
                values_duplicated.append(value)
                values_ok_dict_list.append(r)
            else:
                values_in_data.append(value)
                values_ok_dict_list.append(r)
        except KeyError:
            r_data["field info"] = "KeyError with field: {}".format(field)
            r_data["unique_in_field_dict_list"] = unique_in_field_dict_list
            r_data["duplic_in_field_dict_list"] = duplic_in_field_dict_list
            r_data["values_missing_dict_list"] = values_missing_dict_list
    # end for r dict_list

    r_data["field info"] = "{} values, {} duplicates, {} missing".format(
        len(values_in_data), len(values_duplicated), len(values_missing_dict_list)
    )

    for r in sorted(values_ok_dict_list, key=lambda f: f[field]):
        value = r[field]
        if mode == "Move":
            if value in values_duplicated:
                duplic_in_field_dict_list.append(r)
            else:
                unique_in_field_dict_list.append(r)
        else:
            pass

    r_data["unique_in_field_dict_list"] = unique_in_field_dict_list
    r_data["duplic_in_field_dict_list"] = duplic_in_field_dict_list
    r_data["values_missing_dict_list"] = values_missing_dict_list

    return r_data


# end def divide_duplicates()

# # # # Deprecated stuff from teh 2018 version of this utility

# def s2b(s):
#     return b64encode(s.encode())
#
#
# def b2s(b):
#     if isinstance(b, type('')):
#         r = b == 'True' if b in ('True', 'False') else b2s(bytes(b.encode()))
#     else:
#         r = b64decode(b).decode()
#     return r
#
#
# def ds2db(d):
#     r = {}
#     for k in d.keys():
#         r[s2b(k)] = s2b(d[k]) if isinstance(d[k], type('')) else d[k]
#     return r
#
#
# def db2ds(d):
#     r = {}
#     for k in d.keys():
#         r[b2s(k)] = b2s(bytes(d[k])) if isinstance(d[k], type(b'')) else d[k]
#     return r
#
#
# def ds2ef(s, f):
#     write_dict_to_csv(ds2db(s), f)
#
#
# def ef2ds(f):
#     d = csv_file_to_dict_list(f)[0]
#     r = {}
#     for k in d.keys():
#         r[fs2s(k)] = fs2s(d[k])
#     return r
#
#
# def fs2s(fs):
#     if fs in ('True', 'False'):
#         return fs == 'True'
#     return b2s(bytes(fs.split("'")[1].encode()))
#
#
# @click.command()
# def csv_cli():
#     click.echo('/! {}'.format(stamp_utc_now()))
#
#
# if __name__ == '__main__':
#     csv_cli()
