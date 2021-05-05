import sys

import psycopg2
from parsers.db_config import config


class DBConnection():

    connection = None

    @classmethod
    def connect(cls, filename, autocommit=True):
        """ Creates return new Singleton database connection """
        if cls.connection is None:
            params = config(filename)
            try:
                cls.connection = psycopg2.connect(**params)
                cls.connection.autocommit = autocommit
            except psycopg2.OperationalError as err:
                print(f"Unable to connect with db due to: {err}")
            else:
                print("Connected with success")
        return cls.connection

    @classmethod
    def execute_query(cls, query, fetch=False):
        """ Execute query on singleton db connection """
        result = None
        if cls.connection is not None:
            cursor = cls.connection.cursor()
        else:
            raise ValueError("DB Connection is not established!")

        try:
            cursor.execute(query)
            if fetch:
                result = cursor.fetchall()
            cursor.close()
        except Exception as err:
            cls.print_psycopg2_exception(err)
            cls.connection.rollback()
        return result

    @classmethod
    def load_from_file(cls, filename, table):
        """ Load table from file to db table """
        if cls.connection is not None:
            cursor = cls.connection.cursor()
        else:
            raise ValueError("DB Connection is not established!")
        with open(filename, 'r') as file_:
            next(file_)  # Skipping the headers
            try:
                cursor.copy_from(file_, table, sep=',', null='')
            except Exception as err:
                cls.print_psycopg2_exception(err)
                cls.connection.rollback()

    @staticmethod
    def print_psycopg2_exception(err):
        """ Print details about exception from db """
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno

        # print the connect() error
        print("\npsycopg2 ERROR:", err, "on line number:", line_num)
        print("psycopg2 traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        print("\nextensions.Diagnostics:", err.diag)

        # print the pgcode and pgerror exceptions
        print("pgerror:", err.pgerror)
        print("pgcode:", err.pgcode, "\n")
