"""Test the module :mod:`~pyhelpers.dbms`."""

import pytest

from pyhelpers.dbms import PostgreSQL


class TestPostgreSQL:
    testdb = PostgreSQL(
        host='localhost', port=5432, username='postgres', password=None, database_name='testdb')

    def test_init(self):
        assert self.testdb.address == 'postgres:***@localhost:5432/testdb'

    def test_get_database_names(self):
        assert 'postgres' in self.testdb.get_database_names()

    def test_database_exists(self):
        assert self.testdb.database_exists()

    def test_get_database_size(self):
        assert ' kB' in self.testdb.get_database_size()

    def test_schema_exists(self):
        assert self.testdb.schema_exists('public')

    def test_create_schema(self, capfd):
        """Test .create_schema, .schema_exists, .drop_schema, and .get_schema_names() """
        test_schema_name = 'test_schema'

        assert not self.testdb.schema_exists(schema_name=test_schema_name)

        self.testdb.create_schema(schema_name=test_schema_name, verbose=True)
        out, _ = capfd.readouterr()
        assert f'Creating a schema: "{test_schema_name}" ... Done.' in out

        assert self.testdb.schema_exists(test_schema_name)

        assert 'public' in self.testdb.get_schema_names()

        self.testdb.drop_schema(
            schema_names=test_schema_name, confirmation_required=False, verbose=True)
        out, _ = capfd.readouterr()
        assert 'Dropping' in out and 'Done.' in out


if __name__ == '__main__':
    pytest.main()
