


class Dog:
    def __init__(self, name) :
        self.name = name 

    def speak(self) :
        print( "Woof! My name is ", self.name)

if __name__ == "__main__" :
    dog1=Dog("Rover")
    dog2 = Dog('Rex')

    dog1.speak()
    dog2.speak()