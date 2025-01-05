import numpy as np
import json
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

SKIP_ITERATIONS = 0

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

def run_simulation(path_to_map):
    map_data = load_map(path_to_map)

    # Simulation parameters
    Nx          = 200 # map_data["Nx"]    # resolution x-dir
    Ny          = 200 # map_data["Ny"]    # resolution y-dir
    tau         = 0.6 # map_data["tau"]    # collision timescale
    Nt          = 1000 # map_data["Nt"]   # number of timesteps

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
    is_flow_up = flow_right.any()
    is_flow_left = flow_right.any()
    is_flow_down = flow_right.any()

    # Initial Conditions
    # Fill whole map with ones and add some petrubations
    F = np.ones((Ny,Nx,NL)) + 0.03*np.random.randn(Ny,Nx,NL)

    # Initial interior and outside conditions
    # F[outside, 3] = 1.5
    # F[interior, :] = 1

    # Uncomment for interactive plot
    # plt.ion()

    # Simulation Main Loop
    for it in tqdm(range(Nt)):
        # Absorbing boundaries
        F[:, -1, [6, 7, 8]] = F[:, -2, [6, 7, 8]]
        F[:, 0, [2, 3, 4]] = F[:, 1, [2, 3, 4]]
        F[0, :, [1, 2, 8]] = F[1, :, [1, 2, 8]]
        F[-1, :, [4, 5, 6]] = F[-2, :, [4, 5, 6]]

        # Air flow
        if is_flow_right:
            F[flow_right, 3] = 1.5
        if is_flow_up:
            F[flow_up, 1] = 1.5
        if is_flow_left:
            F[flow_left, 7] = 1.5
        if is_flow_down:
            F[flow_down, 5] = 1.5


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

        # if it >= SKIP_ITERATIONS:
        #     plt.imshow(np.sqrt(ux**2+uy**2), origin='lower')
        #     plt.legend()

        #     plt.pause(0.001)
        #     plt.cla()

        if it % 100 == 0:
            plt.imshow(np.sqrt(ux**2+uy**2))
            plt.pause(0.01)
            plt.cla()
