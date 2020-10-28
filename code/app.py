from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

app = Flask(__name__)
app.secret_key = 'poesiaacustica9'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(ItemList, "/item")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/register")

app.run(debug=True)