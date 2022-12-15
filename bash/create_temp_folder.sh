# # STEP 2: Create Folder System
# This script creates sub-folders for the .csv partitions used in this flow
# This is done to by-pass Azure Blob Storage automatically deleting empty folders (resulting in these folders not generating in AKS),
# as well as by-pass lack of persistent storage in AKS (therefore can't create and keep these folders in AKS)

# Create sub-folders
mkdir temp/
mkdir temp/ACTIONS
mkdir temp/DAILY
mkdir temp/SEP
mkdir temp/SF1
mkdir temp/SFP