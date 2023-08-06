import contextlib
import logging
from os import environ
from typing import cast

from mysql.connector import MySQLConnection
from mysql.connector import connect as db_connect
from pydantic import BaseModel

logger = logging.getLogger("MySql Global Helper")


class DbHandlerException(Exception):
    pass


class MySqlConnectParams(BaseModel):
    user: str
    password: str
    host: str
    port: str


class SqlConnector:
    def db_params_from_env_file(self) -> MySqlConnectParams:
        """
        This method gets the credentials from an environment file. Note that a KeyError Exception will be raised if environment variables are not present on the format:
        - MYSQL_USER
        - MYSQL_PASSWORD
        - MYSQL_HOST
        - MYSQL_PORT
        """
        try:
            return MySqlConnectParams(
                user=environ["MYSQL_USER"],
                password=environ["MYSQL_PASSWORD"],
                host=environ["MYSQL_HOST"],
                port=environ["MYSQL_PORT"],
            )

        except Exception as e:
            logger.error("Could not find ENV variables to connect")
            raise e

    def connect(self) -> MySQLConnection:
        """
        Estabilished a new connection to the database and returns the instance to that connection.
        Credentials should follow the format: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT
        """

        credentials = self.db_params_from_env_file()
        conn = db_connect(**credentials.dict())

        return cast(MySQLConnection, conn)

    @contextlib.contextmanager
    def perform_statement(self):
        try:
            # Open new connection and cursor for operations
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)

            yield cursor
        finally:
            # Now close them!
            cursor.close()
            conn.close()

    @contextlib.contextmanager
    def perform_operation(self):
        try:
            # Open new connection and cursor for operations
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)

            yield cursor

            conn.commit()
        finally:
            # Now close them!
            cursor.close()
            conn.close()


class SqlHelper(SqlConnector):
    database: str

    def __init__(self, db_name: str | None = None) -> None:
        self.database = db_name or environ["MYSQL_DB"]
        super().__init__()

    # def assemble_insert_query(self, table_name: str, value_names: List[str]) -> str:
    #     base_insert_query = """
    #         INSERT INTO {} (
    #             {}
    #         ) VALUES( {} )
    #     """

    #     formatted_query = base_insert_query.format(
    #         table_name, ",".join(value_names), ",".join(["%s"] * len(value_names))
    #     )
    #     return formatted_query

    # def assemble_insert_params(
    #     self, value_names: List[str], value_mapping: Dict[str, any]
    # ) -> List[any]:
    #     values_list = [value_mapping[value] for value in value_names]
    #     return values_list

    # def assemble_update_query(self, table_name: str, value_names: List[str]) -> str:
    #     base_update_query = """
    #         UPDATE {}
    #         SET {}
    #         WHERE id={}
    #     """

    #     formatted_values = [f"{key}=%s" for key in value_names]
    #     formatted_query = base_update_query.format(
    #         table_name,
    #         ",".join(formatted_values),
    #         "%s",
    #     )
    #     return formatted_query

    # def assemble_update_params(
    #     self,
    #     value_names: List[str],
    #     value_mapping: Dict[str, Any],
    # ):
    #     sql_params = [value_mapping[key] for key in value_names]
    #     return sql_params


class MySqlRuntimeException(Exception):
    pass
