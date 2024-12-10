class Contact:
    def __init__(self, name: str, email: str): # default constructor
        self.__name = name
        self.__email = email
        self.__display = 0

    def name(self):
        return self.__name
    
    def email(self):
        return self.__email

    def isfriend(self):
        return self.__display
    
    def display(self): # displays the contact information
        print(f'  {self.name()} <{self.email()}>')
        