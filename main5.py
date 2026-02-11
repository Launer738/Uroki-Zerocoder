class User():
    def __init__(self, id, name, level="user"):
        self.__id = id
        self.__name = name
        self.__level = level

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_level(self):
        return self.__level

    def set_name(self, new_name):
        self.__name = new_name

    def set_level(self, new_level):
        self.__level = new_level

class Admin(User):
    users = []

    def __init__(self, id, name):
        super().__init__(id, name, "admin")

    def add_user(self, user):
        Admin.users.append(user)

    def remove_user(self, user_id):
        for user in Admin.users:
            if user.get_id() == user_id:
                Admin.users.remove(user)
                break

        
user1 = User(1, "Ваня")
print(user1.get_level())

admin1 = Admin(2, "Петр")
print(admin1.get_level())

admin1.add_user(user1)
print(len(Admin.users))

admin1.remove_user(1)
print(len(Admin.users))