"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""

# Object class (Parent)
class Object:
   def __init__(self, name):
      self.name        = name
      self.translation = (0,0,0)
      self.rotation    = (0,0,0)
      self.scale_value = (1,1,1)

   def translate(x, y, z):
      self.translation = (x, y, z)
      print(f"{self.name} translate: {self.translation}")

   def rotate(x, y, z):
      self.rotation = (x, y, z)
      print(f"{self.name} rotate: {self.rotation}")

   def scale(x, y, z):
      self.scale_value = (x, y, z)
      print(f"{self.name} scale: {self.scale_value}")


# Cube class (Child)
class Cube(Object):

   # Default values
   def __init__(self, name):
      super().__init__(name)
      self.color_value = 155, 155, 155

   def translate(self, x=0, y=0, z=0):
      self.translation = (x,y,z)
      print(f"Cube translate values: x = {x}")
      print(f"Cube translate values: y = {y}")
      print(f"Cube translate values: z = {z}")

   def rotate(self, x=0,y=0,z=0):
      self.rotation = (x,y,z)
      print(f"Cube rotate values: x = {x}")
      print(f"Cube rotate values: y = {y}")
      print(f"Cube rotate values: z = {z}")

   def scale(self, x=1,y=1,z=1):
      self.scale_value = (x,y,z)
      print(f"Cube scale values: x = {x}")
      print(f"Cube scale values: y = {y}")
      print(f"Cube scale values: z = {z}")

   def color(R=155,G=155,B=155):
      self.color_value = (R,G,B)
      print(f"Cube Red value: x = {R}")
      print(f"Cube Red value: x = {G}")
      print(f"Cube Red value: x = {B}")

   def print_status(self):
      print(f"Cube name: {self.name}")
      print(f"Translate values: {self.translation}")
      print(f"Rotate values: {self.rotation}")
      print(f"Scale values: {self.scale_value}")
      print(f"RGB values: {self.color_value}")

   def update_transform(self, ttype, value):
      if ttype == "scale":
         self.scale(*value)
      elif ttype == "rotate":
         self.rotate(*value)
      elif ttype == "translate":
         self.translate(*value)
      else:
         print("Invalid choice")

#*********************************************************************#

red_cube = Cube("Red")
red_cube.update_transform("rotate",[50,20,10])
