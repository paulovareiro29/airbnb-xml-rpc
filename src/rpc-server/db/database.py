import psycopg2

''' conn = None
cursor = None
 '''


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.user = "is"
        self.password = "is"
        self.host = "localhost"
        self.port = "5432"
        self.database = "is"

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             port=self.port,
                                             database=self.database)
            except psycopg2.DatabaseError as e:
                raise e

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def insert(self, sql, values):
        with self.conn.cursor() as cursor:
            cursor.execute(query=sql, vars=values)
            self.conn.commit()
            cursor.close()
            return True

    def selectAll(self, query):
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            result = [row for row in cursor.fetchall()]
            cursor.close()
            return result

    def selectOne(self, query):
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result


''' 
try:
    conn = psycopg2.connect(user="is",
                                  password="is",
                                  host="localhost",
                                  port="5432",
                                  database="is")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")

    print("Teachers list:")
    for teacher in cursor:
        print(f" > {teacher[0]}, from {teacher[1]}")

except (Exception, psycopg2.Error) as error:
    print("Failed to fetch data", error)

finally:
    if conn:
        cursor.close()
        conn.close()
 '''
