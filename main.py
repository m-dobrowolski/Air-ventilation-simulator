import numpy as np
import json
from matplotlib import pyplot as plt
from tqdm import tqdm

def load_map(path):
    with open(path, 'r') as fh:
        data = fh.read()

    map_data = json.loads(data)
    return np.array(map_data)

def main():
    map_data = load_map('object_editor/maps/mymap')

    # Simulation parameters
    Nx          = 200 #map_data["Nx"]    # resolution x-dir
    Ny          = 200 #map_data["Ny"]    # resolution y-dir
    tau         = 0.6 #map_data["tau"]    # collision timescale
    Nt          = 1000 #map_data["Nt"]   # number of timesteps

    # Lattice speeds / weights
    NL = 9
    cxs = np.array([0, 0, 1, 1, 1, 0,-1,-1,-1])
    cys = np.array([0, 1, 1, 0,-1,-1,-1, 0, 1])
    weights = np.array([4/9,1/9,1/36,1/9,1/36,1/9,1/36,1/9,1/36]) # sums to 1

    # Initial Conditions - flow to the right with some perturbations
    F = np.ones((Ny,Nx,NL)) + 0.01*np.random.randn(Ny,Nx,NL)
    F[:,:, 3] = 2.3

    # Cylinder boundary
    # def distance(x1, y1, x2, y2):
    #     return np.sqrt((x2-x1)**2 + (y2-y1)**2)

    # cylinder = np.full((Ny, Nx), False)
    # for y in (0, Ny):
    #     for x in range (0, Nx):
    #         if(distance(Nx//4, Ny//2, x, y) < 13):
    #             cylinder[y][x] = True

    obstacles = np.full((Ny, Nx), False)

    for y, row in enumerate(map_data):
        start_y = y * 10
        end_y = start_y + 10
        for x, type in enumerate(row):
            start_x = x * 10
            end_x = start_x + 10
            if type == 1:
                obstacles[start_y:end_y, start_x:end_x] = True


    # plt.ion()

    # Simulation Main Loop
    for it in tqdm(range(Nt)):
        # Absorbing boundaries
        F[:, -1, [6, 7, 8]] = F[:, -2, [6, 7, 8]]
        F[:, 0, [2, 3, 4]] = F[:, 1, [2, 3, 4]]
        F[0, :, [1, 2, 8]] = F[1, :, [1, 2, 8]]
        F[-1, :, [4, 5, 6]] = F[-2, :, [4, 5, 6]]


        # Drift
        for i, cx, cy in zip(range(NL), cxs, cys):
            F[:,:,i] = np.roll(F[:,:,i], cx, axis=1)
            F[:,:,i] = np.roll(F[:,:,i], cy, axis=0)

        # Set reflective boundaries
        bndryF = F[obstacles,:]
        bndryF = bndryF[:,[0,5,6,7,8,1,2,3,4]]

        # Calculate fluid variables
        rho = np.sum(F,2)
        ux  = np.sum(F*cxs,2) / rho
        uy  = np.sum(F*cys,2) / rho

        # F[obstacles, :] = bndryF
        F[obstacles, :] = bndryF
        ux[obstacles] = 0
        uy[obstacles] = 0


        # Apply Collision
        Feq = np.zeros(F.shape)
        for i, cx, cy, w in zip(range(NL), cxs, cys, weights):
            Feq[:,:,i] = rho*w* (1 + 3*(cx*ux+cy*uy) + 9*(cx*ux+cy*uy)**2/2 - 3*(ux**2+uy**2)/2)

        F += -(1.0/tau) * (F - Feq)

        # Apply boundary
        F[obstacles,:] = bndryF

        # if it % 100 == 0:
        # plt.imshow(np.sqrt(ux**2+uy**2))
        # plt.pause(0.001)
        # plt.cla()

        if it % 100 == 0:
            plt.imshow(np.sqrt(ux**2+uy**2))
            plt.pause(0.01)
            plt.cla()


if __name__ == "__main__":
    main()