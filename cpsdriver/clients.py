import logging
import json
from os import path

from pymongo import MongoClient
import requests
from sh import mongorestore

from cpsdriver.codec import DocObjectCodec


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class CpsMongoClient:
    """Abstracts the MongoDB used for storing local test cases"""

    EXCLUDED_DBS = {"admin", "config", "local"}

    def __init__(self, uri):
        """Instantiate the client

        Args:
            uri (str): The mongodb uri.
        """
        self.uri = uri
        self.client = MongoClient(self.uri)
        self.open_cursors = {}

    def __del__(self):
        for cursor in self.open_cursors.items():
            cursor.close()

    def find(self, db_name, collection, filt):
        """Returns a cursor for the find on the db and collection"""
        return self.client[db_name][collection].find(filt)

    def aggregate(self, db_name, collection, pipeline):
        """Returns a cursor for the pipeline on the db and collection"""
        return self.client[db_name][collection].aggregate(
            pipeline, allowDiskUse=True
        )

    def list_products(self, db_name):
        """Lists all products"""
        collection = "products"
        cursor = self.find(db_name, collection, {})
        return [DocObjectCodec.decode(doc, collection) for doc in cursor]

    def find_product_by_id(self, db_name, product_id):
        """Find a product with a specific ID"""
        collection = "products"
        filt = {
            "product_id.barcode_type": product_id.barcode_type,
            "product_id.id": product_id.barcode,
        }
        cursor = self.find(db_name, collection, filt)
        return [DocObjectCodec.decode(doc, collection) for doc in cursor]

    def find_product_facings(self, db_name, product_id):
        """Find all facings of a specific product ID"""
        collection = "planogram"
        filt = {
            "planogram_product_id.barcode_type": product_id.barcode_type,
            "planogram_product_id.id": product_id.barcode,
        }
        cursor = self.find(db_name, collection, filt)
        return [DocObjectCodec.decode(doc, collection) for doc in cursor]

    def find_first_after_time(self, db_name, collection, timestamp):
        """Find the next item in time after the given timestamp"""
        filt = {"$and": self.after("timestamp", timestamp)}
        pipeline = [
            {
                "$match": filt
            },
            {
                "$sort": {"timestamp": 1}
            },
            {
                "$limit": 1
            }
        ]
        cursor = self.aggregate(db_name, collection, pipeline)
        return [DocObjectCodec.decode(doc, collection) for doc in cursor]

    def find_all_between_time(
        self, db_name, collection, timestamp_low, timestamp_high
    ):
        """Find all items in time between the given timestamps"""
        filt = {"$and": self.between(
            "timestamp", timestamp_low, timestamp_high
        )}
        cursor = self.find(db_name, collection, filt)
        return [DocObjectCodec.decode(doc, collection) for doc in cursor]

    @staticmethod
    def between(ts_field_name, low, high):
        """Small helper snippet for finding between a given fieldname"""
        return [{ts_field_name: {"$gt": low}}, {ts_field_name: {"$lt": high}}]

    @staticmethod
    def after(ts_field_name, low):
        """Small helper snippet for finding greater than a given fieldname"""
        return [{ts_field_name: {"$gt": low}}]

    @property
    def test_cases(self):
        """Returns the set of locally loaded test cases"""
        return set(self.client.list_database_names()).difference(
            self.EXCLUDED_DBS
        )

    def available_collections(self, db_name):
        """Returns list of all collections in the given db"""
        return self.client[db_name].list_collection_names()

    def load_archive(self, filepath):
        """Loads an archive into the DB"""
        return mongorestore(uri=self.uri, archive=filepath)


class CpsApiClient:
    """Interfaces with the Cps API
        The interface http://aifi.io/cpsweek/api/v1
        will be enabled in 03/01/2020.
        Before that it will return a "404 Page Not Found"
    """
    def __init__(
        self,
        base_url="http://aifi.io/cpsweek/api/v1",
        download_dir=path.join("data", "downloads"),
        token="",
    ):
        """Instantiates the CPS Week API client

        Args:
            url (str): Base url for the api.
            archive_dir (path): Directory to store archives in.
            token (str): API access token.
        """
        self.base_url = base_url
        self.download_dir = download_dir
        self.headers = {"TOKEN": token}

    # Behaviors
    def download_archive(self, id_=None, name=None):
        """Downloads a test case archive file"""
        raise NotImplementedError

    # Test Case Operations
    def list_test_cases(self):
        """Returns a list of test case metadata"""
        return self._get(url=f"{self.base_url}/testcases")

    def create_test_case(self, name, archive_url):
        """Returns test case metadata"""
        return self._post(
            url=f"{self.base_url}/testcases",
            json=json.dumps({"name": name, "archive": archive_url}),
        )

    def get_test_case(self, id_="", name=""):
        """Returns test case metadata"""
        if name:
            name = f"?name={name}"
        return self._get(url=f"{self.base_url}/testcases/{id_}{name}")

    def delete_test_case(self, id_):
        """Deletes a test case"""
        return self._delete(url=f"{self.base_url}/testcases/{id_}")

    # Result Operations
    def list_results(self, latest_only=True):
        """Lists results belonging to this user"""
        return self._get(
            url=f"{self.base_url}/results?latest_only={latest_only}"
        )

    def create_result(self, name, receipts):
        """Submits the results for the given test case"""
        return self._post(
            url=f"{self.base_url}/results",
            json=json.dumps({"name": name, "receipts": receipts}),
        )

    def get_result(self, id_=None):
        """Gets the result with the given id"""
        return self._get(url=f"{self.base_url}/results/{id_}")

    def delete_result(self, id_=None):
        """Deletes a result"""
        return self._delete(url=f"{self.base_url}/results/{id_}")

    # Request Wrappers
    def _get(self, *args, **kwargs):
        """Returns json of the given request"""
        headers = kwargs.get("headers", {})
        headers.update(self.headers)
        kwargs["headers"] = headers
        return requests.get(*args, **kwargs).json()

    def _post(self, *args, **kwargs):
        """Returns json of the given request"""
        headers = kwargs.get("headers", {})
        headers.update(self.headers)
        kwargs["headers"] = headers
        return requests.post(*args, **kwargs).json()

    def _delete(self, *args, **kwargs):
        """Returns json of the given request"""
        headers = kwargs.get("headers", {})
        headers.update(self.headers)
        kwargs["headers"] = headers
        return requests.delete(*args, **kwargs).json()


class TestCaseClient:
    """Abstracts the Mongo and API client to loads test cases"""

    def __init__(self, cps_mongo_client, cps_api_client=None):
        """Instantiate a TestCaseClient

        Args:
            cps_mongo_client (CpsMongoClient): MongoClient to use.
            cps_api_client (CpsApiClient): ApiClient to use.
        """
        self.cps_mongo_client = cps_mongo_client
        self.cps_api_client = cps_api_client
        self.context = "cps-test-01"

    def set_context(self, test_case_name, load=True):
        """Sets the context of the client to the given test case"""
        if load:
            self.load(test_case_name)
        if test_case_name not in self.cps_mongo_client.test_cases:
            raise LookupError(f"Test case {test_case_name} not found.")
        self.context = test_case_name

    def load(self, name):
        """Loads the given testcase name into the local db"""
        if name in self.cps_mongo_client.test_cases:
            logger.info(f"Test case {name} is already loaded. Skipping it.")
            return
        archive = path.join(
            self.cps_api_client.download_dir, f"{name}.archive"
        )
        try:
            return self.cps_mongo_client.load_archive(archive)
        except FileNotFoundError:
            logger.debug(f"Test case {name} is not found. Downloading...")
        self.cps_api_client.download_archive(name)
        logger.debug(f"Test case {name} downloaded.")
        return self.cps_mongo_client.load_archive(archive)

    @property
    def valid_data_types(self):
        return self.cps_mongo_client.available_collections(self.context)

    @property
    def available_test_cases(self):
        return self.cps_mongo_client.test_cases

    def list_products(self):
        """Lists all products"""
        return self.cps_mongo_client.list_products(self.context)

    def find_product_by_id(self, product_id):
        """Find a product with a specific ID"""
        return self.cps_mongo_client.list_products(self.context, product_id)

    def find_product_facings(self, product_id):
        """Find all facings of a specific product ID"""
        return self.cps_mongo_client.find_product_facings(
            self.context, product_id
        )

    def find_first_after_time(self, data_type, timestamp):
        """Find the next item in time after the given timestamp"""
        if data_type not in self.cps_mongo_client.available_collections(
            self.context
        ):
            logger.error(
                f"Unknown data type {data_type} for case {self.context}"
            )
            return None
        return self.cps_mongo_client.find_first_after_time(
                self.context, data_type, timestamp
        )

    def find_all_between_time(self, data_type, timestamp_low, timestamp_high):
        if data_type not in self.cps_mongo_client.available_collections(
            self.context
        ):
            logger.error(
                f"Unknown data type {data_type} for case {self.context}"
            )
            return None
        return self.cps_mongo_client.find_all_between_time(
                self.context, data_type, timestamp_low, timestamp_high
        )
