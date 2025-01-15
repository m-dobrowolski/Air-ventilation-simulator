import os

from simulation import run_simulation
from level_editor.game import Game

MAPS_DIR = 'level_editor/maps'


def clear():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:               # Linux / Mac
        os.system('clear')


def wrong_choice():
    print("Wrong choice")
    input("Press enter to continue...")


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
            if min_idx <= choice <= max_idx:
                return f'{MAPS_DIR}/{maps[choice - 1]}'
        except ValueError:
            wrong_choice()


def set_map_options():
    sim_iterations = 1000
    view_step = 20

    clear()
    while True:
        try:
            iterations = int(input(f'Enter desired amount of simulation iterations: (current: {sim_iterations}):'))
            if iterations > 0:
                sim_iterations = iterations
            else:
                wrong_choice()
                continue

            step = int(input(f'Every how many sim steps to update the view (current: {view_step}):'))
            if step > 0:
                view_step = step
                break
            else:
                wrong_choice()
                continue

        except ValueError as e:
            wrong_choice()

    return sim_iterations, view_step


def main():
    sim_iterations = 2000
    view_step = 100

    while True:
        clear()

        print('1. Start simulation.')
        print('2. Level editor.')
        print('3. Simulation options')
        print('q. Exit.')

        choice = input('Your choice: ')
        if choice == '1':
            map_path = choose_map()
            if map_path:
                run_simulation(map_path, timesteps_num=sim_iterations, view_step=view_step)

        elif choice == '2':
            level_editor = Game()
            map_path = level_editor.play()
            if map_path:
                print(map_path)
                input("Map saved successfully. Press enter to continue.")

        elif choice == '3':
            sim_iterations, view_step = set_map_options()

        elif choice == 'q':
            break
        else:
            wrong_choice()


if __name__ == "__main__":
    main()
