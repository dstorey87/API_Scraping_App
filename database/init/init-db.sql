-- Create schema
CREATE SCHEMA IF NOT EXISTS api_data;

-- Create tables
CREATE TABLE IF NOT EXISTS api_data.news_articles (
    id SERIAL PRIMARY KEY,
    source VARCHAR(255),
    author VARCHAR(255),
    title TEXT NOT NULL,
    description TEXT,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_data.reddit_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    author VARCHAR(255),
    subreddit VARCHAR(255),
    score INTEGER,
    created_at TIMESTAMP
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

CREATE TABLE IF NOT EXISTS api_data.trending_topics (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    score INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_data.logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(50),
    module VARCHAR(255),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL ON SCHEMA api_data TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA api_data TO postgres;