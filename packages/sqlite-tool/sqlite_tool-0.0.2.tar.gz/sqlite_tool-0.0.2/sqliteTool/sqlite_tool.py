# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sqlite_tool
   Author :        sss
   date：          2023-2-24
-------------------------------------------------
   Change Activity:
                   2023-2-24:
-------------------------------------------------
"""
__author__ = 'sss'
import os
import sqlite3


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteTool:
    db_conn = None

    def __init__(self, db_path, db_name: str):
        self.db_path = db_path
        self.db_name = db_name
        self.db_conn = self.getConn()

    def getConn(self):
        sqlPath = os.path.join(self.db_path, self.db_name)
        if self.db_conn is None:
            try:
                _conn = sqlite3.connect(sqlPath)
            except Exception as error:
                _conn = None
                raise error
        else:
            _conn = self.db_conn
        return _conn

    def execute(self, sql, args=[], result_dict=True, commit=True) -> list:
        """
        执行数据库操作的通用方法
        Args:
        sql: sql语句
        args: sql参数
        result_dict: 操作结果是否用dict格式返回
        commit: 是否提交事务
        """
        if result_dict:
            self.db_conn.row_factory = _dict_factory
        else:
            self.db_conn.row_factory = None
        # 获取游标
        _cursor = self.db_conn.cursor()
        # 执行SQL获取结果
        try:
            _cursor.execute(sql, args)
        except Exception as error:
            raise error
        if commit:
            self.db_conn.commit()
        data = _cursor.fetchall()
        _cursor.close()
        return data

    def closeConn(self):
        self.db_conn.close()

    def __del__(self):
        self.closeConn()


if __name__ == '__main__':
    pass
