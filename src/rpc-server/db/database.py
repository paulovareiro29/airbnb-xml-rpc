import psycopg2

''' connection = None
cursor = None
 '''


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.user = "is"
        self.password = "is"
        self.host = "localhost"
        self.port = "5432"
        self.database = "is"

    def connect(self):
        self.connection = psycopg2.connect(user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           port=self.port,
                                           database=self.database)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def insert(self, sql, values):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query=sql, vars=values)
            return cursor

        except (Exception, psycopg2.Error) as error:
            return Exception(error)

    def select(self, sql):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor

        except (Exception, psycopg2.Error) as error:
            return Exception(error)


''' 
try:
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="localhost",
                                  port="5432",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teachers")

    print("Teachers list:")
    for teacher in cursor:
        print(f" > {teacher[0]}, from {teacher[1]}")

except (Exception, psycopg2.Error) as error:
    print("Failed to fetch data", error)

finally:
    if connection:
        cursor.close()
        connection.close()
 '''
