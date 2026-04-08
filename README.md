This is a project about national buoy database from NOAA. It used Docker containers, MySQL database, Python ingestion scripts, environment variables, and CLI arguments.

To run the project, please run in python 3.10.
1. Type "docker compose up -d" then "docker compose up --build"
2. If there is any error, please type "docker compose down -v" to clear docker images and containers and redo step 1.
2. If you want to change database password, database name, station ID, or year, you only need to change in .env
