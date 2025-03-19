import mysql.connector


class MySQLDatabase:

    def __init__(self, host="localhost", user="", password="", database=""):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        try:
            if self.database:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
            else:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                )
            print("Connection to MySQL successful!")
            return True

        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            return False

    def execute_query(self, query, values=None):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
            return None

        cursor = self.connection.cursor()
        try:
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

        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def close(self):
        """
        Closes the MySQL connection.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")
            self.connection = None  # Reset connection attribute


# Example usage:
if __name__ == "__main__":
    # Create an instance of MySQLDatabase
    db = MySQLDatabase(host="localhost", user="root", password="", database="")
    db.execute_query("SELECT * FROM users")
