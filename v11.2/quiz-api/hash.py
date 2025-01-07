from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])
hashed_password = pwd_context.hash("filip123")
print(hashed_password)
