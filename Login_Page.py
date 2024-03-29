from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pass@123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/app_develop'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
db = SQLAlchemy(app)
jwt = JWTManager(app)


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30, collation='utf8_bin'), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=True)

    def get_id(self):
        return self.id


with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    hashed_password = generate_password_hash(password)

    if not username and not password:
        return jsonify({'Message': 'Username and password field should not be a empty'}), 400

    if not username:
        return jsonify({'Message': 'Username should not be empty'}), 400

    if not password:
        return jsonify({'Message': 'Password should not be empty'}), 400

    if not username.strip() or not password.strip():
        return jsonify({'Message': 'Empty spaces not allowed'}), 400

    if Login.query.filter_by(username=username).first():
        return jsonify({'Message': f'Username {username} is already exists!.Please try again.'}), 409

    new_user = Login(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Message': f'Username {username} is created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = Login.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'Message': 'Invalid User name or password'}), 401
    else:
        access_token = create_access_token(identity=user.username)
        return jsonify({'access_token': access_token}), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({'Message': f'Welcome ,{current_user}!This is a protected route.'}), 200


@app.route('/getDetails/<int:id>', methods=['GET'])
def get_details(id):
    details = Login.query.get(id)

    if not details:
        return jsonify({'Message': f'User details not found for id {id}'}), 400
    user_details = {
        'Username': details.username,
        'Password': details.password
    }
    return jsonify(user_details), 200


@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    user = Login.query.get(id)

    if not user:
        return jsonify({'Message': f'User id {id} not found'}), 404
    new_username = request.json.get('username')
    new_password = request.json.get('password')

    if not new_username and not new_password:
        return jsonify({'Message': f'Username and password should not be empty'}), 400
    if new_username:
        if Login.query.filter(Login.username == new_username).first():
            return jsonify(
                {'Message': f'Username {new_username} is already available.Please choose a different username'}), 409
        user.username = new_username

    if new_username:
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
    db.session.commit()
    return jsonify({'Message': f'User id {id} has been updated successfully'})


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Login.query.get(id)
    if not user:
        return jsonify({'Message': f'User id {id} not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'Message': f'User id {id} has been deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
