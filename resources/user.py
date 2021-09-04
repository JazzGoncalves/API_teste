import sqlite3
from sqlite3.dbapi2 import Connection
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Este campo não pode ficar em branco!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Este campo não pode ficar em branco!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
                return {"message": "Um usuário com esse username já existe."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"mensagem": "Usuario criado com sucesso."}, 201

   