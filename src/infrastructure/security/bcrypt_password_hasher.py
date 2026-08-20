import bcrypt

from src.application.ports.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password):
        return bcrypt.hashpw(password.value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    def verify(self, password, password_hash:str) -> bool:
        return bcrypt.checkpw(password.value.encode("utf-8"), password_hash.encode("utf-8"))