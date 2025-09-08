import screen_helper
from time import sleep

__main__ = "__main__"
if __name__ == __main__:
    screen_helper.start_keyboard_listener()
    while not screen_helper.stop_event.is_set():
        screen_helper.harvest(rows=5)
        screen_helper.wait_to_grow(afk_minutes=4)
        