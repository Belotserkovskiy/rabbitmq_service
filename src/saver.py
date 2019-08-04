import psycopg2
from psycopg2 import sql
from contextlib import closing
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DatabaseSaver:
    def __init__(self, connection):
        self.__host = connection['host']
        self.__user = connection['user']
        self.__password = connection['password']
        self.__dbname = connection['dbname']

    def validate(self, data):
        if len(data) != 3:
            return False
        for i in data.values():
            if not i or not isinstance(i, str):
                return False
        return True

    def push_to_database(self, data):
        if (self.validate(data)):
            return self.__push(data)
        raise Exception("""Wrong format to write in database!
                        Use {'name' : 'some name', 'email': 'some email', 'location' : 'some location'}""")

    def __push(self, data):
        with closing(psycopg2.connect(dbname=self.__dbname, user=self.__user,
                     password=self.__password, host=self.__host)) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO public.users3 ({fields[0]},{fields[1]},{fields[2]}) 
                               VALUES (%s,%s,%s) returning id;""".format(fields = list(data.keys())),
                               list(data.values()))
                return str(next(iter(cursor.fetchone())))

