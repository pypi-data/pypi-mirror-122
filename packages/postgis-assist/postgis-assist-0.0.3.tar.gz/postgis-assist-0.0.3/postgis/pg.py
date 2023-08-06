import psycopg2

class pg:
    def __init__(self, dbname=None, user="postgres", password="admin", host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()

    def execute(self, query, message="Query"):
        try:
            self.cur.execute(query)
            self.conn.commit()
            return (f"{message} executed sucessfully")
        except Exception as e:
            self.conn.rollback()
            return (f"{message} failed to execute: {e}")

    def fetchall(self):
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()

    def return_json(self, data):
        values = []
        for d in data:
            values += [d[0]]
        return values

    # Run a query
    def run_query(self, query):
        self.execute(query)
        return self.return_json(self.fetchall())

    # Create a schema
    def create_schema(self, schema_name):
        return self.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

    # Get all schemas
    def get_schemas(self):
        self.execute("SELECT schema_name FROM information_schema.schemata")
        return self.return_json(self.fetchall())
    
    # Delete a schema
    def delete_schema(self, schema_name):
        return self.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")

    # Create a table
    def create_table(self, table_name, schema_name, columns):
        return self.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns})")

    # Update a table
    def update_table(self, table_name, schema_name, columns):
        return self.execute(f"ALTER TABLE {schema_name}.{table_name} {columns}")

    # Get all tables
    def get_tables(self, schema_name):
        self.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'")
        return self.return_json(self.fetchall())
    
    # Delete a table
    def delete_table(self, table_name, schema_name):
        return self.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name} CASCADE")

    # Create a column
    def create_column(self, table_name, schema_name, column_name, column_type):
        return self.execute(f"ALTER TABLE {schema_name}.{table_name} ADD COLUMN {column_name} {column_type}")
    
    # Get all columns
    def get_columns(self, table_name, schema_name):
        self.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{schema_name}'")
        return self.return_json(self.fetchall())

    # Get a column
    def get_column(self, table_name, schema_name, column_name):
        self.execute(f"SELECT {column_name} FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    # Get numeric column names
    def get_numeric_columns(self, table_name, schema_name):
        self.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{schema_name}' AND data_type IN ('integer', 'smallint', 'bigint', 'decimal', 'numeric')")
        return self.return_json(self.fetchall())

    # Update a column
    def update_column(self, table_name, schema_name, column_name, column_type):
        return self.execute(f"ALTER TABLE {schema_name}.{table_name} ALTER COLUMN {column_name} {column_type}")
    
    # Delete a column
    def delete_column(self, table_name, schema_name, column_name):
        return self.execute(f"ALTER TABLE {schema_name}.{table_name} DROP COLUMN {column_name} CASCADE")
    
    # Insert a row
    def insert_row(self, table_name, schema_name, values):
        return self.execute(f"INSERT INTO {schema_name}.{table_name} VALUES ({values})")

    # Get all rows
    def get_rows(self, table_name, schema_name):
        self.execute(f"SELECT * FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    # Get a row
    def get_row(self, table_name, schema_name, condition):
        self.execute(f"SELECT * FROM {schema_name}.{table_name} WHERE {condition}")
        return self.return_json(self.fetchall())

    # Update a row
    def update_row(self, table_name, schema_name, condition, values):
        self.execute(f"UPDATE {schema_name}.{table_name} SET {values} WHERE {condition}")
        return (f"{table_name} table updated sucessfully")

    # Delete a row
    def delete_row(self, table_name, schema_name, condition):
        return self.execute(f"DELETE FROM {schema_name}.{table_name} WHERE {condition}")

    # Create a constraint
    def create_constraint(self, table_name, schema_name, constraint_name, constraint_type, columns):
        return self.execute(f"ALTER TABLE {schema_name}.{table_name} ADD CONSTRAINT {constraint_name} {constraint_type} ({columns})")
    
    # Get all constraints
    def get_constraints(self, table_name, schema_name):
        self.execute(f"SELECT constraint_name FROM information_schema.table_constraints WHERE table_name = '{table_name}' AND table_schema = '{schema_name}'")
        return self.return_json(self.fetchall())
    
    # Get a constraint
    def get_constraint(self, table_name, schema_name, constraint_name):
        self.execute(f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{table_name}' AND table_schema = '{schema_name}' AND constraint_name = '{constraint_name}'")
        return self.return_json(self.fetchall())
    
    # Update a constraint
    def update_constraint(self, table_name, schema_name, constraint_name, constraint_type, columns):
        return self.execute(f"ALTER TABLE {schema_name}.{table_name} ALTER CONSTRAINT {constraint_name} {constraint_type} ({columns})")

    # Delete a constraint
    def delete_constraint(self, table_name, schema_name, constraint_name):
        return self.execute(f"ALTER TABLE {schema_name}.{table_name} DROP CONSTRAINT {constraint_name} CASCADE")

    # Create a view
    def create_view(self, view_name, schema_name, query):
        return self.execute(f"CREATE VIEW {schema_name}.{view_name} AS {query}")
    
    # Get all views
    def get_views(self, schema_name):
        self.execute(f"SELECT table_name FROM information_schema.views WHERE table_schema = '{schema_name}'")
        return self.return_json(self.fetchall())

    # Get a view
    def get_view(self, schema_name, view_name):
        self.execute(f"SELECT * FROM {schema_name}.{view_name}")
        return self.return_json(self.fetchall())
    
    # Update a view
    def update_view(self, schema_name, view_name, query):
        return self.execute(f"ALTER VIEW {schema_name}.{view_name} AS {query}")
    
    # Delete a view
    def delete_view(self, schema_name, view_name):
        return self.execute(f"DROP VIEW {schema_name}.{view_name}")

    
