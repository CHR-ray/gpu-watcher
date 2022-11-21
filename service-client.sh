#!/bin/sh

echo 'Install gpuwatch service:'

user=$USER
python_path=/usr/local/anaconda3/bin/python

echo ''
echo 'Installing supervisor...'
sudo apt install -y supervisor

echo ''
echo 'Deploying service...'


log_path=/home/${user}/.gpuwatch
mkdir -p ${log_path}

sudo echo "[program:gpuwatch]
user = ${user}
directory = /home/${user}
command = ${path} gpu-watch/client.py
autostart = true
autorestart = true
stderr_logfile = ${log_path}/stderr.log
stdout_logfile = ${log_path}/stdout.log" \
| sudo tee /etc/supervisor/conf.d/gpuwatch.conf > /dev/null

sudo supervisorctl reread

echo ''
sudo service supervisor restart

echo ''
sudo supervisorctl restart gpuwatch

echo '~DONE~'
echo ''
echo 'Visit http://server:9999 in your browser.'
echo ''
