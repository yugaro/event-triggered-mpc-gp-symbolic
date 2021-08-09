import numpy as np
from blueprint.set_args import set_args
from model.vehicle import Vehicle
import matplotlib.pyplot as plt
np.random.seed(0)


def make_data(args, vehicle):
    xinits = np.array([[0.5, 0.5, 0.5], [-0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, -0.5, 0.5],
                       [-0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5], [2, 2, 2]])
    xinits = xinits * 1
    z_train = np.zeros((1, 5))
    y_train = np.zeros((1, 3))
    for i in range(xinits.shape[0] * 5):
        if i % 5 == 0:
            j = i // 5
            x = xinits[j, :]
        if np.random.rand(1) > .5:
            u = np.array([2, 2 * 1]) * \
                np.random.rand(1) - np.array([0, 1])
        else:
            u = vehicle.getPIDCon(x)
        x_next = vehicle.errRK4(x, u)

        z = np.concatenate([x, u], axis=0)
        z_train = np.concatenate([z_train, z.reshape(1, -1)], axis=0)
        y_train = np.concatenate(
            [y_train, (x_next - x).reshape(1, -1)], axis=0)
        x = x_next

    # fig, ax = plt.subplots(1, 1)
    # ax.plot(z_train[1:, 0], marker='*')
    # ax.grid(linestyle='-')
    # fig.savefig('../image/trajectoryx.pdf')

    # fig, ax = plt.subplots(1, 1)
    # ax.plot(z_train[1:, 1], marker='*')
    # ax.grid(linestyle='-')
    # fig.savefig('../image/trajectoryy.pdf')

    # fig, ax = plt.subplots(1, 1)
    # ax.plot(z_train[1:, 2], marker='*')
    # ax.grid(linestyle='-')
    # fig.savefig('../image/trajectorytheta.pdf')
    return z_train[1:], y_train[1:]


def PID_traj(args, vehicle):
    xinit = np.array([3, 3, 3])
    traj_data = np.zeros((1, 3))
    for i in range(12):
        if i == 0:
            xe = xinit
            xr = np.array(args.xinit_r).reshape(-1)
            traj_data = np.concatenate(
                [traj_data, (xr - xe).reshape(1, -1)], axis=0)
        u = vehicle.getPIDCon(xe)
        xe_next = vehicle.errRK4(xe, u)

        ur = np.array([args.v_r, args.omega_r])
        xr_next = vehicle.realRK4(xr, ur)

        traj_data = np.concatenate(
            [traj_data, (xr_next - xe_next).reshape(1, -1)], axis=0)

        xe = xe_next
        xr = xr_next

    fig, ax = plt.subplots(1, 1)
    ax.plot(traj_data[1:, 0], traj_data[1:, 1])
    plt.show()


if __name__ == '__main__':
    args = set_args()
    vehicle = Vehicle(args)
    z_train, y_train = make_data(args, vehicle)
    np.save('../data/z_train.npy', z_train)
    np.save('../data/y_train.npy', y_train)
    # PID_traj(args, vehicle)
