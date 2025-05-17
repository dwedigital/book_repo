from passlib.context import CryptContext

from app.database import SessionLocal
from app.models.models import User

# Use the same password hashing configuration as in your security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def main():
    # Connect to the database
    db = SessionLocal()

    try:
        # Get username from user
        username = input("Enter username to check: ")

        # Get the user from the database
        user = db.query(User).filter(User.username == username).first()

        if not user:
            print(f"User '{username}' not found in the database!")
            return

        print(f"User found: {user.username}, Email: {user.email}")

        if user.password:
            print(f"Stored password hash: {user.password}")
        else:
            print("User has no password set!")

            # Set a password for this user if needed
            set_password = input("Do you want to set a password for this user? (y/n): ")
            if set_password.lower() == "y":
                new_password = input("Enter new password: ")
                user.password = hash_password(new_password)
                db.commit()
                print(f"Password set and hashed as: {user.password}")

        # Test password verification
        test_password = input("Enter password to test: ")
        if user.password and verify_password(test_password, user.password):
            print("✅ Password verification SUCCESSFUL")
        else:
            print("❌ Password verification FAILED")

    finally:
        db.close()


if __name__ == "__main__":
    main()
