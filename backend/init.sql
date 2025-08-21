-- Initialize vocabulary_vault database
-- This script runs when the PostgreSQL container starts for the first time

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE vocabulary_vault'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'vocabulary_vault')\gexec

-- Connect to the vocabulary_vault database
\c vocabulary_vault;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges to the vocabulary_user
GRANT ALL PRIVILEGES ON DATABASE vocabulary_vault TO vocabulary_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vocabulary_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO vocabulary_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO vocabulary_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO vocabulary_user;
