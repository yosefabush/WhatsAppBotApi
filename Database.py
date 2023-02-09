import os

import MySQLdb


class Database(object):
    connection = None
    cursor = None

    def __init__(self):
        if self.connection is None:
            try:
                print("Create new connection!")
                self.connection = MySQLdb.connect(host=os.environ['host'],
                                                  user=os.environ['user'],
                                                  password=os.environ['password'],
                                                  database=os.environ['database'])
                self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
                self.connection.autocommit(True)
            except Exception as error:
                print("Error: Connection not established {}".format(error))
            else:
                print("Connection established")

    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for i in result:
            print(i)
        return result

    def insert_data(self, sql):
        # Preparing SQL query to INSERT a record into the database.
        # Preparing SQL query to INSERT a record into the database.
        insert_stmt = (
            "INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)"
            "VALUES (%s, %s, %s, %s, %s)"
        )
        data = [('Ramya', 'Ramapriya', 25, 'F', 5000), ('Ramya', 'Ramapriya', 25, 'F', 5000)]

        sql = """INSERT INTO EMPLOYEE(
           FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)
           VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

        try:
            # multiple
            # for d in data:
            #     self.cursor.execute(insert_stmt, d)
            #     self.connection.commit()

            # Executing the SQL command
            self.cursor.execute(sql)

            # Commit your changes in the database
            self.connection.commit()

        except Exception as EX:
            print(EX)
            # Rolling back in case of error
            self.connection.rollback()
