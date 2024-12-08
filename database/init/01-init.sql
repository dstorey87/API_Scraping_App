-- database/init/01-init.sql
-- Create schema and tables
CREATE SCHEMA IF NOT EXISTS api_data;

CREATE TABLE IF NOT EXISTS api_data.news_articles (
    id SERIAL PRIMARY KEY,
    source TEXT,
    author TEXT,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_data.guardian_articles (
    id SERIAL PRIMARY KEY,
    headline TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    author VARCHAR(255),
    description TEXT,
    publication_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_data.reddit_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    score INTEGER,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_data.trending_topics (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    score INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL ON SCHEMA api_data TO admin;
GRANT ALL ON ALL TABLES IN SCHEMA api_data TO admin;