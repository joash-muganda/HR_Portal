#!/bin/bash

# Change ownership and permissions of /var/lib/mysql
chown -R mysql:mysql /var/lib/mysql


# Start the original MySQL entrypoint
exec /usr/local/bin/docker-entrypoint.sh "$@"
