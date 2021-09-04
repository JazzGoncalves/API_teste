from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type = float,
            required = True,
            help = "Este campo não ser deixado em branco"
        )
        parser.add_argument('store_id',
            type = int,
            required = True,
            help = "Todos os itens da loja precisam de um id"
        )

        #@jwt_required()
        def get(self, name):
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
            return {'message': "Item não encontrado"},404

            
        def post(self, name):
            if ItemModel.find_by_name(name):
                return {'mensagem': "Um item com o nome " '{}'" já existe".format(name)},400
            
            data = Item.parser.parse_args()

            item = ItemModel(name,**data) 

            try:
                item.save_to_db()
            except:
                return {"message": "Erro na operação com o item"},500

            return item.json(),201
        
          
        def delete(self, name):
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
            return {'message': 'Item deletado'}
            
        def put(self, name):
            data = Item.parser.parse_args()
            
            item = ItemModel.find_by_name(name)
            
            if item is None:
                item = ItemModel(name,**data)
            else:
               item.price = data['price']

            item.save_to_db()
            return item.json()
        
          
class ItemList(Resource):
        def get(self):
           return {'items': [x.json() for x in ItemModel.query.all()]}
