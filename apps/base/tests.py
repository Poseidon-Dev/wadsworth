import testing.postgresql
import unittest
import psycopg2


def test_multiple_postgresql(self):
    pgsql1 = testing.postgresql.Postgresql()
    pgsql2 = testing.postgresql.Postgresql()
    self.assertNotEqual(pgsql1.server_pid, pgsql2.server_pid)
 
    self.assertTrue(pgsql1.is_alive())
    self.assertTrue(pgsql2.is_alive())

def test_idk(self):
    self.assertTrue('FOO'.isupper())

def tearDown(self):
    self.postgresql.stop()


unittest.main()