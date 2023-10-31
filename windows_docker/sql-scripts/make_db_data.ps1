# Load environment variables from .env file
Get-Content env | ForEach-Object {
    if ($_ -notlike "#*") {
        $envVariableName, $envVariableValue = $_ -split '=', 2
        if ($envVariableName -and $envVariableValue) {
            [System.Environment]::SetEnvironmentVariable($envVariableName.Trim(), $envVariableValue.Trim(), [System.EnvironmentVariableTarget]::Process)
        }
    }
}

# Set MySQL connection variables
$USER = $env:MYSQL_USER
$PASSWORD = $env:MYSQL_PASSWORD
$HOSTN = $env:MYSQL_HOST
$DATABASE = $env:MYSQL_DB

# Directory where the dump files are located
$DUMP_DIR = ".\dump_files"

# Change to the directory containing the dumps
# Set-Location -Path $DUMP_DIR

# Loop through all .sql files in the specified directory
$dumpFiles = Get-ChildItem -Path $DUMP_DIR -Filter "*.dump"
foreach ($DUMP_FILE in $dumpFiles) {
    $DUMP_FILE_NAME = $DUMP_FILE.Name
    Write-Host "Importing $DUMP_FILE_NAME into $DATABASE"
    
    # Define MySQL command
    $mysqlCommand = "mysql -u $USER -p$PASSWORD -h $HOSTN -P 3306 -D $DATABASE < '$DUMP_FILE_NAME'"
    
    # Execute MySQL command
    Invoke-Expression -Command $mysqlCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Imported $DUMP_FILE_NAME successfully."
    } else {
        Write-Host "Error occurred during import of $DUMP_FILE_NAME"
    }
}
