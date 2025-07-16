class Person:
  def __init__(self, name, age, body, hair_colour, eye_colour):
    self.name = name
    self.age = age
    self.body = body
    self.hair_colour = hair_colour
    self.eye_colour = eye_colour

  def __str__(self):
    return f"{self.name} {self.age} {self.body} {self.hair_colour} {self.eye_colour}"

p1 = Person("John", 36, 'Body is fit', 'Hair black', 'Eyes are blue')

print(p1)