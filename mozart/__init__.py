import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
        location /myprefix {
            proxy_pass http://127.0.0.1:8888;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Script-Name /myprefix;
        }

    In apache:
        RewriteEngine on
        RewriteRule "^/mozart$" "/mozart/" [R]
        SSLProxyEngine on
        ProxyRequests Off
        ProxyPreserveHost Off
        ProxyPass /mozart/static !
        ProxyPass /mozart/ http://localhost:8888/
        ProxyPassReverse /mozart/ http://localhost:8888/
        <Location /mozart>
            Header add "X-Script-Name" "/mozart"
            RequestHeader set "X-Script-Name" "/mozart"
            Header add "X-Scheme" "https"
            RequestHeader set "X-Scheme" "https"
        </Location>
        Alias /mozart/static/ /home/ops/mozart/ops/mozart/mozart/static/
        <Directory /home/ops/mozart/ops/mozart/mozart/static>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        x_forwarded_host = environ.get('HTTP_X_FORWARDED_HOST', '')
        if x_forwarded_host:
            environ['HTTP_HOST'] = x_forwarded_host
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config.from_pyfile('../settings.cfg')

# set database config
dbdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dbdir, 'app.db')
db = SQLAlchemy(app)

# set user auth config
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'views/main.login'

# views blueprints
from mozart.views.main import mod as viewsModule
app.register_blueprint(viewsModule)

# services blueprints
from mozart.services.main import mod as mainModule
app.register_blueprint(mainModule)
from mozart.services.jobs import mod as jobsModule
app.register_blueprint(jobsModule)
from mozart.services.admin import mod as adminModule
app.register_blueprint(adminModule)
from mozart.services.es import mod as esModule
app.register_blueprint(esModule)
from mozart.services.stats import mod as statsModule
app.register_blueprint(statsModule)
from mozart.services.user_rules import mod as userRulesModule
app.register_blueprint(userRulesModule)
from mozart.services.user_tags import mod as userTagsModule
app.register_blueprint(userTagsModule)

# rest API blueprints
from mozart.services.api_v01 import services as api_v01Services
app.register_blueprint(api_v01Services)
from mozart.services.api_v02 import services as api_v02Services
app.register_blueprint(api_v02Services)
