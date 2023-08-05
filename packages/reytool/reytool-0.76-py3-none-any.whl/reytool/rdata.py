# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's data methods.
"""


from typing import Any, List, Tuple, Dict, Iterable, Literal, Optional, Union, Type
from sqlalchemy.engine.cursor import LegacyCursorResult
from pandas import DataFrame, ExcelWriter

from .rbasic import is_iterable, check_least_one, to_type
from .rtime import time_to_str


def to_table(
    data: Union[LegacyCursorResult, DataFrame, List[Dict], Iterable[Iterable]],
    fields: Optional[Iterable] = None
) -> List[Dict]:
    """
    Fetch data to table in List[Dict] format, keys and keys sort of the dictionary are the same.

    Parameters
    ----------
    data : Data.
    fields : Table fields.
        - None : Infer.
        - Iterable : Use values in Iterable.

    Returns
    -------
    Table in List[Dict] format.
    """

    data_type = type(data)
    if data_type == LegacyCursorResult:
        if fields == None:
            fields = data.keys()
        data_table = [dict(zip(fields, [val for val in row])) for row in data]
    elif data_type == DataFrame:
        data_df = data.copy()
        if fields != None:
            data_df.columns = fields
        data_df = data_df.where(data.notnull(), None)
        data_table = data_df.to_dict("records")
    else:
        data_df = DataFrame(data, columns=fields)
        data_df = data_df.where(data.notnull(), None)
        data_table = data_df.to_dict("records")
    return data_table

def to_df(data: Union[LegacyCursorResult, DataFrame, List[Dict], Iterable[Iterable]], fields: Optional[Iterable] = None) -> DataFrame:
    """
    Fetch data to table of DataFrame object.

    Parameters
    ----------
    data : Data.
    fields : Table fields.
        - None : Infer.
        - Iterable : Use values in Iterable.

    Returns
    -------
    DataFrame object.
    """

    data_type = type(data)
    if data_type == LegacyCursorResult:
        if fields == None:
            fields = data.keys()
        data_df = DataFrame(data, columns=fields)
    elif data_type == DataFrame:
        data_df = data.copy()
        if fields != None:
            data_df.columns = fields
        return data_df
    else:
        data_df = DataFrame(data, columns=fields)
    return data_df

def to_json(data: Union[LegacyCursorResult, DataFrame, List[Dict], Iterable[Iterable]], fields: Optional[Iterable] = None) -> str:
    """
    Fetch data to JSON string.

    Parameters
    ----------
    data : Data.
    fields : Table fields.
        - None : Infer.
        - Iterable : Use values in Iterable.

    Returns
    -------
    JSON string.
    """

    data_df = to_df(data, fields)
    data_json = data_df.to_json(orient="records", force_ascii=False)
    return data_json

def to_sql(data: Union[LegacyCursorResult, DataFrame, List[Dict], Iterable[Iterable]], fields: Optional[Iterable] = None) -> str:
    """
    Fetch data to SQL string.

    Parameters
    ----------
    data : Data.
    fields : Table fields.
        - None : Infer.
        - Iterable : Use values in Iterable.

    Returns
    -------
    SQL string.
    """

    data_type = type(data)
    if data_type == LegacyCursorResult:
        if fields == None:
            fields = data.keys()
    else:
        data = to_table(data, fields)
        fields = data[0].keys()
    sql_rows_values = [
        [
            repr(time_to_str(val, "%Y-%m-%d %H:%M:%S"))
            if val != None
            else "NULL"
            for val in row
        ]
        for row in data
    ]
    sql_rows = [
        "SELECT " + ",".join(row_values)
        for row_values in sql_rows_values
    ]
    sql_row_first = "SELECT " + ",".join(
        [
            "%s AS `%s`" % (val, key)
            for key, val in list(zip(fields, sql_rows_values[0]))
        ]
    )
    sql_rows[0] = sql_row_first
    data_sql = " UNION ALL ".join(sql_rows)
    return data_sql

def to_html(data: Union[LegacyCursorResult, DataFrame, List[Dict], Iterable[Iterable]], fields: Optional[Iterable] = None) -> str:
    """
    Fetch data to HTML string.

    Parameters
    ----------
    data : Data.
    fields : Table fields.
        - None : Infer.
        - Iterable : Use values in Iterable.

    Returns
    -------
    HTML string.
    """

    data_df = to_df(data, fields)
    data_html = data_df.to_html(col_space=50, index=False, justify="center")
    return data_html

def to_csv(
    data: Union[LegacyCursorResult, DataFrame, Iterable[Dict], Iterable],
    path: str = "table.csv",
    fields: Optional[Iterable] = None
) -> DataFrame:
    """
    Fetch data to save csv format file.

    Parameters
    ----------
    data : Data.
    path : File save path.
    fields : Table fields.
        - None : Infer.
        - Iterable : Use values in Iterable.
    """

    data_df = to_df(data, fields)
    data_df.to_csv(path, mode="a")
    return data_df

def to_excel(
    data: Union[LegacyCursorResult, DataFrame, Iterable[Dict], Iterable],
    path: str = "table.xlsx",
    group_field: Optional[str] = None,
    sheets_set: Dict[Union[str, int], Dict[Literal["name", "index", "filter"], Union[str, int, List[str]]]] = {}
) -> List[Tuple[str, DataFrame]]:
    """
    Fetch data to save excel format file and return sheet name and sheet data.

    Parameters
    ----------
    data : Data.
    path : File save path.
    group_field : Group filed.
    sheets_set : Set sheet new name and sort sheet and filter sheet fields,
        key is old name or index, value is set parameters.
        - Parameter 'name' : Set sheet new name.
        - Parameter 'index' : Sort sheet.
        - Parameter 'filter' : Filter sheet fields.

    Returns
    -------
    Sheet name and sheet data.
    """

    if type(data) != DataFrame:
        data = to_df(data)
    if group_field == None:
        data_group = (("Sheet1", data),)
    else:
        data_group = data.groupby(group_field)
    sheets_table_before = []
    sheets_table_after = []
    for index, sheet_table in enumerate(data_group):
        sheet_name, sheet_df = sheet_table
        if group_field != None:
                del sheet_df[group_field]
        if sheet_name in sheets_set:
            sheet_set = sheets_set[sheet_name]
        elif index in sheets_set:
            sheet_set = sheets_set[index]
        else:
            sheets_table_after.append((sheet_name, sheet_df))
            continue
        if "name" in sheet_set:
            sheet_name = sheet_set["name"]
        if "filter" in sheet_set:
            sheet_df = sheet_df[sheet_set["filter"]]
        if "index" in sheet_set:
            sheets_table_before.append((sheet_set["index"], (sheet_name, sheet_df)))
        else:
            sheets_table_after.append((sheet_name, sheet_df))
    sort_func = lambda item: item[0]
    sheets_table_before.sort(key=sort_func)
    sheets_table = [sheet_table for sheet_index, sheet_table in sheets_table_before] + sheets_table_after
    excel = ExcelWriter(path)
    for sheet_name, sheet_df in sheets_table:
        sheet_df.to_excel(excel, sheet_name, index=False)
    excel.close()
    return sheets_table

def count(
    data: Any,
    count_value: Dict = {"size": 0, "total": 0, "types": {}},
    surface: bool = True
) -> Dict[Literal["size", "total", "types"], Union[int, Dict[Type, int]]]:
    """
    Count data element.

    Parameters
    ----------
    data : Data.
    count_value : Cumulative Count.
    surface : Whether is surface recursion.

    Returns
    -------
    Count data.
    """

    data_type = type(data)
    count_value["total"] += 1
    count_value["types"][data_type] = count_value["types"].get(data_type, 0) + 1
    if data_type == dict:
        for element in data.values():
            count(element, count_value, False)
    elif is_iterable(data):
        for element in data:
            count(element, count_value, False)
    else:
        count_value["size"] = count_value["size"] + 1
    if surface:
        sorted_func = lambda key: count_value["types"][key]
        sorted_key = sorted(count_value["types"], key=sorted_func, reverse=True)
        count_value["types"] = {key: count_value["types"][key] for key in sorted_key}
        return count_value

def flatten(data: Any, flattern_data: List = []) -> List:
    """
    Flatten data.
    """

    data_type = type(data)
    if data_type == dict:
        for element in data.values():
            _ = flatten(element, flattern_data)
    elif is_iterable(data):
        for element in data:
            _ = flatten(element, flattern_data)
    else:
        flattern_data.append(data)
    return flattern_data

def split(data: Iterable, bin_size: Optional[int] = None, share: int = 2) -> List[List]:
    """
    Split data into multiple data.
    """

    check_least_one(bin_size, share)

    data = list(data)
    data_len = len(data)
    _data = []
    _data_len = 0
    if bin_size == None:
        average = data_len / share
        for n in range(share):
            bin_size = int(average * (n + 1)) - int(average * n)
            _data = data[_data_len:_data_len + bin_size]
            _data.append(_data)
            _data_len += bin_size
    else:
        while True:
            _data = data[_data_len:_data_len + bin_size]
            _data.append(_data)
            _data_len += bin_size
            if _data_len > data_len:
                break
    return _data

def de_dup(data: Iterable) -> List:
    """
    De duplication of data.

    Parameters
    ----------
    data : Data.

    Returns
    -------
    List after de duplication.
    """

    data = to_type(data, tuple)
    data_de_dup = list(set(data))
    data_de_dup.sort(key=data.index)
    return data_de_dup