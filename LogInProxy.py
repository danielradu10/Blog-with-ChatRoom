from werkzeug.utils import secure_filename
from PIL import Image, ImageChops

from User import User


class LogIn(User):

    def __init__(self, email, username, password, image):
        super().__init__(email, username, password, image)


    def verify_email(self) -> bool:
        print("Email: " + self.mail)
        if(self.mail == "daniel.radu31.dr.dr@gmail.com"):
           print("Ai introdus emailul corect")
           return True

        return False

    def verify_password(self):
        if(self.password == "PortaculDeAur"):
            print("Parola e corecta")
            return True
        else:
            print("Parola e gresita")
            return False

    def verify_username(self) -> bool:
        if(self.username == "DanielRdw14"):
            print("Username-ul tau este corect")
            return True
        print("Username:" + self.username)
        print("Username-ul este gresit")
        return False

    def verify_image(self) -> bool:
        filename = secure_filename(self.image.filename)
        mimetype = self.image.mimetype

        if not filename or not mimetype:
            print("Not a image")
        else:
            print("E imagine")
            img1 = Image.open('descarcare.jpg')
            img2 = Image.open('cheie.jpg')
            diff = ImageChops.difference(img1, img2)
            if (diff.getbbox()):
                print("Imaginea introdusa este diferita de cheie")
                return False
            else:
                print("A introdus chiar cheia")
                return True

    def validate_username(self) -> (bool, bool, bool, bool):
        return (self.verify_email(), self.verify_username(), self.verify_password(), self.verify_image())