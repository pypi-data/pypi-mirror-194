"""influxlog - """
from pathlib import Path

import influxdb_client
import yaml
from influxdb_client.client.write_api import SYNCHRONOUS

__version__ = '0.1.0'
__author__ = 'fx-kirin <fx.kirin@gmail.com>'
__all__: list = []


def _load():
    global write_api, influx_db
    yaml_path_text = "~/.config/influxdb.yml"
    yaml_path = Path(yaml_path_text).expanduser()
    if not yaml_path.exists():
        raise FileNotFoundError(f"You must store influxdb yaml path to {yaml_path_text}")
    yaml_text = yaml_path.read_text()
    influx_db = yaml.safe_load(yaml_text)

    client = influxdb_client.InfluxDBClient(
        url=influx_db["url"],
        token=influx_db["token"],
        org=influx_db["org"]
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)


def record(measurement, fields, tags=None, time_v=None):
    point_dict = {"measurement": measurement, "fields": fields}
    if tags is not None:
        point_dict["tags"] = tags
    if time_v is not None:
        point_dict["time"] = time_v
    p = influxdb_client.Point.from_dict(point_dict)
    write_api.write(bucket=influx_db["bucket"], org=influx_db["org"], record=p)


_load()
