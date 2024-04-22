import time
import keyboard

'''def press_key(key, duration):
    if key == 'left':
        keyboard.press("left")
    elif key == 'right':
        keyboard.press("right")
    elif key == 'space':
        keyboard.press("space")
    time.sleep(abs(duration))
    if key == 'left':
        keyboard.release("left")
    elif key == 'right':
        keyboard.release("right")
    elif key == 'space':
        keyboard.release("space")'''

'''def handle_input(input_list):
    if len(input_list) != 2:
        print("Invalid input list. It should contain two elements.")
        return
    
    time_spacebar_pressed = input_list[0]
    duration = input_list[1]

    press_key('space', time_spacebar_pressed)

    if duration < 0:
        press_key('left', abs(duration))
    else:
        press_key('right', duration)'''


def press_keys(space, direction):
    # Press space 'delay' times
    keyboard.press('space')
    time.sleep(abs(space))
    keyboard.release('space')
    
    # Press left or right based on the sign of 'direction'
    if direction < 0:
        keyboard.press('left')
        time.sleep(abs(direction))
        keyboard.release('left')
    elif direction > 0: 
        keyboard.press('right')
        time.sleep(abs(direction))
        keyboard.release('right')
