from sqlalchemy import create_engine, text


class Connection:
    def __init__(self, host, user, password, database, port=5432):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def execute(self, query, values=None):
        try:
            engine_str = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"  # changed engine string
            engine = create_engine(engine_str)

            with engine.connect() as connection:
                result = connection.execute(text(query), values)

                if result.returns_rows:
                    return [dict(row) for row in result.mappings()]
                else:
                    connection.commit()
                    return None

        except Exception as e:
            print(f"Error executing PostgreSQL query: {e}")  # changed error message
            return None


if __name__ == "__main__":
    host = "your_postgres_host"  # e.g., "localhost"
    user = "your_postgres_user"
    password = "your_postgres_password"
    database = "your_postgres_database"
    port = 5432  # or the port your postgres is running on.

    connection = Connection(host, user, password, database, port)  # added port

    query = ""
    connection.execute(query)

    results = connection.execute(query)

    if results:
        for row in results:
            print(row)
    else:
        print("No results found or an error occurred.")
