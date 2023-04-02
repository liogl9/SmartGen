import datetime
import time
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json

bucket = "timeSeries"
org = "TeamSocket"
token = "SmXEw_WZ_IbC12fejxEQ850vLXneR_ChiR0orjx--uJgXrFf3RpSBlGRHlGrEg3aMkklrTTjhu4i-3dKpc2grw=="
# Store the URL of your InfluxDB instance
url = "http://172.18.0.2:8086"

centrales = {
    "Alc": {
        "Lugar": "Cáceres", "Nivel": 300.0, "Superficie": 140.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": False,  "Estado": "Bom"
    },
    "Ced": {
        "Lugar": "Cáceres", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": False,  "Estado": "Gen"
    },
    "Agu": {
        "Lugar": "Cantabria", "Nivel": 300.0, "Superficie": 200.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": True,  "Estado": "Stop"
    },
    "Lun": {
        "Lugar": "León", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": False,  "Estado": "Stop"
    },
    "Est": {
        "Lugar": "Lleida", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": True,  "Estado": "Stop"
    },
    "Enc": {
        "Lugar": "Málaga", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": True,  "Estado": "Stop"
    },
    "Ald": {
        "Lugar": "Salamanca", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": True,  "Estado": "Stop"
    },
    "Alm": {
        "Lugar": "Salamanca", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": True,  "Estado": "Stop"
    },
    "Sau": {
        "Lugar": "Salamanca", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": False,  "Estado": "Stop"
    },
    "Cor": {
        "Lugar": "Valencia", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": True,  "Estado": "Stop"
    },
    "Meq": {
        "Lugar": "Zaragoza", "Nivel": 300.0, "Superficie": 160.0, "LimInf": 0.0, "LimSup": 1000.0, "Bombeo": False,  "Estado": "Stop"
    },
}


def get_water_cons():
    with open('./water_cons/command.txt', 'w') as f:
        f.write('get_data')
    water_cons = []
    # Get results
    while not water_cons:
        with open('./water_cons/results.txt', 'r') as f:
            str_res = f.read().split("\n")
            if str_res != [''] and str_res != '':
                water_cons.append(str_res)
                print(water_cons)
    with open('./water_cons/command.txt', 'w') as f:
        f.write('No_command')
    with open('./water_cons/results.txt', 'w') as f:
        pass
    water_cons = water_cons[0]
    water_cons_dict = {x.split()[0]: float(x.split()[1])
                       for x in water_cons}
    return water_cons_dict


def get_prev_prec():
    with open('./prev_prec/command.txt', 'w') as f:
        f.write('get_data')
    prev_prec = []
    # Get results
    while not prev_prec:
        with open('./prev_prec/results.txt', 'r') as f:
            str_res = f.read().split("\n")
            if str_res != [''] and str_res != '':
                prev_prec.append(str_res)
                print(prev_prec)
    with open('./prev_prec/command.txt', 'w') as f:
        f.write('No_command')
    with open('./prev_prec/results.txt', 'w') as f:
        pass
    prev_prec = prev_prec[0]
    prev_prec_dict = {x.split()[0]: float(x.split()[1])
                      for x in prev_prec}
    return prev_prec_dict


def get_dem_stat():
    with open('./gen_dem/command.txt', 'w') as f:
        f.write('get_data')
    gen_dem = []
    # Get results
    while not gen_dem:
        with open('./gen_dem/results.txt', 'r') as f:
            str_res = f.read().split("\n")
            if str_res != [''] and str_res != '':
                gen_dem.append(str_res)
                print(gen_dem)
    with open('./gen_dem/command.txt', 'w') as f:
        f.write('No_command')
    with open('./gen_dem/results.txt', 'w') as f:
        pass
    return float(gen_dem[0][0])


def SmartGen():
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)

    last_water_time = datetime.datetime.now() - datetime.timedelta(days=1)
    last_elec_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
    last_prec_time = datetime.datetime.now() - datetime.timedelta(days=1)
    last_pred_time = datetime.datetime.now() - datetime.timedelta(days=1)
    pred = 0
    while True:
        now = datetime.datetime.now()
        # Get water consumption once a day
        if now - last_water_time >= datetime.timedelta(days=1):
            # Send order to compute it
            water_cons_dict = get_water_cons()
            last_water_time = datetime.datetime.now()

        # Get rain predictions once a day
        if now - last_prec_time >= datetime.timedelta(days=1):
            # Send order to compute it
            # prev_prec_dict = get_prev_prec()
            prev_prec_dict = water_cons_dict
            last_prec_time = datetime.datetime.now()

        # Get electricity demand
        if now - last_elec_time >= datetime.timedelta(minutes=15):
            # Send order to compute it
            gen_dem = get_dem_stat()
            last_elec_time = datetime.datetime.now()

        # make level prediction
        for key in centrales.keys():
            nivel = centrales[key]["Nivel"] + prev_prec_dict[centrales[key]["Lugar"]] * \
                centrales[key]["Superficie"] - \
                water_cons_dict[centrales[key]["Lugar"]]
            # record level prediction once a day
            if now - last_pred_time >= datetime.timedelta(days=1):
                pred = 1
                p = influxdb_client.Point("Nivel_Embalse_pred").tag(
                    "location", centrales[key]["Lugar"]).field("m3", nivel).time(now + datetime.timedelta(days=1))
                write_api.write(bucket=bucket, org=org, record=p)
            if nivel > centrales[key]["LimInf"] + 100:
                centrales[key]["Estado"] = "Gen"
            else:
                if gen_dem > 50 and centrales[key]["Bombeo"]:
                    centrales[key]["Estado"] = "Bom"
                else:
                    centrales[key]["Estado"] = "Stop"
        if pred == 1:
            last_pred_time = now
            pred = 0

        with open("./centrales.json", "w") as outfile:
            json.dump(centrales, outfile)

        time.sleep(5)


if __name__ == "__main__":
    SmartGen()
