""" This python file is just for easy & simple testing of the Settings class """
import random
from src.generalpy import Settings


defSettings = {
    'key1': True,
    'key2': 'value2'
}

s = Settings(
    default_settings=defSettings,
    hard_fetch=False
)

def print_v():
    print(f"[V] {s.settings_directory = }")
    print(f"[V] {s.settings_file_name = }")
    print(f"[V] {s.settings_file_path = }")
    print(f"[V] {s.default_settings = }")

def print_f():
    print(f"[F] {s.get_all_settings() = }")
    print(f"[F] {s.get_setting('key1') = }")
    print(f"[F] {s.get_setting('key2') = }")
    print(f"[F] {s.get_setting('unavailable-key') = }")

def prt():
    print()
    print_v()
    print()
    print_f()


if __name__ == "__main__":        
    while True:
        prt()
        inputValue = input('\n\n>>> Again? (r/c/n/anything-else) ')
        if inputValue == 'r':
            s.reset()
        if inputValue == 'c':
            s.update_setting(
                'key1', 
                not s.get_setting('key1')
            )
        if inputValue == 'n':
            s.update_setting(
                str(random.randint(1, 1000)),
                str(random.randint(1, 1000))
            )
