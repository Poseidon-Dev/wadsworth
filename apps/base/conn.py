import psycopg2
import core.config
from core.config import log

import apps.base.exceptions as BaseErr

class DBConnection:

    def __init__(self):
        self.host = core.config.PG_HOST
        self.db_name = core.config.PG_DB[0]
        self.user = core.config.PG_USR[0]
        self.pwd = core.config.PG_PWD[0]
        self.port = core.config.PG_PORT


    def conn(self):
        """
        Creates a connection object to the localDB
        """
        conn = psycopg2.connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.pwd,
            port=self.port
        )
        log.info(conn)
        return conn

    def close(self):
        """
        Closes postgres connections
        """
        self.conn.close()

class ExecuteMixin:

    def __init__(self):
        self.conn = None
        self.cur = None
        

    def execute(self, command):
        """
        Simple cursor execution
        """
        self.conn = DBConnection().conn()
        self.cur = self.conn.cursor()
        log.info(command)
        try:
            response = ''
            self.cur.execute(command)
            try:
                response = self.cur.fetchall()
            except Exception as err:
                log.error(err)
            log.info(f'DATA: {bool(response)}')
            self.conn.commit()
            self.conn.close()
        except (
            BaseErr.UndefinedTable,
            BaseErr.UndefinedColumn,
            BaseErr.UndefinedFunction,
            BaseErr.PsqlSyntaxError
            ) as err:
            log.error(err)
            self.conn.rollback()
            self.conn.close()
            response = ''
            return err
        except Exception as e:
            print(f'uncaught exeception: {e}')
        finally:
            return response

class TableBuilder(ExecuteMixin):

    def __init__(self, table, columns):
        super().__init__()
        self.table = table
        self.columns = columns

    def build(self):
        columns = ',\n'.join(map(
            lambda x: str(x[0]) + ' ' + str(x[1]),
            self.columns))
        command = f"""
        CREATE TABLE IF NOT EXISTS {self.table}(
            {columns}
        );
        """
        log.info(command)
        self.execute(command)
