# Script just for testing and debugging purposes
docker-compose -f docker-compose.test.yml -p phd_deployment_test stop
sudo rm -rf /var/opt/api_test/pg_data
sh initialization.sh