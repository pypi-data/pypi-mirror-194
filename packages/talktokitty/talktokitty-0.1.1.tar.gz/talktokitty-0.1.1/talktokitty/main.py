from talktokitty.cat import Cat
from talktokitty.wait import wait

def get_name(first_run = True):
    if first_run:
        wait()
        print("Hello!")
        wait()
        print("Welcome to Talk to Kitty, the program that lets you talk to our kitty girls.")
        wait()
        print("Which kitty do you want to talk to")
        wait()
        cat_name = input("... Peaches or Molasses? ")
    else:
        wait()
        cat_name = input("So, do you want to talk to Peaches or Molasses? ")

    if cat_name.strip().lower() not in ['peaches', 'molasses']:
        wait()
        print('Sorry. Only Peaches and Molasses can talk right now. The other kitties are sleepin.')
        return get_name(first_run = False)
    
    else:
        return cat_name
    

def get_size(name):
    name = name.strip().lower()

    size_dict = {
        'peaches': 'lil',
        'molasses': 'big ol'
    }

    return size_dict[name]
    

def get_color(name):
    name = name.strip().lower()
    wait()
    cat_color = input('Great. Just to confirm, what color is her fur? ')

    color_dict = {
        'peaches': ['calico', 'caliby', 'vanilla', 'niller'],
        'molasses': ['tortie', 'choccy', 'chocolate', 'tortoiseshell']
    }

    if cat_color.strip().lower() not in color_dict[name]:
        wait()
        print(f"WRONG. Ya stoopit. She {color_dict[name][0]}. Anyway, here's what {name.title()} has to say:")
        wait()

    else:
        wait()
        print(f"Cool, that's right. Here's what {name.title()} has to say:")
        wait()

    return color_dict[name][0]

def print_cat_art():
    print("""

    ---TALK TO KITTY---
       version 0.1.0

     _._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-)

          """)
    
def run_again():
    again = input('Do you want to go again? (y/n) ')
    return again.strip().lower() == 'y'


def main(first_run = True):
    if first_run:
        print_cat_art()
    cat_name = get_name()
    cat_size = get_size(cat_name)
    cat_color = get_color(cat_name)
    cat = Cat(cat_name, cat_color, cat_size)
    cat.intro_self()
    wait()
    wait()
    if run_again():
        main(first_run = False)

if __name__ == '__main__':
    main()