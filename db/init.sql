CREATE DATABASE awardData;
use awardData;

CREATE TABLE IF NOT EXISTS oscarAgeMale (
    `id` INT NOT NULL AUTO_INCREMENT,
    `year` INT,
    `age` INT,
    `name` VARCHAR(22) ,
    `movie` VARCHAR(43) ,
    PRIMARY KEY (`id`)
);
