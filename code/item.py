from flask_restful import Resource, request, reqparse
from flask_jwt import jwt_required

items_list = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items_list), None)
        return {"item": item}, 200 if item else 404

    @jwt_required()
    def post(self, name):      
        if next(filter(lambda x: x["name"] == name, items_list), None):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = {"name": name, "price": request_data["price"]}
        items_list.append(item)
        return item, 201
    
    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()

        item =  next(filter(lambda x: x["name"] == name, items_list), None)
        if item is None:
            item = {"name": name, "price": request_data["price"]}
            items_list.append(item)
        else:
            item.update(request_data)

        return item, 200

    @jwt_required()
    def delete(self, name):
        global items_list
        items_list = list(filter(lambda x: x["name"] != name, items_list))
        return {'message': 'Item deleted'}, 200
        
class ItemList(Resource):
    @jwt_required()
    def get(self):
        return items_list, 200