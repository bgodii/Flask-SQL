import sqlite3
from flask_restful import Resource, request, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200

    @classmethod
    def insert(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item

        return {'message': 'Item not Found'}, 404

    def post(self, name):      
        if self.find_by_name(name):
            return {'message': 'Item not Found'}, 404

        request_data = Item.parser.parse_args()
        item = {"name": name, "price": request_data["price"]}
        try:
            self.insert(item)
        except Exception as err:
            return {"message": err}
    
        return item, 201

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()
        
        item = self.find_by_name(name)
        updated_item = {"name": name, "price": request_data["price"]}

        if item is None:
            try:
                self.insert(updated_item)
            except Exception as err:
                return {'message': err}, 500
        else:
            try:
                self.update(updated_item)
            except Exception as err:
                return {'message': err}, 500

        return updated_item, 200

    @jwt_required()
    def delete(self, name):
        if not self.find_by_name(name):  
            return {"message": "item does not exist!"}, 404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        
        connection.commit()
        connection.close()
        
        return {'message': 'Item deleted'}, 200
        
class ItemList(Resource):
    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()

        return {"items": items}