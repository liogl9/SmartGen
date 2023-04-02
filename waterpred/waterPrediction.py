import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
import os
import time
import numpy as np
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Archivo para prediccion de datos de consumo de agua según petición
bucket = "timeSeries"
org = "TeamSocket"
token = "ov51OebBPoCb-b5j-f0CNcA9fO13Pbi8JucOTe91vxWpHHuE7b2SxedBqqYK7x3ukDoo6h6kNwbpgA0m--IBfQ=="
# Store the URL of your InfluxDB instance
url = "http://172.18.0.2:8086"

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


class LSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=100, output_size=1):
        super().__init__()
        self.hidden_size = hidden_size

        # Add an LSTM layer:
        # =================
        self.lstm = nn.LSTM(input_size, hidden_size)

        # Add a fully-connected layer:
        # =================
        self.linear = nn.Linear(hidden_size, output_size)

        # Initialize h0 and c0:
        # =================
        self.hidden = (torch.zeros(1, 1, self.hidden_size),
                       torch.zeros(1, 1, self.hidden_size))

    def forward(self, seq):
        lstm_out, self.hidden = self.lstm(
            seq.view(len(seq), 1, -1), self.hidden)
        pred = self.linear(lstm_out.view(len(seq), -1))
        return pred[-1]  # we only want the last value


if __name__ == "__main__":
    command = ""
    # Cargamos el modelo
    model = LSTM()
    model.load_state_dict(torch.load('./waterpred/models/model_1680372195.pt'))
    model.eval()
    scaler = MinMaxScaler(feature_range=(-1, 1))
    locations = ["Cáceres", "Cantabria", "León", "Lleida",
                 "Málaga", "Salamanca", "Valencia", "Zaragoza"]
    while True:
        # Buscamos si hay alguna petición de predicciones
        with open('./water_cons/command.txt', 'r') as f:
            command = f.read()
        # Si es el caso se genera la predicción
        if command == 'get_data':
            print("compute consumption")
            command = ""
            sum_preds = []
            # Para cada localización genera una predicción
            for location in locations:
                prev_data = []
                while not prev_data:
                    prev_data = query_data("timeSeries", "24h",
                                           "ConsumoAgua", location, "m3")
                prev_data = [x[1] for x in prev_data]
                prev_size = len(prev_data)

                torch.manual_seed(101)

                # torch.save(model.state_dict(), os.path.join(
                #     os.getcwd(), 'WaterPred', 'models', 'model_{}.pt'.format(int(time.time()))))

                # Normalize the training set
                y_norm = scaler.fit_transform(
                    np.array(prev_data).reshape(-1, 1))
                y_norm = torch.FloatTensor(y_norm).view(-1)
                future = 24

                preds = y_norm[-prev_size:].tolist()

                for i in range(future):
                    seq = torch.FloatTensor(preds[-prev_size:])
                    with torch.no_grad():
                        # Reset the hidden parameters here!
                        model.hidden = (torch.zeros(1, 1, model.hidden_size),
                                        torch.zeros(1, 1, model.hidden_size))
                        preds.append(model(seq).item())

                # Inverse-normalize the prediction set
                true_predictions = scaler.inverse_transform(
                    np.array(preds).reshape(-1, 1))
                sum_preds.append(true_predictions[-future:].sum())
            # Guarda los resultados de las predicciones en un archi ve texto en un volumen compartido
            with open('./water_cons/results.txt', 'w') as f:
                for i, location in enumerate(locations):
                    if i == 0:
                        f.write('{} {}'.format(location,
                                               sum_preds[i]))
                    else:
                        f.write('\n{} {}'.format(location,
                                                 sum_preds[i]))

        time.sleep(10)
