# Windows Docker Database
Using Docker, we can automate and orchestrate the database for quick setup.
In order to use get the database up and running, you need to:

1. Install WSL (Windows Subsystem for Linux) - this will allow Docker to use Linux and 
identify the bash interpreter for running the initialization scripts. 

2. Install the Docker Desktop app for Windows. This will install the Docker CLI and the Docker Engine.

3. CD into this directory & open the Powershell/Command Prompt and enter `bash` to use the bash shell for all following commands.

4. Run the commands in this order:

    > `sudo apt-get update`
    
    > `sudo apt-get install dos2unix`

    > `dos2unix ./sql-scripts/assign_rights.sh`

    > `dos2unix ./sql-scripts/make_db_data.sh`

    > `docker-compose up -d`

5. Wait a couple minutes for the database to initialize and load the data. (Check the log in the Docker container for the DB)

6. To check that the DB is up and running on your local system and is connected to the container, open the Powershell/Command Prompt and enter `bash` to use the bash shell.

7. To enter the SQL Shell: `mysql -u hr_system -h 127.0.0.1 -p` 

    > (enter the password `team_late` when prompted`)

8. To check the database info
    > First, enter `use hr_db;`

    > Then, enter `show tables;`