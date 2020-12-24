import os
from dotenv import load_dotenv


load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/.env")


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or \
        f"sqlite:////{os.path.dirname(os.path.realpath(__file__))}/app.db"
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'vZ9YVje1aU'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 25


SWAGGER_CONFIG = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/twitter-clone/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/twitter-clone/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/twitter-clone/apidocs/"
}


SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "twitter-clone api",
        "description": (
            "API docs for twitter-clone.\n\n"
            "Set authorization header using \"Authorize\" to try out endpoints.\n\n"
        )
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": (
                "Token: 'curl --user \"username:password\" -XPOST http://localhost:5001/api/tokens'"
                "\nExample: 'Bearer 2vYuaDza171SSXZWCFQWs9HaOpyBwK0i'"
            )
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}
