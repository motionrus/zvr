# ZVR

Zakaz for execute work. Generete tamplate for continue work on zakaz.

### Instalation

You need `git clone` project, create your env and change on current dir. Install the dependencies
```sh
$ cd zvr
$ pip install -r requirements.txt
```

### Running app
```sh
$ export FLASK_APP = start.py
$ export FLASK_DEBUG = 0
$ flask run
```

### Configure
```
$ cp config_example.py config.py
```
You need edit username and password in config.py file. You may edit other row for changing template

### RoadMap
 - Create simple Auth
 - Storage Auth and use it for storage helpdesk session cookie
 - Create bootstrap template and attach