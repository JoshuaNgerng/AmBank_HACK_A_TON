#!/bin/bash
set -e

# Generate the SQL script using environment variables
cat <<EOF > /docker-entrypoint-initdb.d/setup.sql

DO \$\$
BEGIN
    -- Check if the database exists
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB') THEN
        CREATE DATABASE $POSTGRES_DB;
        CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
        ALTER ROLE $POSTGRES_USER SET client_encoding TO 'utf8';
        ALTER ROLE $POSTGRES_USER SET default_transaction_isolation TO 'read committed';
        ALTER ROLE $POSTGRES_USER SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
    END IF;
END \$\$
EOF

# Execute the standard entrypoint for PostgreSQL
exec docker-entrypoint.sh postgres
