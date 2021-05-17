from core.config import log
import apps.base.exceptions as BaseErr
from apps.base.conn import DBConnection

class ExecuteMixin:
    """
    Establish connection with psqldb and create a standard execute/commit method
    """
    def __init__(self):
        self.conn = DBConnection().conn()
        self.cur = self.conn.cursor()
        

    def execute(self, command):
        """
        Simple cursor execution
        """
        log.info(command[:250])
        try:
            response = ''
            self.cur.execute(command)
            try:
                response = self.cur.fetchall()
            except Exception as err:
                log.error(err)
            log.info(f'DATA: {bool(response)}')
            self.conn.commit()
        except (
            BaseErr.UndefinedTable,
            BaseErr.UndefinedColumn,
            BaseErr.UndefinedFunction,
            BaseErr.PsqlSyntaxError
            ) as err:
            log.error(err)
            self.conn.rollback()
            response = ''
            return err
        except Exception as e:
            print(f'uncaught exeception: {e}')
        finally:
            return response

class QueryBase(ExecuteMixin):

    def __init__(self, table=''):
        super().__init__()
        self.table = table
        self.base_command = ''
        self.command = ''

    def filter(self, col: str = 'id', val: str = '', op: str = "="):
        if val:
            command = ''
            if 'WHERE' in self.command:
                command += f" AND {col} {op} '{val}'"
            else:
                command += f" WHERE {col} {op} '{val}'"
            self.statement_helper(command)
        return self

    def filter_like(self, col: str='id', val: str='', op: str="like", like=''):
        if val:
            if not like:
                val = f'{val}%'
            elif like == 'end':
                val = f'%{val}'
            else:
                val = f'%{val}%'
            self.filter(col, val, op)
        return self

    def columns(self, columns="*"):
        if type(columns) is list:
            columns = ', '.join(columns)
        if "*" in self.command:
            self.command = self.command.replace('*', f'{columns}')
        else:
            self.command = self.base_command.replace('*', f'{columns}')
        return self

    def order(self, by: str = 'id', order: str = ''):
        command = f' ORDER BY {by} {order} '
        self.statement_helper(command)
        return self

    def join(self, table='', current_tbl_field='', join_tbl_field='id'):
        command = f'JOIN {table} ON {table}.{join_tbl_field} = {self.table}.{current_tbl_field}'
        if self.command:
            self.command.replace(f'{self.table}', f'{self.table} {command}')
        else:
            self.command = self.base_command.replace(f'{self.table}', f'{self.table} {command}')
        return self

    def limit(self, amount=1):
        command = f' LIMIT {amount}'
        if self.command:
            self.command += command
        else:
            self.command = self.base_command + command
        return self

    def all(self):
        self.command += f'SELECT * FROM {self.table}'
        return self
        
    def query(self, command=''):
        if not command:
            return self.execute(self.command + ';')
        else:
            return self.execute(command + ';')

    def statement_helper(self, command):
        if not self.command:
            self.command += self.base_command
        self.command += command

class QueryMixin(QueryBase):

    def __init__(self, table=''):
        self.table = table
        super().__init__(self.table)
        self.base_command = f'SELECT * FROM {self.table}'
        self.command = ''

    def select_last(self): 
        return self.order(order='DESC').limit()

    def select_first(self): 
        return self.order().limit()

    def count(self):
        return self.columns(['COUNT (*)',])

    def delete(self, records):
        records = records.command.replace('SELECT *', 'DELETE')
        records = records.replace('SELECT', 'DELETE')
        self.query(command=records)

    def insert(self, records):
        cols = [str(record[0]) for record in records]
        cols = ', '.join(cols)
        vals = [str(record[1]) for record in records]
        vals = ', '.join(map(lambda x: f"'{x}'", vals))
        command = f"""
        INSERT INTO {self.table} ({cols}) VALUES ({vals})
        ON CONFLICT ON CONSTRAINT {self.table}_pkey DO NOTHING;
        """
        self.execute(command)
        return True

    def insert_many(self, cols, vals):
        """ 
        Accepts a list of tupes as values and dumps into current table
        """
        vals = str(vals).strip('[]')
        command = f"""
        INSERT INTO {self.table} ({cols})
        VALUES {vals}
        ON CONFLICT ON CONSTRAINT {self.table}_pkey DO NOTHING;
        """
        self.execute(command)

    def update_record(self, record, updates):
        detail = ', '.join(f"{update[0]} = '{update[1]}'" for update in updates)
        command = f"""
        UPDATE {self.table} SET {detail} WHERE id = {record[0][0]}; 
        """
        return command

    def manual(self, command):
        self.execute(command)


class Query(QueryMixin):

    def __init__(self, table):
        self.table = table
        super().__init__(self.table)