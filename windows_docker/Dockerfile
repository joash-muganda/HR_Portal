   # Start from the MySQL image
   FROM mysql:debian
   RUN chown -R mysql:mysql /var/lib/mysql
   RUN chown -R mysql:mysql /docker-entrypoint-initdb.d
   # Install necessary packages for PowerShell
   #RUN apt-get update && apt-get install -y \
   #    curl \
   #    gnupg2 \
   #    apt-transport-https \
   #    lsb-release

   # Add Microsoft's public key
   #RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

   # Add the PowerShell repository to the sources list
   #RUN curl -o /etc/apt/sources.list.d/microsoft.list https://packages.microsoft.com/config/ubuntu/20.04/prod.list

   # Install PowerShell
   #RUN apt-get update && apt-get install -y powershell
   # Install the acl package
   #RUN apt-get install -y acl

