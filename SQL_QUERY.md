
## Sql Queries


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
    time_out DATETIME
);



INSERT INTO parking_spots (id, spot, driver_name, plate_number, time_in, time_out, is_occupied) VALUES
(1, 'A1', NULL, NULL, NULL, NULL, 0),
(2, 'A2', NULL, NULL, NULL, NULL, 0),
(3, 'A3', NULL, NULL, NULL, NULL, 0),
(4, 'A4', NULL, NULL, NULL, NULL, 0),
(5, 'A5', NULL, NULL, NULL, NULL, 0),
(6, 'B1', NULL, NULL, NULL, NULL, 0),
(7, 'B2', NULL, NULL, NULL, NULL, 0),
(8, 'B3', NULL, NULL, NULL, NULL, 0),
(9, 'B4', NULL, NULL, NULL, NULL, 0),
(10, 'B5', NULL, NULL, NULL, NULL, 0),
(11, 'C1', NULL, NULL, NULL, NULL, 0),
(12, 'C2', NULL, NULL, NULL, NULL, 0),
(13, 'C3', NULL, NULL, NULL, NULL, 0),
(14, 'C4', NULL, NULL, NULL, NULL, 0),
(15, 'C5', NULL, NULL, NULL, NULL, 0),
(16, 'D1', NULL, NULL, NULL, NULL, 0),
(17, 'D2', NULL, NULL, NULL, NULL, 0),
(18, 'D3', NULL, NULL, NULL, NULL, 0),
(19, 'D4', NULL, NULL, NULL, NULL, 0),
(20, 'D5', NULL, NULL, NULL, NULL, 0);