from app.models import User, db

class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def save_user(user):
        
        db.session.add(user)
        db.session.commit()
        return user
