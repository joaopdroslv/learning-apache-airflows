CREATE DATABASE IF NOT EXISTS airflow;

USE airflow;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO products (name, price) VALUES
('Iphone 14', 999.99),
('Samsung Galaxy S23', 849.99),
('MacBook Pro 16"', 2399.99),
('Sony WH-1000XM5 Headphones', 348.00),
('Dell XPS 13', 1299.99),
('Apple Watch Series 8', 399.99),
('AirPods Pro 2', 249.99),
('PlayStation 5', 499.99),
('Nintendo Switch OLED', 349.99),
('GoPro Hero 11', 499.99),
('Microsoft Surface Laptop 4', 1499.99),
('LG OLED TV 65"', 1999.99),
('Bose QuietComfort 45', 329.00),
('Kindle Paperwhite', 139.99),
('Garmin Fenix 7', 699.99),
('Sony PlayStation VR2', 549.99),
('Razer Blade 15', 1799.99),
('Apple iPad Air 5', 599.99),
('DJI Mavic Air 2', 799.99),
('Nikon Z6 II Mirrorless Camera', 1999.99);
