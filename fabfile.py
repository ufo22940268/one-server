from fabric.api import *

# the user to use for the remote commands
env.user = 'root'
# the servers where the commands are executed
env.hosts = ['192.241.196.189']

def deploy():
    local('tar -cvf /tmp/k.tar ../one-server')
    put('/tmp/k.tar', '/tmp/k.tar')
    run('tar -xvf /tmp/k.tar')
    with cd('one-server'):
        with prefix('source /usr/bin/virtualenvwrapper.sh'):
            with prefix('workon one-server'):
                run("bash kill.sh")
                run("pip install -r requirements.txt")
                #run("./manage.py init")
                run('gunicorn -w 4 -b 127.0.0.1:20010 run:app')

def kill_unicorn():
    with cd('one-server'):
        run("bash kill.sh")
