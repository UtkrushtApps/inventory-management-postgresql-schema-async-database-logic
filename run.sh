#!/bin/bash

echo "Starting StockTrack containers..."
docker-compose up -d

echo "Waiting for PostgreSQL startup..."
RETRIES=20
until docker exec postgres pg_isready -U stocktrack_user -h localhost && docker exec postgres psql -U stocktrack_user -d stocktrack_db -c 'SELECT 1' >/dev/null 2>&1
 do
  sleep 2
  ((RETRIES--))
  if [ $RETRIES -le 0 ]; then
    echo "PostgreSQL did not start up in time!"
    exit 1
  fi
done
echo "PostgreSQL is ready."

echo "Applying schema.sql..."
docker exec -i postgres psql -U stocktrack_user -d stocktrack_db < /root/task/schema.sql
if [ -s /root/task/data/sample_data.sql ]; then
  echo "Applying sample_data.sql..."
  docker exec -i postgres psql -U stocktrack_user -d stocktrack_db < /root/task/data/sample_data.sql
fi
echo "Creating database client user..."
docker exec -i postgres psql -U stocktrack_user -d stocktrack_db -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'client_user') THEN CREATE ROLE client_user LOGIN PASSWORD 'client_pwd'; END IF; END \$\$;"

sleep 2
STATUS=1
for i in {1..10}; do
  if curl -s http://localhost:8000/docs | grep -q 'Swagger'; then
    STATUS=0
    break
  fi
  sleep 2
done
if [ $STATUS -ne 0 ]; then
  echo "FastAPI app did not start properly."
  exit 1
fi
echo "StockTrack application and database ready!"
