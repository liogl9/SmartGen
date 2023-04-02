import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import os

# Establecemos parámetros de acceso al contenedor
bucket = "timeSeries"
org = "TeamSocket"
token = "EbfvN-ykoux3uY8FKXN95dbamkNA39tLAnGtEse4Vuk62tcK0rv0-AQzWfHQkdFepQCD2nrwDP46uO7KRpEE3Q=="
# Store the URL of your InfluxDB instance
url = "http://172.18.0.2:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
# write_api = client.write_api(write_options=SYNCHRONOUS)

# p = influxdb_client.Point("ConsumoAgua").tag(
#     "location", "Salamanca").field("m3", 8)
# write_api.write(bucket=bucket, org=org, record=p)

with client as client:
    i = 0
    for df in pd.read_csv(os.path.join(os.getcwd(), "waterpred", "ConsumoAgua.csv"), chunksize=1, index_col=False):
        with client.write_api(write_options=SYNCHRONOUS) as write_api:
            try:
                p = influxdb_client.Point("ConsumoAgua").tag(
                    "location", df["location"][i]).field("m3", int(df["m3"])).time(int(df["timeStamp"]), write_precision=influxdb_client.WritePrecision.MS)
                write_api.write(bucket=bucket, org=org, record=p)
                i += 1
            except influxdb_client.InfluxDBError as e:
                print(e)
