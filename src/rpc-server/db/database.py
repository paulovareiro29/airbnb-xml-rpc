import psycopg2

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
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query=sql, vars=values)
                self.conn.commit()
                cursor.close()
                return True
        except psycopg2.Error as ex:
            raise ex

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
