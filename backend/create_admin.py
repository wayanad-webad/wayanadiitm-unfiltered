from app import create_app
from extensions import mongo
import bcrypt
import sys

def create_admin(username, password):
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        if mongo.db.admins.find_one({"username": username}):
            print(f"Admin '{username}' already exists.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mongo.db.admins.insert_one({
            "username": username,
            "password": hashed_password
        })
        print(f"Admin '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <username> <password>")
        sys.exit(1)
    
    create_admin(sys.argv[1], sys.argv[2])
