#!/bin/bash

# Load environment variables from creds.json
# shellcheck disable=SC2046
export $(jq -r 'to_entries | .[] | "\(.key)=\(.value)"' /var/www/sheepdog/creds.json)

# Start the application (replace this with your actual application start command)
uwsgi --ini /etc/uwsgi/uwsgi.ini
