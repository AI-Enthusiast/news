#!/bin/bash

# Set the project name -- MUST BE SET
PROJ_NAME="news"

# Set the path to the directory where the script is located
cd "$(dirname "$0")" || exit

# Go to the root directory, currently in its /bin directory
cd ..

# Capture the path up until ~/Code and store it as a variable
base_path="${HOME}/Code/${PROJ_NAME}"

# Initiate logging
run_date="$(date +'%Y-%m-%d')"
exec 2>> "${base_path}/log/logfile_parent_${run_date}.log"

# Ensure SSH agent is running and add the key
eval "$(ssh-agent -s)"
ssh-add "${HOME}/.ssh/id_rsa.pub"

# Update the code
git remote set-url origin git@github.com:AI-Enthusiast/news.git
git stash
git pull origin main

# Build and run the Docker container
docker build -t news . 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
docker run --rm -v "${base_path}/src:/news/src" -v "${base_path}/data:/news/data" -v "${base_path}/archive:/news/archive" -v "${base_path}/log:/news/log" news 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"

# alert that the job is done
echo "Job is done"

# get all .log files in the log directory and move them into a folder with the current date
mkdir -p "${base_path}/log/${run_date}"
mv "${base_path}/log"/*.log "${base_path}/log/${run_date}"

# any date older than 30 days, move them to archive
find "${base_path}/log" -mindepth 1 -maxdepth 1 -type d -ctime +30 -exec mv {} "${base_path}/archive/" \; 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
find "${base_path}/data" -mindepth 1 -maxdepth 1 -type d -ctime +30 -exec mv {} "${base_path}/archive/" \; 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"

# Go to the archive and log directory and all the files
cd "${base_path}/archive" || exit
git add . 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
git commit -m "added: output $(date)" 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
git push 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
cd "${base_path}/log" || exit
git add . 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
git commit -m "added: logs $(date)" 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
git push 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
cd "${base_path}/data" || exit
git add . 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
git commit -m "added: data $(date)" 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"
git push 1>> "${base_path}/log/logfile_${run_date}.log" 2>> "${base_path}/log/errfile_${run_date}.log"