import os

from simulation import run_simulation

MAPS_DIR = 'level_editor/maps'

def clear():
    if os.name == 'nt': # Windows
        os.system('cls')
    else:               # Linux / Mac
        os.system('clear')

def wrong_choice():
    print("Wrong choice")
    input("Press any key to continue...")

def choose_map():
    maps = os.listdir(MAPS_DIR)
    min_idx = 1 if maps else None
    max_idx = len(maps) if maps else None


    while True:
        clear()

        for idx, map in enumerate(maps, 1):
            print(f'{idx}. {map}')
        print('q. Go back.')

        choice = input('Choose map: ')
        if choice == 'q':
            return None

        try:
            choice = int(choice)
            print(f'choice{choice}')
            if min_idx <= choice and choice <= max_idx:
                return f'{MAPS_DIR}/{maps[choice - 1]}'
        except ValueError:
            wrong_choice()
            continue


def main():
    while True:
        clear()

        print('1. Start simulation.')
        print('2. Level editor.')
        print('q. Exit.')

        choice = input('Your choice: ')
        if choice == '1':
            map_path = choose_map()
            if map_path:
                run_simulation(map_path)
        elif choice == '2':
            pass
        elif choice == 'q':
            break
        else:
            wrong_choice()

if __name__=="__main__":
    main()