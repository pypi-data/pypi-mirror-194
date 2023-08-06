from talktokitty.wait import wait

class Cat:
        def __init__(self, name, color, size):
            self.name = name
            self.color = color
            self.size = size

        def show_face(self):
             if self.name.strip().lower() == 'peaches':
                  print(
"""
|\---/|
| o_o |
 \_^_/
 """
                        )
                  
             if self.name.strip().lower() == 'molasses':
                  print(
"""
 .       .
 |\_---_/|
/   o_o   \\
|    U    |
\  ._I_.  /
 `-_____-'
 """
                        )
        
        def meow(self):
            if self.name.strip().lower() == 'peaches':
                print('muh-mew')
            
            if self.name.strip().lower() == 'molasses':
                print('meo-OH-WOW')

        def intro_self(self):
            self.show_face()
            print(f"hewwo my name is {self.name}. I'm a {self.size} {self.color} kitty")
            wait()
            self.show_face()
            self.meow()
            
