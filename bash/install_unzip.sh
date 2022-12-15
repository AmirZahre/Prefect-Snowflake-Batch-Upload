# # STEP 1: Install unzip
# This script installs 'unzip', which is used to uncompress the .csv files pulled from the API.
# Sudo is not needed as the Prefect Agent runs as root internally.

#### Uncomment echo lines for troubleshooting.

# echo apt-get update
apt-get update

# echo apt-get upgrade
apt-get upgrade

# echo apt-get install zip unzip
apt-get install unzip