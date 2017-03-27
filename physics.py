"""
@Author Alex Chapman
3.26.17

First iteration physics for hover-craft type vehicle

"""
delta_time = 1
mass = 500
moment = 200


def physics(position, velocity, angle, F_net=0, T_net=0, dt=delta_time):
    """
        Inputs:
            position->  Point object holding x and y: (x, y)
            velocity->  Point object holding vx and vy: (vx, vy)
            angle   ->  Point object holding theta and omega
                            (theta, omega)
            F_net   ->  Net Force on car
            T_net   ->  Net Torque on car
            dt      ->  time_step, assumed to be the global variable delta_time
                            this is for the simulation, if desirable a method
                            to find dt can be uncommented.

        Outputs:
            position->  Point object holding updated x and y: (x, y)
            velocity->  Point object holding updated vx and vy: (vx, vy)
            angle   ->  Point object holding updated theta and omega
    """
    F_x = F_net.x
    F_y = F_net.y

    x = position.x
    y = position.y

    vx = velocity.x
    vy = velocity.y

    theta = angle.x
    omega = angle.y
    [x, vx] = integrate(F_x, mass, x, vx, dt)
    [y, vy] = integrate(F_y, mass, y, vy, dt)
    [theta, omega] = integrate(T_net, moment, theta, omega, dt)
    position = Point(x, y)
    velocity = Point(vx, vy)
    angle = Point(theta, omega)
    return [position, velocity, angle]


def integrate(F_net, mass, pos, vel, dt=delta_time):
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


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point(%d, %d)' % (self.x, self.y)


POS = Point(0, 0)
VEL = Point(0, 0)
ANGLE = Point(60, 1)

for i in range(10):
    [pos, vel, ang] = physics(POS, VEL, ANGLE, Point(1000, 0))
    POS = pos
    VEL = vel
    ANGLE = ang
    print(pos.x, pos.y, ':', vel.x, vel.y, ':', ang.x, ang.y)
for i in range(10):
    [pos, vel, ang] = physics(POS, VEL, ANGLE, Point(-1000, 0))
    POS = pos
    VEL = vel
    ANGLE = ang
    print(pos.x, pos.y, ':', vel.x, vel.y, ':', ang.x, ang.y)
