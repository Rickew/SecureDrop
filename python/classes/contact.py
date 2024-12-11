class Contact:
    def __init__(self, name: str, email: str): # default constructor
        self.__name = name
        self.__email = email
        self.isfriend = False
        self.retradd = None

    def name(self):
        return self.__name
    
    def email(self):
        return self.__email
    
    def display(self): # displays the contact information
        if (self.isfriend):
            print(f'  {self.name()} <{self.email()}>')
        