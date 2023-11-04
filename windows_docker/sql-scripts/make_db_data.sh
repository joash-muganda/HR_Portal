#! /bin/bash
# windows-specific code
# Load environment variables from docker compose env

# Set MySQL connection variables
USER=$MYSQL_USER
PASSWORD=$MYSQL_PASSWORD
HOST=$MYSQL_HOST
DATABASE=$MYSQL_DATABASE

# Directory where the dump files are located
DUMP_DIR="./dump_files"

# Change to the directory containing the dumps
cd "$DUMP_DIR"

# Loop through all .sql files in the specified directory
for DUMP_FILE in *.dump
do
  echo "Importing $DUMP_FILE into $DATABASE"
  mysql -u hr_system -p"team_late" -h"localhost" -P"3306" -D "$DATABASE" < "$DUMP_FILE"
  if [ $? -eq 0 ]; then
    echo "Imported $DUMP_FILE successfully."
  else
    echo "Error occurred during import of $DUMP_FILE"
    # show error details

  fi
done
