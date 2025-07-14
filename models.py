class User:
    def __init__(self, fullname, username, password, email, role="user"):
        self.__fullname = fullname
        self.__username = username
        self.__password = password
        self.__email = email
        self.__role = role

    # Геттеры (доступ к полям)
    def get_fullname(self):
        return self.__fullname

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_role(self):
        return self.__role

    # Сеттеры (изменение полей)
    def set_fullname(self, fullname):
        self.__fullname = fullname

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_role(self, role):
        if role in ["admin", "user"]:
            self.__role = role

    # Полиморфизм: метод для представления объекта в виде строки
    def to_string(self):
        return f"{self.__fullname},{self.__username},{self.__password},{self.__email},{self.__role}"

# Наследник User -> Admin
class Admin(User):
    def __init__(self, fullname, username, password, email):
        super().__init__(fullname, username, password, email, role="admin")

    # Переопределим to_string
    def to_string(self):
        return f"Admin: {super().to_string()}"
