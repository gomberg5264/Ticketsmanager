from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_predefined_user():
    username = 'maxwell5264'
    email = 'maxwell5264@example.com'
    password = '3YSoQH5Eq??oNpNYotT9pB&95kbY5EmMpcY8G$'

    with app.app_context():
        try:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print('User already exists')
            else:
                user = User()
                user.username = username
                user.email = email
                user.password_hash = generate_password_hash(password)
                db.session.add(user)
                db.session.commit()
                print('User created successfully')
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            db.session.rollback()

if __name__ == '__main__':
    create_predefined_user()
