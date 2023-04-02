import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "timeSeries"
org = "TeamSocket"
token = "Wg4DmUNeNTPwPZXTeiY3oE39gD-1S4WcOhYAW3UhGK7J3zoQ2RzeV3b_HGA366ykCJDTU7Eu6eULb1m4n44kKA=="
# Store the URL of your InfluxDB instance
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)


def query_data(bucket, time_range, measure, location, field):
    query_api = client.query_api()
    query = 'from(bucket:"{}")\
    |> range(start: -{})\
    |> filter(fn: (r)=> r._measurement == "{}")\
    |> filter(fn: (r)=> r.location == "{}")\
    |> filter(fn: (r)=> r._field == "{}")'.format(bucket, time_range, measure, location, field)
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time().strftime(
                "%m/%d/%Y, %H:%M:%S"), record.get_value()))

    return results


if __name__ == "__main__":
    # Query script
    # query_api = client.query_api()
    # query = 'from(bucket:"timeSeries")\
    # |> range(start: -6h)\
    # |> filter(fn:(r) => r._measurement == "ConsumoAgua")\
    # |> filter(fn:(r) => r.location == "Caceres")\
    # |> filter(fn:(r) => r._field == "m3")'
    # result = query_api.query(org=org, query=query)
    # results = []
    # for table in result:
    #     for record in table.records:
    #         results.append((record.get_time(), record.get_value()))

    # print(results)

    print(query_data("timeSeries", "6h", "ConsumoAgua", "Caceres", "m3"))
