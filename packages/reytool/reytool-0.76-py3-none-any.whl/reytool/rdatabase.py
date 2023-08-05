# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's database methods.
"""


from typing import Any, List, Dict, Iterable, Optional, Literal, Union
import re
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.cursor import LegacyCursorResult
from sqlalchemy.sql.elements import TextClause

from .rbasic import get_first_notnull, error
from .rdata import to_table, to_df, to_json, to_sql, to_html, to_csv, to_excel
from .roption import print_default_frame_full
from .rtext import rprint
from .rtime import now
from .rwrap import runtime


def monkey_patch_more_fetch() -> None:
    """
    Add more methods to LegacyCursorResult object of sqlalchemy package.
    """

    # Fetch SQL result to table in List[Dict] format.
    LegacyCursorResult.fetch_table = to_table

    # Fetch SQL result to DataFrame object.
    LegacyCursorResult.fetch_df = to_df

    # Fetch SQL result to JSON string.
    LegacyCursorResult.fetch_json = to_json

    # Fetch SQL result to SQL string.
    LegacyCursorResult.fetch_sql = to_sql

    # Fetch SQL result to HTML string.
    LegacyCursorResult.fetch_sql = to_html

    # Fetch SQL result to save csv format file.
    LegacyCursorResult.fetch_csv = to_csv

    # Fetch SQL result to save excel file.
    LegacyCursorResult.fetch_excel = to_excel

monkey_patch_more_fetch()

class RConnect(object):
    """
    Rey's database connection type, based on the package sqlalchemy.
    """

    # Values to be converted to None.
    none_values: List = ["", " ", b"", [], (), {}, set()]
    
    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        charset: Optional[str] = None,
        once: bool = True,
        conn: Optional[Union[Engine, Connection]] = None,
        recreate_ms: int = 7_200_000
    ) -> None:
        """
        Set database connection parameters.

        Parameters
        ----------
        user : Server user name.
        password : Server password.
        host : Server host.
        port : Server port.
        database : Database name in the server.
        charset : Coding charset.
        once : Whether the connection object is one time, and create for each execution.
        conn : Existing connection object, will get parameters from it, but preferred input parameters.
        recreate_ms : Connection object recreate interval millisecond.
        """

        # Get parameters from existing connection object.
        if type(conn) == Connection:
            conn = conn.engine
        if type(conn) == Engine:
            user = get_first_notnull(user, conn.url.username)
            password = get_first_notnull(password, conn.url.password)
            host = get_first_notnull(host, conn.url.host)
            port = get_first_notnull(port, conn.url.port)
            database = get_first_notnull(database, conn.url.database)
            charset = get_first_notnull(charset, conn.url.query.get("charset"))
            conn = conn.connect(close_with_result=once)

        # Set parameters.
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.charset = charset
        self.once = once
        self.conn = conn
        self.conn_timestamp = now("timestamp")
        self.recreate_ms = recreate_ms

    def create_conn(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        database: Optional[str] = None,
        charset: Optional[str] = None,
        once: bool = None
    ) -> Connection:
        """
        Get database connection engine.

        Parameters
        ----------
        user : Server user name.
        password : Server password.
        host : Server host.
        port : Server port.
        database : Database name in the server.
        charset : Coding charset.
        once : Whether the connection object is one time, and create for each execution.

        Returns
        -------
        Connection object.
        """

        # Check whether the connection object is invalid.
        if self.conn != None \
            and (
                now("timestamp") > self.conn_timestamp + self.recreate_ms \
                or self.conn.closed
            ):
            self.conn.close()
            self.conn = None

        # Judge whether existing connection objects can be reused.
        elif self.conn != None \
            and (user == None or self.conn.engine.url.username == user) \
            and (password == None or self.conn.engine.url.password == password) \
            and (host == None or self.conn.engine.url.host == host) \
            and (port == None or self.conn.engine.url.port == port) \
            and (database == None or self.conn.engine.url.database == database) \
            and (charset == None or self.conn.engine.url.query["charset"] == charset):
            return self.conn

        # Get parameters by priority.
        user: str = get_first_notnull(user, self.user, default="error")
        password: str = get_first_notnull(password, self.password, default="error")
        host: str = get_first_notnull(host, self.host, default="error")
        port: Union[str, int] = get_first_notnull(port, self.port, default="error")
        database: str = get_first_notnull(database, self.database, default="error")
        charset: str = get_first_notnull(charset, self.charset, default="utf8")
        once: str = get_first_notnull(once, self.once, default=True)

        # Create connection object.
        try:
            url = f"mysql+mysqldb://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        except ModuleNotFoundError:
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        conn = engine.connect(close_with_result=once)

        # Save connection object.
        if self.conn == None and not once:
            self.conn = conn
            self.conn_timestamp = now("timestamp")
        return conn

    def fill_sql_none(
        self,
        sql: Union[str, TextClause],
        params: Union[Dict, List[Dict]],
        fill_field: bool = True,
        none_values: List = none_values
    ) -> Union[Dict, List[Dict]]:
        """
        Fill missing parameters according to contents of sqlClause object of sqlalchemy module.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format or return of sqlalchemy.text.
        params : Parameters set for filling sqlalchemy.text.
        fill_field : Whether fill missing fields.
        none_values : Values to be converted to None.

        Returns
        -------
        Filled parameters.
            - When parameter params is Dict, then return Dict.
            - When parameter params is List[Dict], then return List[Dict].
        """

        if type(sql) == TextClause:
            sql = sql.text
        pattern = "(?<!\\\):(\w+)"
        sql_keys = re.findall(pattern, sql)
        if type(params) == dict:
            for key in sql_keys:
                if fill_field:
                    val = params.get(key)
                else:
                    val = params[key]
                if val in none_values:
                    val = None
                params[key] = val
        else:
            for param in params:
                for key in sql_keys:
                    if fill_field:
                        val = param.get(key)
                    else:
                        val = param[key]
                    if val in none_values:
                        val = None
                    param[key] = val
        return params

    def execute(
        self,
        sql: Union[str, TextClause],
        params: Optional[Union[List[Dict], Dict]] = None,
        database: Optional[str] = None,
        fill_field: bool = True,
        none_values: List = none_values,
        once: bool = None,
        report: bool = False,
        **kw_params: Any
    ) -> LegacyCursorResult:
        """
        Execute SQL.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format or return of sqlalchemy.text.
        params : Parameters set for filling sqlalchemy.text.
        database : Database name.
        fill_field : Whether fill missing fields.
        none_values : Values to be converted to None.
        once : Whether the database conn engine is one-time (i.e. real time creation).
        report : Whether print SQL and SQL runtime.
        kw_params : Keyword parameters for filling sqlalchemy.text.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        once = get_first_notnull(once, self.once, default=True)

        if type(sql) == str:
            sql = text(sql)
        if params != None:
            if type(params) == dict:
                params = [params]
            else:
                params = params.copy()
            for param in params:
                param.update(kw_params)
        else:
            params = kw_params
        if params != {}:
            params = self.fill_sql_none(sql, params, fill_field, none_values)
        conn = self.create_conn(database=database, once=once)
        if report:
            result, report_runtime = runtime(conn.execute, sql, params, _ret_report=True)
            report_info = "%s\nRow Count: %d" % (report_runtime, result.rowcount)
            if params == {}:
                rprint(report_info, sql, title="SQL", frame=print_default_frame_full)
            else:
                rprint(report_info, sql, params, title="SQL", frame=print_default_frame_full)
        else:
            result = conn.execute(sql, params)
        if once:
            conn.close()
            self.conn = None
        return result

    def execute_select(
            self,
            table: str,
            database: Optional[str] = None,
            fields: Optional[Union[str, Iterable]] = None,
            where: Optional[str] = None,
            order: Optional[str] = None,
            limit: Optional[Union[int, str, Iterable[Union[int, str]]]] = None,
            report: bool = False
        ) -> LegacyCursorResult:
        """
        Execute select SQL.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        fields : Select clause content.
            - None : Is 'SELECT *'.
            - str : Join as 'SELECT str'.
            - Iterable[str] : Join as 'SELECT \`str\`, ...'.

        where : 'WHERE' clause content, join as 'WHERE str'.
        order : 'ORDER BY' clause content, join as 'ORDER BY str'.
        limit : 'LIMIT' clause content.
            - Union[int, str] : Join as 'LIMIT int/str'.
            - Iterable[Union[str, int]] with length of 1 or 2 : Join as 'LIMIT int/str, ...'.

        report : Whether print SQL and SQL runtime.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        sqls = []
        if database == None:
            _database = self.database
        else:
            _database = database
        if fields == None:
            fields = "*"
        elif type(fields) != str:
            fields = ",".join(["`%s`" % field for field in fields])
        select_sql = (
            f"SELECT {fields}\n"
            f"FROM `{_database}`.`{table}`"
        )
        sqls.append(select_sql)
        if where != None:
            where_sql = "WHERE %s" % where
            sqls.append(where_sql)
        if order != None:
            order_sql = "ORDER BY %s" % order
            sqls.append(order_sql)
        if limit != None:
            list_type = type(limit)
            if list_type in [str, int]:
                limit_sql = f"LIMIT {limit}"
            else:
                if len(limit) in [1, 2]:
                    limit_content = ",".join([str(val) for val in limit])
                    limit_sql = "LIMIT %s" % limit_content
                else:
                    error("The length of the limit parameter value must be 1 or 2", ValueError)
            sqls.append(limit_sql)
        sql = "\n".join(sqls)
        result = self.execute(sql, database=database, report=report)
        return result

    def execute_update(
        self,
        data: Union[LegacyCursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        where_fields: Optional[Union[str, Iterable[str]]] = None,
        report: bool = False
    ) -> LegacyCursorResult:
        """
        Update the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.
        table : Table name.
        database : Database name.
        where_fields : 'WHERE' clause content.
            - None : Is 'WHERE \`%s\` = :%s' % (first field name and value of each item).
            - str : Is 'WHERE \`%s\` = :%s' % (str, str).
            - Iterable[str] : Is 'WHERE \`%s\` = :%s and ...' % (str, str, ...).

        report : Whether print SQL and SQL runtime.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = to_table(data)
        elif data_type == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database
        data_flatten = {}
        sqls = []
        if where_fields == None:
            no_where = True
        else:
            no_where = False
            if type(where_fields) == str:
                where_fields = [where_fields]
        for index, row in enumerate(data):
            for key, val in row.items():
                index_key = "%d_%s" % (index, key)
                data_flatten[index_key] = val
            if no_where:
                where_fields = [list(row.keys())[0]]
            set_content = ",".join(
                [
                    "`%s` = :%d_%s" % (key, index, key)
                    for key in row
                    if key not in where_fields
                ]
            )
            where_content = "\n    AND ".join(
                [
                    f"`{field}` = :{index}_{field}"
                    for field in where_fields
                ]
            )
            sql = (
                f"UPDATE `{_database}`.`{table}`\n"
                f"SET {set_content}\n"
                f"WHERE {where_content}"
            )
            sqls.append(sql)
        sqls = ";\n".join(sqls)
        result = self.execute(sqls, data_flatten, database, once=False, report=report)
        if self.once:
            self.conn == None
        return result

    def execute_insert(
        self,
        data: Union[LegacyCursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        duplicate_method: Optional[Literal["ignore", "update"]] = None,
        report: bool = False
    ) -> LegacyCursorResult:
        """
        Insert the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.
        table : Table name.
        database : Database name.
        duplicate_method : Handle method when constraint error.
            - None : Not handled.
            - 'ignore' : Use 'UPDATE IGNORE INTO' clause.
            - 'update' : Use 'ON DUPLICATE KEY UPDATE' clause.

        report : Whether print SQL and SQL runtime.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = self.to_table(data)
        elif data_type == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database
        fields = list({key for row in data for key in row})
        fields_str = ",".join(["`%s`" % field for field in fields])
        fields_str_position = ",".join([":" + field for field in fields])
        if duplicate_method == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        elif duplicate_method == "update":
            update_content = ",".join(["`%s` = VALUES(`%s`)" % (field, field) for field in fields])
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"{update_content}"
            )
        else:
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        result = self.execute(sql, data, database, report=report)
        return result