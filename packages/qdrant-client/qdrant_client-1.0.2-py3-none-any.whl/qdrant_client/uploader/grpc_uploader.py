from itertools import count
from typing import Iterable, Any, Union, Tuple, Optional, Generator

from qdrant_client import grpc as grpc
from qdrant_client.connection import get_channel
from qdrant_client.conversions.conversion import payload_to_grpc, RestToGrpc
from qdrant_client.grpc import PointsStub, PointStruct, PointId
from qdrant_client.http.models import Batch
from qdrant_client.uploader.uploader import BaseUploader


def upload_batch_grpc(points_client: PointsStub, collection_name: str, batch: Union[Batch, Tuple]) -> bool:
    ids_batch, vectors_batch, payload_batch = batch
    if payload_batch is None:
        payload_batch = (None for _ in count())

    points = [
        PointStruct(
            id=RestToGrpc.convert_extended_point_id(idx) if not isinstance(idx, PointId) else idx,
            vectors=RestToGrpc.convert_vector_struct(vector),
            payload=payload_to_grpc(payload or {}),
        ) for idx, vector, payload in zip(ids_batch, vectors_batch, payload_batch)
    ]
    points_client.Upsert(grpc.UpsertPoints(collection_name=collection_name, points=points))
    return True


class GrpcBatchUploader(BaseUploader):

    def __init__(self, host: str, port: int, collection_name: str, **kwargs: Any):
        self.collection_name = collection_name
        self._host = host
        self._port = port
        self._kwargs = kwargs

    @classmethod
    def start(cls, collection_name: Optional[str] = None, host: str ="localhost", port: int = 6334, **kwargs: Any) -> 'GrpcBatchUploader':
        if not collection_name:
            raise RuntimeError("Collection name could not be empty")

        return cls(host=host, port=port, collection_name=collection_name, **kwargs)

    def process_upload(self, items: Iterable[Any]) -> Generator[bool, None, None]:
        channel = get_channel(
            host=self._host,
            port=self._port,
            **self._kwargs
        )
        points_client = PointsStub(channel)
        for batch in items:
            yield upload_batch_grpc(points_client, self.collection_name, batch)

    def process(self, items: Iterable[Any]) -> Generator[bool, None, None]:
        yield from self.process_upload(items)
