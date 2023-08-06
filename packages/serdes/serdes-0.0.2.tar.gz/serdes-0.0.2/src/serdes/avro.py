import io
from typing import List, Union

import fastavro
import pyarrow as pa
from dataclasses_avroschema.avrodantic import AvroBaseModel


# io
def _io(filepath_or_buffer: Union[str, bytes], mode: str):
    if isinstance(filepath_or_buffer, (io.BytesIO, io.BufferedIOBase)):
        filepath_or_buffer.seek(0)
        return filepath_or_buffer
    if isinstance(filepath_or_buffer, bytes):
        return io.BytesIO(filepath_or_buffer)
    return open(filepath_or_buffer, mode)


# reader
def _reader(filepath_or_buffer: Union[str, bytes]):
    return _io(filepath_or_buffer=filepath_or_buffer, mode="rb")


# serialize
def serialize(*record: AvroBaseModel, schema: dict = None) -> bytes:
    if not schema:
        sample = record[0]
        if not isinstance(sample, AvroBaseModel):
            _msg = "You need schema if record is not a instance of AvroBaseModel."
            raise KeyError(_msg)
        schema = sample.avro_schema_to_python()
    schema = fastavro.parse_schema(sample.avro_schema_to_python())
    fo = io.BytesIO()
    fastavro.writer(fo, schema, [x.asdict() for x in record])
    fo.seek(0)
    return fo.read()


# deserialzie
def deserialize(buffer: bytes) -> List[dict]:
    reader = fastavro.reader(io.BytesIO(buffer))
    return [record for record in reader]


# read
def read(filepath_or_buffer: Union[str, bytes]):
    fo = _reader(filepath_or_buffer)
    records = [record for record in fastavro.reader(fo)]
    fo.close()
    return records


# to arrow table
def to_arrow_table(filepath_or_buffer: Union[str, bytes]):
    fo = _reader(filepath_or_buffer)
    return pa.Table.from_pylist([row for row in fastavro.reader(fo)])


# to pandas dataframe
def to_pandas(buffer: bytes):
    return to_arrow_table(buffer).to_pandas()
