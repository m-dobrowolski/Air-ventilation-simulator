import numpy as np
import json
import signal
from matplotlib import pyplot as plt
from tqdm import tqdm

# Define types of tiles
OUTSIDE = 0
OBSTACLE = 1
INTERIOR = 2
FLOW_RIGHT = 3
FLOW_UP = 4
FLOW_LEFT = 5
FLOW_DOWN = 6

RUNNING = True


def load_map(path):
    with open(path, 'r') as fh:
        data = fh.read()

    map_data = json.loads(data)
    return np.array(map_data)


def mask(shape, map_data, required_type):
    data = np.full(shape, False)
    for y, row in enumerate(map_data):
        start_y = y * 10
        end_y = start_y + 10
        for x, type in enumerate(row):
            start_x = x * 10
            end_x = start_x + 10
            if type == required_type:
                data[start_y:end_y, start_x:end_x] = True
    return data


def handle_close(event):
    global RUNNING
    RUNNING = False


def exit_gracefully():
    global RUNNING
    print("Exiting gracefully...")
    RUNNING = False


def run_simulation(
        path_to_map,
        timesteps_num=2000,
        view_step=100,
        skip_iterations=0,
        is_interactive=False,
        right_speed=1.2,
        up_speed=1.2,
        left_speed=1.2,
        down_speed=1.2
    ):
    global RUNNING
    RUNNING = True

    signal.signal(signal.SIGINT, lambda sig, frame: exit_gracefully())

    map_data = load_map(path_to_map)

    # Simulation parameters
    Nx          = 200  # resolution x-dir
    Ny          = 200  # resolution y-dir
    tau         = 1.0  # collision timescale
    Nt          = timesteps_num  # number of time steps

    # Lattice speeds / weights
    NL = 9
    cxs = np.array([0, 0, 1, 1, 1, 0,-1,-1,-1])
    cys = np.array([0, 1, 1, 0,-1,-1,-1, 0, 1])
    weights = np.array([4/9,1/9,1/36,1/9,1/36,1/9,1/36,1/9,1/36]) # sums to 1

    shape = (Ny, Nx)

    outside = mask(shape, map_data, OUTSIDE)
    obstacles = mask(shape, map_data, OBSTACLE)
    interior = mask(shape, map_data, INTERIOR)
    flow_right = mask(shape, map_data, FLOW_RIGHT)
    flow_up = mask(shape, map_data, FLOW_UP)
    flow_left = mask(shape, map_data, FLOW_LEFT)
    flow_down = mask(shape, map_data, FLOW_DOWN)

    is_flow_right = flow_right.any()
    is_flow_up = flow_up.any()
    is_flow_left = flow_left.any()
    is_flow_down = flow_down.any()

    # Initial Conditions
    # Fill whole map with ones and add some perturbations
    F = np.ones((Ny,Nx,NL)) + 0.03*np.random.randn(Ny,Nx,NL)

    # Initial interior and outside conditions
    # F[outside, 3] = 1.5
    # F[interior, :] = 1

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('close_event', handle_close)

    if is_interactive:
        plt.ion()

    # Simulation Main Loop
    for it in tqdm(range(Nt)):
        # Absorbing boundaries
        F[:, -1, [6, 7, 8]] = F[:, -2, [6, 7, 8]]
        F[:, 0, [2, 3, 4]] = F[:, 1, [2, 3, 4]]
        F[0, :, [1, 2, 8]] = F[1, :, [1, 2, 8]]
        F[-1, :, [4, 5, 6]] = F[-2, :, [4, 5, 6]]

        # Air flow
        if is_flow_right:
            F[flow_right, 3] = right_speed
        if is_flow_up:
            F[flow_up, 1] = up_speed
        if is_flow_left:
            F[flow_left, 7] = left_speed
        if is_flow_down:
            F[flow_down, 5] = down_speed


        # Drift
        for i, cx, cy in zip(range(NL), cxs, cys):
            F[:,:,i] = np.roll(F[:,:,i], cx, axis=1)
            F[:,:,i] = np.roll(F[:,:,i], cy, axis=0)

        # Set reflective boundaries
        # Skip first iteration for avoiding bug (initial reflection, although air is not  moving)
        if it > 1:
            bndryF = F[obstacles,:]
            bndryF = bndryF[:,[0,5,6,7,8,1,2,3,4]]

        # Calculate fluid variables
        rho = np.sum(F,2)
        ux  = np.sum(F*cxs,2) / rho
        uy  = np.sum(F*cys,2) / rho

        if it > 1:
            F[obstacles, :] = bndryF

        ux[obstacles] = 0
        uy[obstacles] = 0


        # Apply Collision
        Feq = np.zeros(F.shape)
        for i, cx, cy, w in zip(range(NL), cxs, cys, weights):
            Feq[:,:,i] = rho*w* (1 + 3*(cx*ux+cy*uy) + 9*(cx*ux+cy*uy)**2/2 - 3*(ux**2+uy**2)/2)

        F += -(1.0/tau) * (F - Feq)

        if it >= skip_iterations and (is_interactive or it % view_step == 0):
            velocity = np.sqrt(ux ** 2 + uy ** 2)
            ax.clear()

            ax.imshow(velocity, origin='lower', cmap='viridis')

            obstacle_overlay = np.ma.masked_array(
                np.ones_like(velocity),
                mask=~obstacles
            )
            ax.imshow(obstacle_overlay, origin='lower', cmap='gray', alpha=0.5)

            plt.draw()

            if is_interactive:
                plt.pause(0.001)
            else:
                pass
                plt.pause(0.01)

        if not RUNNING:
            break

    plt.close('all')

