from ansible/ansible:httptester

copy . /app 
run cd /app && pip install .
expose 5000
cmd "/usr/bin/flaskstrap"
