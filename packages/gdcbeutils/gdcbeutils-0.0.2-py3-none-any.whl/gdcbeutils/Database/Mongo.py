import contextlib
import urllib.parse
from os import environ, getenv
from typing import Any, Dict

from pydantic import BaseModel
from pymongo import MongoClient


class MongoDbException(Exception):
    pass


class DocumentNotFoundException(MongoDbException):
    pass


class DuplicateDocumentFoundException(MongoDbException):
    key: str

    def __init__(self, message: str, key: str, *args: object) -> None:
        self.key = key
        super().__init__(message, *args)


class MongoConnectParams(BaseModel):
    user: str
    password: str
    host: str
    port: str


class MongoConnectionHelper:
    prefix: str | None
    database: str
    collection: str

    def __init__(
        self,
        database: str,
        collection: str,
    ) -> None:
        self.database = database
        self.collection = collection

    def db_params_from_env_file(self) -> MongoConnectParams:
        """
        This method gets the credentials from an environment file. Note that a KeyError Exception will be raised if environment variables are not present on the format:
        - MONGO_USER
        - MONGO_PASSWORD
        - MONGO_HOST
        - MONGO_PORT
        """

        return MongoConnectParams(
            user=environ["MONGO_USER"],
            password=environ["MONGO_PASSWORD"],
            host=environ["MONGO_HOST"],
            port=environ["MONGO_PORT"],
        )

    def build_conn_string(self, credentials: MongoConnectParams) -> str:
        username = urllib.parse.quote_plus(credentials.user)
        password = urllib.parse.quote_plus(credentials.password)

        conn_string = (
            f"mongodb://{username}:{password}@{credentials.host}:{credentials.port}"
        )

        if getenv("MONGO_USE_SRV", "") == "True":
            conn_string = f"mongodb+srv://{username}:{password}@{credentials.host}"

        return conn_string

    def connect(self) -> MongoClient:
        """
        Estabilished a new connection to the database and returns the instance to that connection.
        Credentials should follow the format: MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT
        """

        credentials = self.db_params_from_env_file()
        conn_string = self.build_conn_string(credentials=credentials)
        client = MongoClient(conn_string)

        return client

    @contextlib.contextmanager
    def perform_operation(self):
        client = self.connect()

        try:
            db = client[self.database]
            collection = db[self.collection]

            yield collection

        finally:
            client.close()


class BaseMongoDbHelper(MongoConnectionHelper):
    def __init__(self, collection: str) -> None:
        super().__init__(environ["MONGO_DB"], collection)

    def __insert_single_document__(self, document: Dict[str, Any]):
        with self.perform_operation() as cursor:
            cursor.insert_one(document)
