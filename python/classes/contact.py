class Contact:
    def __init__(self, name: str, email: str): # default constructor
        self.__name = name
        self.__email = email

    def name(self):
        return self.__name
    
    def email(self):
        return self.__email
    
    def display(self): # displays the contact information
        print(f'  {self.name()} <{self.email()}>')