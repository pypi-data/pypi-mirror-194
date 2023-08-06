from termcolor import colored
from pyfiglet import Figlet 

def vsb_text(text: str, font: str, color: str):
    f = Figlet(font=font)
    print(colored(f.renderText(text), color))

if __name__ == '__main__':
    vsb_text('Hello', 'isometric2', 'red')
