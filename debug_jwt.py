from datetime import datetime, timedelta

from jose import JWTError, jwt

# Use the same settings as in your security.py
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return {"username": username, "exp": payload.get("exp")}
    except JWTError:
        return None


def main():
    # Create a test token
    username = input("Enter username for token test: ")
    token = create_access_token({"sub": username})

    print(f"\nGenerated token:\n{token}\n")

    # Verify the token
    decoded = verify_token(token)
    if decoded:
        print(f"✅ Token verification SUCCESSFUL")
        print(f"Username from token: {decoded['username']}")
        expiry = datetime.fromtimestamp(decoded["exp"])
        print(
            f"Token expires: {expiry} (in {(expiry - datetime.utcnow()).total_seconds() / 3600:.1f} hours)"
        )
    else:
        print("❌ Token verification FAILED")


if __name__ == "__main__":
    main()
