from sqlalchemy import create_engine, text


class Connection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def execute_sql_alchemy(host, user, password, database, query, values=None):
        try:
            engine_str = f"mysql+pymysql://{user}:{password}@{host}/{database}"
            engine = create_engine(engine_str)

            with engine.connect() as connection:
                result = connection.execute(text(query), values)

                if result.returns_rows:
                    return [dict(row) for row in result.mappings()]
                else:
                    connection.commit()
                    return None

        except Exception as e:
            print(f"Error executing SQLAlchemy query: {e}")
            return None


if __name__ == "__main__":
    host = "your_host"
    user = "your_user"
    password = "your_password"
    database = "your_database"

    connection = Connection(host, user, password, database)

    query = ""
    results = execute_sql_alchemy(host, user, password, database, query)

    if results:
        for row in results:
            print(row)
    else:
        print("No results found or an error occurred.")
