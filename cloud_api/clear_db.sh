# Script just for testing and debugging purposes
docker-compose -f docker-compose.yml -p phd_deployment stop
sudo rm -rf /var/opt/api_local/pg_data
sh initialization.sh