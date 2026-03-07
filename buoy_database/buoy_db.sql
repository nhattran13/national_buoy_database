ALTER USER 'root'@'%'
IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;


DROP DATABASE IF EXISTS buoy_db;
CREATE DATABASE IF NOT EXISTS buoy_db;
USE buoy_db;

CREATE TABLE buoy_observations (
    station_id VARCHAR(10) NOT NULL,
    observation_time DATETIME NOT NULL,
    wdir  DECIMAL(10,1),
    wspd  DECIMAL(10,1),
    gst   DECIMAL(10,1),
    wvht  DECIMAL(10,1),
    dpd   DECIMAL(10,1),
    apd   DECIMAL(10,1),
    mwd   DECIMAL(10,1),
    pres  DECIMAL(10,1),
    atmp  DECIMAL(10,1),
    wtmp  DECIMAL(10,1),
    dewp  DECIMAL(10,1),
    vis   DECIMAL(10,1),
    ptdy  DECIMAL(10,1),
    tide  DECIMAL(10,1)
);

CREATE TABLE cwind (
    station_id VARCHAR(10) NOT NULL,
    observation_time DATETIME NOT NULL,
    wdir  INT,
    wspd  DECIMAL(10,1),
    gdr   INT,
    gst  DECIMAL(10,1),
    gtime  INT
);
