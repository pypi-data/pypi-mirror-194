import os

import azure.functions as func
import pandas as pd

from warpzone.servicebus.data.client import DataMessage, WarpzoneDataClient
from warpzone.servicebus.events.client import EventMessage, WarpzoneEventClient


def get_data_client() -> WarpzoneDataClient:
    return WarpzoneDataClient.from_connection_strings(
        service_bus_conn_str=os.environ["SERVICE_BUS_CONNECTION_STRING"],
        storage_account_conn_str=os.environ["DATA_STORAGE_ACCOUNT_CONNECTION_STRING"],
    )


def get_event_client() -> WarpzoneEventClient:
    return WarpzoneEventClient.from_connection_string(
        conn_str=os.environ["SERVICE_BUS_CONNECTION_STRING"],
    )


def func_msg_to_event(msg: func.ServiceBusMessage) -> EventMessage:
    event_msg = EventMessage.from_func_msg(msg)
    return event_msg


def func_msg_to_data(msg: func.ServiceBusMessage) -> DataMessage:
    data_client = get_data_client()
    event_msg = func_msg_to_event(msg)
    data_msg = data_client.event_to_data(event_msg)
    return data_msg


def func_msg_to_pandas(msg: func.ServiceBusMessage) -> pd.DataFrame:
    data_msg = func_msg_to_data(msg)
    return data_msg.to_pandas()


def send_event(event_msg: EventMessage, topic_name: str) -> None:
    event_client = get_event_client()
    event_client.send(
        topic_name=topic_name,
        event_msg=event_msg,
    )


def send_data(data_msg: DataMessage, topic_name: str) -> None:
    data_client = get_data_client()
    data_client.send(
        topic_name=topic_name,
        data_msg=data_msg,
    )


def send_pandas(
    df: pd.DataFrame, topic_name: str, subject: str, schema: dict = None
) -> None:
    data_msg = DataMessage.from_pandas(df, subject, schema=schema)
    send_data(data_msg, topic_name)
