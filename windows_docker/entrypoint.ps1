# entrypoint.ps1
# Start MySQL or any other necessary commands
Write-Host "Starting MySQL"
Start-Process -FilePath "mysqld_safe"
# Get a list of all .ps1 files in the sql-scripts directory and sort them alphabetically
$scriptFiles = Get-ChildItem -Path .\sql-scripts\*.ps1 | Sort-Object

# Execute each script in alphabetical order
foreach ($scriptFile in $scriptFiles) {
    Write-Host "Running $($scriptFile.Name)"
    & "pwsh" -ExecutionPolicy Bypass -File $scriptFile.FullName
}
