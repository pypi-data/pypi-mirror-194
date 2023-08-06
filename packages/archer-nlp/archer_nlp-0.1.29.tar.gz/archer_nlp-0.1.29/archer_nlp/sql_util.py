import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from archer_nlp.common_utils import except_info


def escape(q):
    """
    sqlalchemy转义，如单引号
    :param q:
    :return:
    """
    # 注：英文冒号是sqlalchemy的关键词
    return pymysql.converters.escape_string(q.strip()).replace(':', '\:')


class DataBase:
    def __init__(self, url, table):
        engine = create_engine(url, pool_recycle=30)
        self.session = scoped_session(sessionmaker(bind=engine))
        self.table = table

    def execute_query(self, query=None, keys=None, table=None, where='', fetch=0):
        """
        执行sql语句
        :param query: 直接执行sql语句
        :param keys:
        :param table:
        :param where:
        :param fetch: 0：返回cursor，1：返回第一行，2：返回所有行
        :return:
        """
        try:
            if query is None:
                query = 'SELECT '
                if keys is None:
                    query += '*'
                else:
                    query += keys
                if table is None:
                    query += ' FROM ' + self.table
                else:
                    query += ' FROM ' + table
                if where:
                    query += " WHERE " + where

            res = self.session.execute(query)
            if fetch == 0:
                return res
            elif fetch == 1:
                return res.fetchone()
            else:
                return res.fetchall()
        except Exception as e:
            print(except_info(e))
            raise Exception('execute_query error!')
        finally:
            self.session.close()

    def insert_table(self, insert_dic=None):
        """
        插入数据表
        :param session:
        :param table:
        :param insert_dic:
        :return:
        """
        if insert_dic is None:
            insert_dic = {}
        query = f"insert into {self.table}("
        try:
            for insert_name in insert_dic.keys():
                query += f"{insert_name},"
            query = query.strip(',') + ') values('

            for insert_value in insert_dic.values():
                if isinstance(insert_value, str):
                    insert_value = escape(insert_value)
                    query += f"'{insert_value}',"
                else:
                    query += f"{insert_value},"
            query = query.strip(',') + ')'
            self.session.execute(query)
            self.session.commit()
        except Exception as e:
            print(except_info(e))
            raise Exception('insert to table error!')
        finally:
            self.session.close()

    def update_table(self, where=None, update_dic=None):
        """
        更新数据表
        :param session:
        :param table:
        :param where: 可为空
        :param update_dic:
        :return:
        """
        if where is None:
            where = {}
        if update_dic is None:
            update_dic = {}
        try:
            query = f"UPDATE {self.table} SET "
            for update_name, update_value in update_dic.items():
                if isinstance(update_value, str):
                    update_value = escape(update_value)
                    query += f"{update_name}='{update_value}',"
                else:
                    query += f"{update_name}={update_value},"

            query = query.strip(',')
            if where:
                query += " WHERE "
                for where_key, where_value in where.items():
                    if isinstance(where_value, str):
                        where_value = escape(where_value)
                        query += f"{where_key}='{where_value}' and "
                    else:
                        query += f"{where_key}={where_value} and "
                query = query.strip(' and ')
            self.session.execute(query)
            self.session.commit()
        except Exception as e:
            print(except_info(e))
            raise Exception('update table error!')
        finally:
            self.session.close()
