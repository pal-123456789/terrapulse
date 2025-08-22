-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Table for event categories
CREATE TABLE IF NOT EXISTS event_categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#FFFFFF',
    icon VARCHAR(50)
);

-- Insert common EONET categories
INSERT INTO event_categories (id, name, description, color, icon) VALUES
('wildfires', 'Wildfires', 'Active wildfires and fire hotspots', '#FF6B6B', '🔥'),
('severeStorms', 'Severe Storms', 'Hurricanes, cyclones, and severe weather systems', '#4ECDC4', '🌀'),
('volcanoes', 'Volcanoes', 'Volcanic eruptions and activities', '#FFE66D', '🌋'),
('icebergs', 'Icebergs', 'Iceberg calving and movements', '#A3D9FF', '🧊'),
('drought', 'Drought', 'Drought conditions and impacts', '#D4A5A5', '🏜️'),
('dustHaze', 'Dust and Haze', 'Dust storms and haze events', '#D9BF77', '🌫️'),
('floods', 'Floods', 'Flooding events and water inundation', '#449DD1', '🌊'),
('landslides', 'Landslides', 'Landslide events and risks', '#9A031E', '⛰️'),
('earthquakes', 'Earthquakes', 'Seismic activities', '#5F0F40', '🌋'),
('manmade', 'Manmade', 'Human-made environmental events', '#B8B8FF', '🏭'),
('seaLakeIce', 'Sea and Lake Ice', 'Ice formation and melting', '#98C1D9', '❄️'),
('tempExtremes', 'Temperature Extremes', 'Heatwaves and cold snaps', '#E36414', '🌡️'),
('waterColor', 'Water Color', 'Algal blooms and water quality events', '#0FA3B1', '🔵')
ON CONFLICT (id) DO NOTHING;

-- Enhanced events table
CREATE TABLE IF NOT EXISTS events (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    description TEXT,
    category_id VARCHAR(50) REFERENCES event_categories(id),
    geometry GEOGRAPHY(GEOMETRY, 4326),
    -- Use GEOGRAPHY type for accurate distance calculations on a sphere
    acquired TIMESTAMP WITH TIME ZONE,
    updated TIMESTAMP WITH TIME ZONE,
    source_url VARCHAR(1024),
    severity VARCHAR(20),
    confidence NUMERIC(3, 2),
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for spatial queries (CRITICAL for performance)
CREATE INDEX IF NOT EXISTS events_geometry_idx ON events USING GIST (geometry);
-- Index for time-based queries
CREATE INDEX IF NOT EXISTS events_acquired_idx ON events (acquired DESC);
-- Index for category-based queries
CREATE INDEX IF NOT EXISTS events_category_idx ON events (category_id);

-- Table for event sources
CREATE TABLE IF NOT EXISTS event_sources (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) REFERENCES events(id) ON DELETE CASCADE,
    source_id VARCHAR(255),
    url VARCHAR(1024)
);

-- Table for user alert preferences
CREATE TABLE IF NOT EXISTS user_alerts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255), -- Would reference users table in a real implementation
    category_id VARCHAR(50) REFERENCES event_categories(id),
    min_severity VARCHAR(20),
    region GEOGRAPHY(GEOMETRY, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);