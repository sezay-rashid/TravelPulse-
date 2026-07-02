-- 1. Total number of bookings
SELECT COUNT(*) AS total_bookings
FROM bookings;

-- 2. Cancellation rate
SELECT 
    ROUND(AVG(is_canceled) * 100, 2) AS cancellation_rate_percentage
FROM bookings;

-- 3. Average daily rate
SELECT 
    ROUND(AVG(adr), 2) AS average_daily_rate
FROM bookings;

-- 4. Bookings by hotel type
SELECT 
    hotel,
    COUNT(*) AS total_bookings
FROM bookings
GROUP BY hotel
ORDER BY total_bookings DESC;

-- 5. Monthly booking volume
SELECT 
    arrival_month,
    COUNT(*) AS total_bookings
FROM bookings
GROUP BY arrival_month;

-- 6. Cancellation rate by hotel type
SELECT 
    hotel,
    ROUND(AVG(is_canceled) * 100, 2) AS cancellation_rate_percentage
FROM bookings
GROUP BY hotel
ORDER BY cancellation_rate_percentage DESC;

-- 7. Top 10 guest countries
SELECT 
    country,
    COUNT(*) AS total_bookings
FROM bookings
GROUP BY country
ORDER BY total_bookings DESC
LIMIT 10;

-- 8. Average ADR by hotel type
SELECT 
    hotel,
    ROUND(AVG(adr), 2) AS average_adr
FROM bookings
GROUP BY hotel;

-- 9. Bookings by market segment
SELECT 
    market_segment,
    COUNT(*) AS total_bookings
FROM bookings
GROUP BY market_segment
ORDER BY total_bookings DESC;

-- 10. Bookings by customer type
SELECT 
    customer_type,
    COUNT(*) AS total_bookings
FROM bookings
GROUP BY customer_type
ORDER BY total_bookings DESC;
