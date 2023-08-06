import pyautogui
import time
import datetime
import randfacts
import keyboard


now = datetime.datetime.now()


def spam(msg, spamCount, format='gap', delay=0.0):
    time.sleep(delay)
    keycode = 0
    if 'gap' in format:
        keycode = 'space'
    elif 'nl' in format:
        keycode = 'enter'
    else:
        print(
            f"Error while recognizing format.It takes only two arguments 'gap' & 'nl'.'{format}',this is an unknown argument")

    for i in range(spamCount):
        if (keycode != 0):
            pyautogui.typewrite(msg)
            pyautogui.hotkey(keycode)
        elif (keycode == 0):
            break


def infSpam(msg, format='gap', delay=0.0):
    time.sleep(delay)
    keycode = 0
    print("to stop loop press escape")
    if 'gap' in format:
        keycode = 'space'
    elif 'nl' in format:
        keycode = 'enter'
    else:
        print(
            f"Error while recognizing format.It takes only two arguments 'gap' & 'nl'.'{format}',this is an unknown argument")

    while True:
        if (keycode != 0):
            pyautogui.typewrite(msg)
            pyautogui.hotkey(keycode)
            if keyboard.is_pressed('ESC'):
                print("breaking spam")
                break
        elif (keycode == 0):
            break


def currentTime(format="24h", msg="Current time is : "):
    if "24h" in format:
        ct = now.strftime("%H:%M:%S")
        print(msg + ct)
    elif "12h" in format:
        ct = now.strftime("%I:%M:%S %p")
        print(msg + ct)
    else:
        print(
            f"Error while recognizing format.It takes only two arguments '24h' & '12h'.'{format}',this is an unknown argument")


def facts():
    print(randfacts.getFact())


def calculator(msg='Enter an expression to evaluate (or "quit" to exit)', resMsg='result'):
    while True:
        # get input from the user

        input_string = input(
            f'{msg}')

    # check if the user wants to quit
        if input_string.lower() == 'quit':
            break

    # evaluate the expression and print the result
        try:
            result = eval(input_string)
            print(f'{resMsg}', result)
        except (SyntaxError, NameError):
            print('Invalid input')
