ALTER USER 'root'@'%'
IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;


DROP DATABASE IF EXISTS buoy_db;
CREATE DATABASE IF NOT EXISTS buoy_db;
USE buoy_db;

CREATE TABLE buoy_observations (
    station_id VARCHAR(10) NOT NULL,
    observation_time DATETIME NOT NULL,
    wdir  DECIMAL(10,1) NOT NULL,
    wspd  DECIMAL(10,1) NOT NULL,
    gst   DECIMAL(10,1) NOT NULL,
    wvht  DECIMAL(10,1) NOT NULL,
    dpd   DECIMAL(10,1) NOT NULL,
    apd   DECIMAL(10,1) NOT NULL,
    mwd   DECIMAL(10,1) NOT NULL,
    pres  DECIMAL(10,1) NOT NULL,
    atmp  DECIMAL(10,1) NOT NULL,
    wtmp  DECIMAL(10,1) NOT NULL,
    dewp  DECIMAL(10,1) NOT NULL,
    vis   DECIMAL(10,1) NOT NULL,
    ptdy  DECIMAL(10,1) NOT NULL,
    tide  DECIMAL(10,1) NOT NULL
);

CREATE TABLE cwind (
    station_id VARCHAR(10) NOT NULL,
    observation_time DATETIME NOT NULL,
    wdir  INT NOT NULL,
    wspd  DECIMAL(10,1) NOT NULL,
    gdr   INT NOT NULL,
    gst  DECIMAL(10,1) NOT NULL,
    gtime  INT NOT NULL
);
