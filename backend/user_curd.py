from .table_schemas import User
from fastapi import HTTPException
import bcrypt

def create_user(user_data, db):
    try:
        # Validate password length
        password_bytes = user_data.password.encode("utf-8")
        if len(password_bytes) > 72:
            raise ValueError("Password exceeds maximum length of 72 bytes")

        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

        # Create new user
        db_user = User(
            name=user_data.name,
            age=str(user_data.age),
            email=user_data.email,
            password=hashed_password,
        )

        # Save to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Remove password from return value
        response_user = db_user.__dict__.copy()
        response_user.pop("password", None)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

    return response_user
 
    def get_all_user(db):
    try:
        users = db.query(User).all()
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    return users


def get_user_id(id, db):
    try:
        user = db.query(User).filter(User.id == id).first()
    except Exception as e:
        print(f"Error fetching user by ID {id}: {e}")
        return None
    return user


def update_user_id(id, user_data, db):
    try:
        user = db.query(User).filter(User.id == id).first()
        if user:
            user.name = user_data.name
            user.age = user_data.age
            db.commit()
            db.refresh(user)
            return user
    except Exception as e:
        print(f"Error updating user {id}: {e}")
        db.rollback()
    return None


def delete_user(id, db):
    try:
        user = db.query(User).filter(User.id == id).first()
        if user:
            db.delete(user)
            db.commit()
            return user
    except Exception as e:
        print(f"Error deleting user {id}: {e}")
        db.rollback()
    return None
