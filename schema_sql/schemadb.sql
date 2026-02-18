ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;


DROP DATABASE IF EXISTS schemadb;
CREATE DATABASE IF NOT EXISTS schemadb;
USE schemadb;

CREATE TABLE buoy_observations (

    station_id VARCHAR(10) ,

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
    tide  DECIMAL(10,1),

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM buoy_observations;