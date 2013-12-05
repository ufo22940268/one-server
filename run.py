import one_server 

app = one_server.create_app('one_server.settings.DevConfig', env='dev')
#app.run(port=10000, debug=True)
