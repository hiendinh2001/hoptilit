from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import cloudinary
from flask_login import LoginManager
from flask_babelex import Babel


app = Flask(__name__)
app.secret_key = '12#^&*+_%&*)(*(&(*^&^$%$#((*65t87676'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/hoptilit?charset=utf8mb4' % quote('123456')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 6 
app.config['COMMENT_SIZE'] = 3 
app.config['MY_CART'] = 'cart'

MY_SWAGGER = '/swagger'
MY_API = '/static/swagger.json'
SWAGGER_PRINT = get_swaggerui_blueprint(
    MY_SWAGGER,
    MY_API,
    config={
        'app-name': "pythonProject010123"
    }
)

app.register_blueprint(SWAGGER_PRINT, url_prefix=MY_SWAGGER)

db = SQLAlchemy(app=app)
babel = Babel(app=app)

cloudinary.config(
    cloud_name='dnnjwr3bl',
    api_key='537858359784695',
    api_secret='MTiq2hbjq2WyHYUwgX-hJaplU6k',
)

login = LoginManager(app=app)

@babel.localeselector
def load_locale():
    return 'fr'
