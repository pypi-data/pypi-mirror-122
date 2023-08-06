import unittest
import pandas
import tempfile
from mappable.server import setup_app
from mappable.map import Mappable, MappableDataset

from fastapi.testclient import TestClient


class TestApp(unittest.TestCase):
    def setUp(self):

        self.data = pandas.read_csv("test/fixtures/data.tsv", sep="\t")
        self.out_file = tempfile.mkdtemp()
        mappable_app = Mappable(self.out_file)

        app = setup_app(mappable_app)

        self.client = TestClient(app)

    def test_labels(self):
        r = self.client.get("/labels")
        assert {x["name"] for x in r.json()} == {
            "conspiratorial",
            "Non-conspiratorial",
            "None",
        }

        # Delete a label
        self.client.post("/labels/delete/conspiratorial")
        r = self.client.get("/labels")
        assert {x["name"] for x in r.json()} == {"Non-conspiratorial", "None"}

        # Add a label
        self.client.post(
            "/labels/add",
            json={"name": "conspiratorial", "light": "white", "dark": "black"},
        )
        r = self.client.get("/labels")
        assert {x["name"] for x in r.json()} == {
            "conspiratorial",
            "Non-conspiratorial",
            "None",
        }

    def test_annotation(self):

        r = self.client.post("/annotate/None", json=[0, 1, 2, 3])
        metadata = r.json()["metadata"]

        labels = {d["label"] for d in metadata[:4]}
        assert labels == {None}
