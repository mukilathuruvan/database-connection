import psycopg2


class PostgresConnection:
    def __init__(self, host, user, password, database, port=5432):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            return True
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return False

    def execute(self, query, values=None):
        if self.connection is None:
            print("Connection not established.")
            return None

        try:
            with self.connection.cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)

                if cursor.description:
                    results = cursor.fetchall()
                    self.connection.commit()
                    return results
                else:
                    self.connection.commit()
                    return None

        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None


if __name__ == "__main__":
    host = "your_postgres_host"
    user = "your_postgres_user"
    password = "your_postgres_password"
    database = "your_postgres_database"
    port = 5432

    db = PostgresConnection(host, user, password, database, port)

    if db.connect():
        select_query = "SELECT * FROM example_table"
        results = db.execute(select_query)

        if results:
            for row in results:
                print(row)
        else:
            print("No results found or an error occurred.")

    else:
        print("Failed to connect to the database.")
