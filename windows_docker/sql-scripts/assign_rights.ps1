# Windows-specific code
$mysqlPath = "/var/lib/mysql"
$initdbPath = "/docker-entrypoint-initdb.d"

try {
    # Change ownership to mysql:mysql (adjust permissions as needed)
    getfacl -p $mysqlPath > acl.txt
    setfacl --set-file=acl.txt $mysqlPath
    
    getfacl -p $initdbPath > acl.txt
    setfacl --set-file=acl.txt $initdbPath

    # Start the original MySQL entrypoint using powershell
    # Define the path to the original Docker entrypoint file (docker-entrypoint.sh)
    $dockerEntrypointPath = "/usr/local/bin/docker-entrypoint.sh"

    # Define the arguments to pass to the entrypoint script
    $entrypointArgs = @("-u", "mysql")

    # Construct the full command to run the entrypoint script with arguments
    $commandToRun = "$dockerEntrypointPath $($entrypointArgs -join ' ')"

    # Start the original MySQL entrypoint using PowerShell
    Start-Process pwsh -ArgumentList "-c `"$commandToRun`""

    } catch {
        Write-Host "An error occurred: $_"
        # Handle errors as needed
    }