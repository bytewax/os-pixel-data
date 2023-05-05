import json
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Optional

from pandas import DataFrame
from pyarrow import parquet, Table

from bytewax.dataflow import Dataflow
from bytewax.connectors.kafka import KafkaInput
from bytewax.connectors.stdio import StdOutput
from bytewax.outputs import PartitionedOutput, StatefulSink
from bytewax.window import EventClockConfig, TumblingWindow


flow = Dataflow()
flow.input(
    "events", 
    KafkaInput(
        brokers=["localhost:9092"], 
        topics=["events"],
        tail = False
        )
    )

# flow.inspect(print)

class Event(BaseModel):
    id: str
    group_key: str
    year: Optional[str]
    month: Optional[str]
    day: Optional[str]
    ts: datetime
    page: str
    msg: str
    location: str
    subject: str


def deserialize(key_bytes__payload_bytes):
    key_bytes, payload_bytes = key_bytes__payload_bytes
    key = key_bytes.decode()
    payload = json.loads(payload_bytes) if payload_bytes else None
    event = Event(
        id=payload['uuid'],
        group_key=key,
        ts=datetime.strptime(payload['buzTimestamp'][:-2] + 'Z', "%Y-%m-%dT%H:%M:%S.%fZ"),
        page=payload['payload']['page'],
        msg=payload['payload']['msg'],
        location=payload['payload']['location'],
        subject=payload['payload']['subject']
    )
    return event

flow.map(deserialize)
# id=UUID('0047fb7f-4739-47ea-8e3a-5d256f1a1ceb') group_key='buz.pixel.pageView' ts=datetime.datetime(2023, 5, 5, 17, 27, 28, 563309) page='os-pixel-data' msg='hello' location='buzwax' subject='world'

def add_date_columns(event):
    event.year = event.ts.year
    event.month = event.ts.month
    event.day = event.ts.day
    return event

flow.map(add_date_columns)
# id=UUID('0047fb7f-4739-47ea-8e3a-5d256f1a1ceb') group_key='buz.pixel.pageView' partition_by=[2023, 5, 5] ts=datetime.datetime(2023, 5, 5, 17, 27, 28, 563309) page='os-pixel-data' msg='hello' location='buzwax' subject='world'

# group by page
flow.map(lambda x: (x.group_key, x))

# This is the accumulator function, and outputs a list of event objects
def acc_values(acc, event):
    acc.append(event.dict())
    return acc

# This function instructs the event clock on how to retrieve the
# event's datetime from the input.
def get_event_time(event):
    return event.ts.replace(tzinfo=timezone.utc)

# Configure the `fold_window` operator to use the event time.
cc = EventClockConfig(get_event_time, wait_for_system_duration=timedelta(seconds=10))

# And a 5 seconds tumbling window
align_to = datetime(2023, 5, 5, tzinfo=timezone.utc)
wc = TumblingWindow(align_to=align_to, length=timedelta(minutes=10))

flow.fold_window("acc_values", cc, wc, list, acc_values)

flow.inspect(print)

flow.map(lambda x: (x[0], DataFrame(x[1])))

flow.inspect(print)

class ParquetSink(StatefulSink):
    def write(self, value):
        table = Table.from_pandas(value)
        parquet.write_to_dataset(
            table,
            root_path="parquet_demo_out",
            partition_cols=["year", "month", "day", "group_key"],
        )

    def snapshot(self):
        pass

    def close(self):
        pass


class ParquetOutput(PartitionedOutput):
    def list_parts(self):
        return {"singleton"}

    def assign_part(self, item_key):
        return "singleton"

    def build_part(self, for_part, resume_state):
        return ParquetSink()

flow.output("out", ParquetOutput())