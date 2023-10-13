from LogInProxy import LogIn
from User import User

class Utilizator(User):
    logIn: User
    profile_image: None
    def __init__(self, mail, password, username, image_key):
        super().__init__(mail, password, username, image_key)
        self.logIn = LogIn(mail, password, username, image_key)

    def validate(self) -> str:
        if (self.logIn.validate_username()[0] and self.logIn.validate_username()[1]
                and self.logIn.validate_username()[2] and self.logIn.validate_username()[3]):
            if(self.mail == "daniel.radu31.dr.dr@gmail.com"):
                self.profile_image = "poza.jpg"
            return "Conectare reusita!"
        elif (self.logIn.validate_username()[0] == False):
            return "Mail incorect!"
        elif (self.logIn.validate_username()[1] == False):
            return "Username incorect!"
        elif (self.logIn.validate_username()[2] == False):
            return "Parola incorecta!"
        elif (self.logIn.validate_username()[3] == False):
            return "Cheie incorecta!"


    def getProfilePicture(self) -> str:
        return self.profile_image

    def getName(self) -> str:
        return self.username

