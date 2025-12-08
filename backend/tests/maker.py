from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    pw = input("Enter admin password to hash: ")
    print("\nYour bcrypt hash:\n")
    print(hash_password(pw))
    print("\nStore this value in ADMIN_PASSWORD_HASH on Render.")
