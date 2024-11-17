
CREATE DATABASE IF NOT EXISTS delivery;
USE delivery;


CREATE TABLE IF NOT EXISTS parcel_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO parcel_types (name) VALUES ('clothing'), ('electronics'), ('other');

CREATE TABLE IF NOT EXISTS parcels (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    weight FLOAT NOT NULL,
    type_id INT NOT NULL,
    type VARCHAR(255) NOT NULL,
    cost_usd FLOAT NOT NULL,
    shipping_cost_rub FLOAT,
    FOREIGN KEY (type_id) REFERENCES parcel_types(id)
);



CREATE TABLE IF NOT EXISTS shipping_cost_rub_agg (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
	timestamp DATETIME NOT NULL,
    type_id INT NOT NULL,
    type VARCHAR(255) NOT NULL,
    shipping_cost_rub FLOAT NOT NULL,
    FOREIGN KEY (type_id) REFERENCES parcel_types(id)
);