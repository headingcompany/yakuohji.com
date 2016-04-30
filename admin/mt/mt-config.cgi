##          Movable Type configuration file                   ##
##                                                            ##
## This file defines system-wide settings for Movable Type    ##
## In total, there are over a hundred options, but only those ##
## critical for everyone are listed below.                    ##
##                                                            ##
## Information on all others can be found at:                 ##
## http://www.sixapart.jp/movabletype/manual/config

################################################################
##################### REQUIRED SETTINGS ########################
################################################################

# The CGIPath is the URL to your Movable Type directory
CGIPath    http://yakuohji.com/admin/mt/

# The StaticWebPath is the URL to your mt-static directory
# Note: Check the installation documentation to find out 
# whether this is required for your environment.  If it is not,
# simply remove it or comment out the line by prepending a "#".
#StaticWebPath    http://www.example.com/mt-static

#================ DATABASE SETTINGS ==================
#   REMOVE all sections below that refer to databases 
#   other than the one you will be using.

##### MYSQL #####
#ObjectDriver DBI::mysql
#Database DATABASE_NAME
#DBUser DATABASE_USERNAME
#DBPassword DATABASE_PASSWORD
#DBHost localhost

##### POSTGRESQL #####
ObjectDriver DBI::postgres
Database hdg_yakuohji
DBUser hdg_yakuohji
DBPassword abanun
#DBHost localhost

##### SQLITE #####
#ObjectDriver DBI::sqlite
#Database /path/to/sqlite/database/file

##### BERKELEYDB #####
#DataSource  /path/to/database/directory
