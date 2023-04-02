# InfluxDB container

After downloading the official InfluxDB image

docker pull InfluxDB

Start the container creating a volume for persistent data for it

docker run -d --name influxdb -p 8086:8086 -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_PASSWORD=admin123 -v influxdbdata:/var/lib/influxdb influxdb

Acces the local host and load data from the following file:

Api token for writing:

KnozwwefZRA5450uPDbBfYNO75B16kSaPZ3do02a5AhrL6lK7wM1oq0myJ2AUhg2TO9IgaP17RrJIuNFu74WcQ==
Admins token: xqsm_Qo3mLMR5w7V9CzZ_1avBfV0pvRmAyiEhPMshOsIkIvG6fV_oLIdnhoGCbkVzmWH8mHyT2e2QkDNjREq3A==

Api token for reading:

Wg4DmUNeNTPwPZXTeiY3oE39gD-1S4WcOhYAW3UhGK7J3zoQ2RzeV3b_HGA366ykCJDTU7Eu6eULb1m4n44kKA==
