



class User:
    def __init__(self, user_id: str, name: str):
        if not user_id:
            raise ValueError("User_id cannot be empty")
        if not name:
            raise ValueError("Name cannot be empty")

        self.id = user_id
        self.name = name
