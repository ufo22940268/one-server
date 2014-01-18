from fabric.api import *

# the user to use for the remote commands
env.user = 'root'
# the servers where the commands are executed
# env.hosts = ['192.241.196.189']

#aliyun
# env.hosts = ['115.29.187.10']

#rms
env.hosts = ['122.226.88.51']


def deploy():
    local('tar --exclude "../one-server/\.*" -cvf /tmp/k.tar ../one-server')
    put('/tmp/k.tar', '/tmp/k.tar')
    run('tar -xvf /tmp/k.tar')
    start()


def start():
    with cd('one-server'):
        run("bash kill.sh")
        run('APPNAME_ENV=prod;gunicorn -w 4 -b 127.0.0.1:20010 run:app &> log.txt', pty=False, shell_escape=False)

def kill_unicorn():
    with cd('one-server'):
        run("bash kill.sh")

def db():
    #clear remote db
    run('mongo one_server --eval "db.dropDatabase()"')
    
    # Migrate db file.
    local('mongodump --out /tmp/db && tar -cvf /tmp/db.tar /tmp/db')
    put('/tmp/db.tar', '/tmp/db.tar')
    with cd('/tmp'):
        run('tar -xvf /tmp/db.tar')
        run('mongorestore /tmp/tmp/db/one_server/ -d one_server')
