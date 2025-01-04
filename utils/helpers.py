from flask_restful import fields, reqparse


user_table_dict = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'created_at': fields.DateTime
}


def get_user_args():
    user_args = reqparse.RequestParser()

    necessary_cols = ['username', 'email', 'password']
    for col_name in necessary_cols:
        user_args.add_argument(col_name, type=str, required=True, help=f"{col_name} column can not be empty")

    return user_args
