from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from datetime import date, time, datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        sender = db.Column(db.String(32), unique=True)
        receiver = db.Column(db.String(32))
        message = db.Column(db.String(32))
        subject = db.Column(db.String(32))
        creation_date = db.Column(db.DateTime)

        def __init__(self, sender, receiver, message, subject, creation_date):
            self.sender = sender
            self.receiver = receiver
            self.message = message
            self.subject = subject
            self.creation_date = datetime.utcnow()

   

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sender', 'receiver', 'message', 'subject', 'creation_date')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserManager(Resource):
    @staticmethod
    def get():
        try:
            id = request.args['id']
        except Exception as _:
            id = None

        if not id:
            users = Message.query.all()
            return jsonify(users_schema.dump(users))
        user = Message.query.get(id)
        return jsonify(user_schema.dump(user))

    @staticmethod
    def post():
        sender = request.json['sender']
        receiver = request.json['receiver']
        message = request.json['message']
        subject = request.json['subject']
        creation_date = request.json['creation_date']

        user = Message(sender, receiver, message, subject, creation_date)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'Message': f'Subject: " {subject} ", Message: " {message} " => inserted successfully.'
        })

    @staticmethod
    def put():
        try:
            id = request.args['id']
        except Exception as _:
            id = None

        if not id:
            return jsonify({'Message': 'Must provide the user ID'})

        user = Message.query.get(id)
        sender = request.json['sender']
        receiver = request.json['receiver']
        message = request.json['message']
        subject = request.json['subject']
        creation_date = request.json['creation_date']

        user.sender = sender
        user.receiver = receiver
        user.message = message
        user.subject = subject
        user.creation_date = creation_date

        db.session.commit()
        return jsonify({
            'Message': f'Subject: " {subject} ", Message: " {message} => altered successfully.'
        })

    @staticmethod
    def delete():
        try:
            id = request.args['id']
        except Exception as _:
            id = None

        if not id:
            returnjsonify({'Message': 'Must provide the user ID'})

        user = Message.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'message {str(id)} deleted.'
        })

api.add_resource(UserManager, '/api/message')

if __name__ == '__main__':
    app.run(debug=True)