from typing import List, Optional
import logging
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from mappable.map import Mappable

logging.basicConfig(level=os.environ.get("LOG_LEVEL", default=logging.INFO))
logger = logging.getLogger("uvicorn")
numba_logger = logging.getLogger("numba")
numba_logger.setLevel(logging.WARNING)


STATIC_FILES_DIR = os.path.join(os.path.dirname(__file__), "static")


class Label(BaseModel):
    name: str
    light: str
    dark: str


class LabelFreq(BaseModel):
    name: str
    count: int


class DatasetInfo(BaseModel):
    name: str
    description: str
    created_at: str
    label_count: int
    labeled_percent: int
    count: str
    label_statistics: List[LabelFreq]
    columns: List[str]
    types: List[str]
    label_column: str
    default_view_id: Optional[str]
    searchable: bool


def setup_app(mappable_app: Mappable) -> FastAPI:
    app = FastAPI()

    origins = ["http://localhost:3000", "http://127.0.0.1:8000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    try:
        app.mount("/static", StaticFiles(directory=STATIC_FILES_DIR), name="static")
    except RuntimeError:
        print("No static files found! Only an API will be available.")

    @app.get("/")
    async def read_index():
        return FileResponse(f"{STATIC_FILES_DIR}/index.html")

    @app.get("/{dataset_id}/labels")
    def get_labels(dataset_id: str) -> List[Label]:
        return mappable_app.get(dataset_id).get_labels()

    @app.get("/{dataset_id}/info")
    def get_dataset_info(dataset_id: str) -> DatasetInfo:

        return mappable_app.get(dataset_id).info()

    @app.post("/{dataset_id}/labels/add")
    def add_label(dataset_id: str, label: Label) -> List[Label]:
        dataset = mappable_app.get(dataset_id)
        dataset.add_label(label.dict())
        return dataset.get_labels()

    @app.post("/{dataset_id}/labels/delete/{label}")
    def delete_label(dataset_id: str, label: str) -> List[Label]:
        dataset = mappable_app.get(dataset_id)
        dataset.delete_label(label)
        return dataset.get_labels()

    @app.get("/{dataset_id}/labels/check/{label}")
    def check_label(dataset_id: str, label: str) -> int:
        # TODO(Mark): Change once labels are counted automatically.
        return mappable_app.get(dataset_id).count_labels(label)

    @app.get("/{dataset_id}/search")
    async def search(dataset_id: str, q: str) -> List[int]:
        return mappable_app.get(dataset_id).search(q)

    @app.post("/{dataset_id}/annotate/{label}")
    def annotate(dataset_id: str, label: str, points: List[int]):
        dataset = mappable_app.get(dataset_id)
        dataset.add_annotations(points, label)
        return {"ok": True}

    @app.get("/{dataset_id}/view/{view_id}")
    def view(dataset_id: str, view_id: str):

        return mappable_app.get(dataset_id).get_points(view_id)

    @app.get("/{dataset_id}/views")
    def views(dataset_id: str) -> List[str]:
        return mappable_app.get(dataset_id).views()

    @app.get("/datasets")
    def dataset_info() -> List[str]:
        return mappable_app.info()

    @app.post("/{dataset_id}/{view_id}/recommend")
    def recommend(
        dataset_id: str,
        view_id: str,
        points: List[int],
        minSimilarity: float,
        percent: int,
        includeLabelled: bool,
        excludedPoints: List[int],
    ) -> List[int]:

        return mappable_app.get(dataset_id).recommend(
            view_id,
            points,
            minSimilarity,
            percent,
            includeLabelled,
            excludedPoints,
        )

    return app
