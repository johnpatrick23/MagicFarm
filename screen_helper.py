from time import sleep
import pyautogui

import threading
import keyboard  # pip install keyboard

stop_event = threading.Event()

def keyboard_listener():
    """
    Listens for the 'c' key press to set the stop event.
    """
    while True:
        if keyboard.is_pressed('c'):
            stop_event.set()
            print("Stop signal received (pressed 'c').")
            break
        sleep(0.1)

def start_keyboard_listener():
    """
    Starts the keyboard listener in a separate thread.
    """
    listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    listener_thread.start()


def is_image_on_screen(image_path, confidence=0.8):
    """
    Checks if the given image is currently visible on the screen.

    Args:
        image_path (str): Path to the image file to search for.
        confidence (float): Matching confidence (0.0 - 1.0).

    Returns:
        bool: True if image is found, False otherwise.
    """
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        return location
    except Exception as e:
        return None

def get_weather():
    print("Detecting weather...")
    if is_image_on_screen('img/sunny.png', confidence=0.8) is not None:
        print("Weather detected: sunny")
        return 'sunny'
    elif is_image_on_screen('img/rainy.png', confidence=0.8) is not None:
        print("Weather detected: rainy")
        return 'dawn'
    elif is_image_on_screen('img/frost.png', confidence=0.8) is not None:
        print("Weather detected: frost")
        return 'frost'
    elif is_image_on_screen('img/rain.png', confidence=0.8) is not None:
        print("Weather detected: rain")
        return 'rain'
    else:
        return None

def is_upper_or_lower():
    weather = get_weather()
    print("Determining position (upper/lower)...")
    base_img_path = 'img/' + weather + '/'
    if is_image_on_screen(base_img_path +'/upper_right.png', confidence=0.8) is not None and is_image_on_screen(base_img_path +'/upper_left.png', confidence=0.8) is not None:
        print("Position detected: upper")
        return 'upper'
    elif is_image_on_screen(base_img_path +'/lower_right.png', confidence=0.8) is not None and is_image_on_screen(base_img_path +'/lower_left.png', confidence=0.8) is not None:
        print("Position detected: lower")
        return 'lower'
    
def click_image_center(image_path, confidence=0.8):
    """
    Clicks the center of the given image if it is found on the screen.

    Args:
        image_path (str): Path to the image file to search for.
        confidence (float): Matching confidence (0.0 - 1.0).

    Returns:
        bool: True if image was found and clicked, False otherwise.
    """
    location = is_image_on_screen(image_path, confidence)
    if location:
        center = pyautogui.center(location)
        pyautogui.click(center)
        return True
    return False

def sell():
    if click_image_center('img/sell.png', confidence=0.8):
        sleep(0.5)
        keyboard.send('space') 

def wait_to_grow(afk_minutes=1):
    for _ in range(afk_minutes):
        if stop_event.is_set(): break
        print(f"Waiting for {afk_minutes} minutes to grow plants. Press 'c' to stop.")
        click_image_center('img/shop.png', confidence=0.8)
        sleep(5)
        pyautogui.press('esc')
        sleep(5)
        click_image_center('img/my_garden.png', confidence=0.8)
        sleep(5)
        click_image_center('img/sell.png', confidence=0.8)
        sleep(45)

def harvest(rows=0):
    for row in range(rows):
        click_image_center('img/my_garden.png', confidence=0.8)
        sleep(0.2)
        position = is_upper_or_lower()
        if position == "upper":
            pyautogui.press('down', presses=1+row, interval=0.1)
        elif position == "lower":
            pyautogui.press('up', presses=10-row, interval=0.1)
        sleep(0.2)    
        if stop_event.is_set(): break
        for _ in range(10):
            if stop_event.is_set(): break
            pyautogui.press('right')
            sleep(0.2)
            keyboard.send('space') 
            sleep(0.1)
            keyboard.send('space') 
            sleep(0.1)
        sleep(0.2)
        sell()
        sleep(0.2)