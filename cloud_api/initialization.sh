# Initialize the cloud_api project
docker-compose -f docker-compose.yml -p phd_deployment up -d postgres
sh ./scripts/configure_postgres.sh phd_deployment_postgres_1 api_db
docker-compose -f docker-compose.yml -p phd_deployment stop

docker-compose -f docker-compose.test.yml -p phd_deployment_test up -d postgres
sh ./scripts/configure_postgres.sh phd_deployment_test_postgres_1 api_db_test
docker-compose -f docker-compose.test.yml -p phd_deployment_test stop