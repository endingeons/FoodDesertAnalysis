CREATE DATABASE IF NOT EXISTS fooddesert;
USE fooddesert;

# DROP TABLE IF EXISTS restaurant;
# DROP TABLE IF EXISTS census_tract;

CREATE TABLE census_tract(
census_tract_id      BIGINT              PRIMARY KEY,
LILATracts_1And10    BOOL NOT NULL,
state                VARCHAR(500)     NOT NULL,
county               VARCHAR(150)     NOT NULL,
latitude        	 DECIMAL(15, 10)   NOT NULL,
longitude            DECIMAL(15, 10)   NOT NULL
);

CREATE TABLE restaurant(
	restaurant_key      INT             PRIMARY KEY     AUTO_INCREMENT,
	place_id   			VARCHAR(520)    NOT NULL,
    restaurant_name 	VARCHAR(200)    NOT NULL,
    census_tract_id     BIGINT             NOT NULL,
    CONSTRAINT fk_census_tract_id FOREIGN KEY (census_tract_id) 
    REFERENCES census_tract (census_tract_id), 
    price_level 		INT,
    rating 				DECIMAL(5, 2)   NOT NULL,
    user_rating_total 	INT   			NOT NULL,
    avg_calories 		DECIMAL(5, 2)   NOT NULL,
    avg_fat 			DECIMAL(5, 2)   NOT NULL,
    avg_protein 		DECIMAL(5, 2)   NOT NULL,
    avg_carbs 			DECIMAL(5, 2)   NOT NULL
);
