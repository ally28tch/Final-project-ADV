CREATE DATABASE smartpark;
USE smartpark;

CREATE TABLE parking_spots (
    id INT PRIMARY KEY,
    spot VARCHAR(10),
    driver_name VARCHAR(255),
    plate_number VARCHAR(50),
    time_in DATETIME,
    time_out DATETIME,
    is_occupied TINYINT(1) DEFAULT 0
);

CREATE TABLE parking_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    spot_id INT,
    driver_name VARCHAR(255),
    plate_number VARCHAR(50),
    time_in DATETIME,
    time_out DATETIME,
    FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
);