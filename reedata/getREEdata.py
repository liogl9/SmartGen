import requests
import random
import json


def get_ree_data():
    while True:
        with open('./gen_dem/command.txt', 'r') as f:
            command = f.read()
        if command == 'get_data':
            print("compute consumption")
            dem_r = requests.get(
                "https://apidatos.ree.es/es/datos/demanda/demanda-tiempo-real?start_date=2023-04-02T00:00&end_date=2023-04-02T23:59&time_trunc=hour")

            dem_json = dem_r.json()
            last_dem_real = dem_json["included"][0]["attributes"]["values"][-1]
            date_last_dem_real = last_dem_real["datetime"]

            dem_prog = dem_json["included"][1]["attributes"]["values"]
            for item in dem_prog:
                if item["datetime"] == date_last_dem_real:
                    dem_prog = item
            with open('./gen_dem/results.txt', 'w') as f:
                f.write("{}".format(dem_prog["value"]-last_dem_real["value"]))


if __name__ == "__main__":
    get_ree_data()
