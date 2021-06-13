class Dog():
  name = ""
  age = 0
  __breed = None
  def __init__(self, dog_name, dog_age, dog_breed):
    self.name = dog_name
    self.age = dog_age
    self.__breed = dog_breed


#print(scout)
#print(scout.__breed)
#print(scout.name)
#print(scout.age)

#print scout doesn't print out anything, because we didn't specify which attributes
#print(scout.__breed) shows that 'Dog' object has no attribute '__breed'. Because breed is
#encapsulate variable and is not readable

  def speak(self, sound):
    print(self.name, "says", sound)

  def run(self, speed):
    print(self.name, "runs", speed, "mph")

  def description(self):
    print(self.name, "is a", self.age,  "year old", self.__breed)

  def define_buddy(self, buddy):
    self.buddy = buddy
    buddy.buddy = self

scout = Dog("Scout", 2, "Belgian Malinois")
#scout.speak("woof")
#scout.description()

skippy = Dog("Skippy", 3 ,"Belgian Malinois")
skippy.define_buddy(scout)
scout.buddy.description()





