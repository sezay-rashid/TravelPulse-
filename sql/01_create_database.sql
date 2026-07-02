USE travelpulse_db;

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel VARCHAR(50),
    is_canceled TINYINT,
    lead_time INT,
    arrival_year INT,
    arrival_month VARCHAR(20),
    arrival_week INT,
    arrival_day INT,
    stays_weekend INT,
    stays_weekday INT,
    total_guests INT,
    meal VARCHAR(20),
    country VARCHAR(10),
    market_segment VARCHAR(50),
    adr DECIMAL(10,2),
    deposit_type VARCHAR(30),
    customer_type VARCHAR(30),
    reservation_status VARCHAR(20)
);
