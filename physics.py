"""
@Author Alex Chapman
3.26.17

First iteration physics for hover-craft type vehicle

"""

def physics(position, velocity, angle, dt, mass, moment, F_net=[0, 0], T_net=0,):
    """
        Inputs:
            position->  list object holding x and y: (x, y)
            velocity->  list object holding vx and vy: (vx, vy)
            angle   ->  list object holding theta and omega
                            (theta, omega)
            F_net   ->  Net Force on car
            T_net   ->  Net Torque on car
            dt      ->  time_step, assumed to be the global variable delta_time
                            this is for the simulation, if desirable a method
                            to find dt can be uncommented.

        Outputs:
            position->  list object holding updated x and y: (x, y)
            velocity->  list object holding updated vx and vy: (vx, vy)
            angle   ->  list object holding updated theta and omega
    """
    F_x = F_net[0]
    F_y = F_net[1]

    x = position[0]
    y = position[1]

    vx = velocity[0]
    vy = velocity[1]

    # Car needs new omega variable
    # theta = angle[0]
    # omega = angle[1]
    theta = angle
    omega = 0
    [x, vx] = integrate(F_x, mass, x, vx, dt)
    [y, vy] = integrate(F_y, mass, y, vy, dt)
    [theta, omega] = integrate(T_net, moment, theta, omega, dt)
    position = [x, y]
    velocity = [vx, vy]
    # angle = [theta, omega]
    angle = angle
    return [position, velocity, angle]


def integrate(F_net, mass, pos, vel, dt):
    """
        Function to do all of the heavy lifting for the physics function.
        Calculates both the rotational and linear motions.

        Inputs:
            F_net->  Net force (or torque) on the car before time step
            mass ->  Mass if Force, Moment if Torque
            pos  ->  x, y, theta position before time step
            vel  ->  dx, dy, or dtheta of car before time step
            dt   ->  dt timestep for calculation

        Outputs:
            pos->  x, y, or theta of vehicle after time_step
            vel->  dx, dy, or dtheta of vehicle after time step

    """
    acc = F_net / mass

    vel_old = vel
    vel = acc * dt + vel
    pos = .5 * acc * dt**2 + vel_old*dt + pos
    return [pos, vel]
