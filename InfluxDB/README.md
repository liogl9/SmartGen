# InfluxDB container

After downloading the official InfluxDB image

docker pull InfluxDB

Create the network

docker network create mynetwork

Start the container creating a volume for persistent data for it

docker run -d --name influxdb -p 8086:8086 -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_PASSWORD=admin123 -v influxdbdata:/var/lib/influxdb influxdb --network mynetwork

check the ip

docker network inspect mynetwork

Copy the ip into the files of waterprediction.py main.py writeInfluxDB.py

Access the localhost:8086 server and generate 3 tokens

copy each token into the previous files mentioned
