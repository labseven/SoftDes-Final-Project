"""
@Author Alex Chapman
3.27.17

Second iteration physics for bicycle-type vehicle

"""
import math


def update_physics(position, velocity, angle, steering, F_traction, mass,
                   moment, dt):
    """
        position -> vector of positions(x, y) respectively
        velocity -> vector of velocities (x, y) respectively
        angle   ->  list object holding theta and omega
                        (theta, omega)
        steering -> input from steering
        F_traction -> Tractive force input from keys (accelerating or brakes)
        mass
        moment
        dt

        beta -> angle between velocity and car in RADIANS
    """
    L = 3  # Wheelbase in meters

    a = 1/3
    b = 1 - a
    a = a*L
    b = b*L

    theta = angle[0]
    omega = angle[1]

    # Initialize all constant values: some are magic numbers
    max_slip_angle = math.radians(12)
    # C_cornering = (mass * 9.81) / (2 * max_slip_angle)
    C_cornering = 2000
    C_drag = 0.75
    C_rolling = 30 * C_drag
    speed = (velocity[0]**2 + velocity[1]**2)**.5

    car_vector = [math.sin(theta), math.cos(theta)]
    direction = velocity[0] * car_vector[0] + velocity[1] * car_vector[1]
    if not direction == 0:
        direction = direction / abs(direction)

    if velocity[1] == 0:
        velocity[1] = .001

    # velocity_ratio = abs(velocity[0] / velocity[1])
    # coefficient = 1
    # if velocity[0] > 0 or velocity[1] > 0:
    #     coefficient = -1
    #     print('A')

    # if velocity[0] < 0 and velocity[1] > 0:
    #     coefficient = -1
    #     print('B')

    # beta = math.atan(coefficient * velocity_ratio)
    vertical_unit = [0, -1]
    # top = velocity[0] * vertical_unit[0] + velocity[1] * vertical_unit[1]
    # bottom = (velocity[0]**2 + velocity[1]**2)**.5 + (vertical_unit[0]**2 + vertical_unit[1]**2)**.5
    # beta = math.acos(top / bottom)
    beta = math.acos(-velocity[1] / (velocity[0]**2 + velocity[1]**2)**.5)
    if velocity[0] > 0:
        beta = 2*math.pi - beta
    print(velocity[0], '\t',  velocity[1], '\t', beta)
    angle_sep = theta - beta

    v_lat = math.sin(angle_sep) * speed
    v_long = math.cos(angle_sep) * speed
    """print((int)(velocity[0]*10)/10, '\t', (int)(velocity[1]*1000)/1000,
          "\t", (int)(theta*10)/10, '\t', (int)(omega*10)/10,
          '\t', (int)(beta*10)/10, '\t', (int)(angle_sep*10)/10)"""
    if speed < 1:
        angle[1] = 0
        slip_angle_f = 0
        slip_angle_r = 0
    else:
        slip_angle_f = steering - math.atan((a * omega + v_lat)/v_long)
        slip_angle_r = math.atan((b * omega + v_lat)/v_long)

        if slip_angle_f > max_slip_angle:
            slip_angle_f = max_slip_angle
        elif slip_angle_f < -max_slip_angle:
            slip_angle_f = -max_slip_angle

        if slip_angle_r > max_slip_angle:
            slip_angle_r = max_slip_angle
        elif slip_angle_r < -max_slip_angle:
            slip_angle_r = -max_slip_angle

    F_drag = -C_drag * speed * direction
    F_rolling = -C_rolling * speed * direction

    F_l_front = C_cornering * slip_angle_f
    F_l_rear = C_cornering * slip_angle_r

    F_long_wheels = -1 * math.sin(steering) * F_l_front
    F_lat_wheels = math.cos(steering) * F_l_front + F_l_rear

    F_long = F_traction + F_drag + F_rolling + F_long_wheels
    F_lat = F_lat_wheels

    F_x = math.sin(theta) * F_long + math.cos(theta) * F_lat
    F_y = math.cos(theta) * F_long - math.sin(theta) * F_lat

    Net_Torque = F_l_front * a - F_l_rear * b
    # print(F_l_front, ':', F_l_rear, "=", Net_Torque)

    return calc_change(position, velocity, angle, dt, mass, moment, [F_x, F_y],
                       Net_Torque)


def calc_change(position, velocity, angle, dt, mass, moment, F_net, T_net):
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

    theta = angle[0]
    omega = angle[1]
    [x, vx] = integrate(F_x, mass, x, vx, dt)
    [y, vy] = integrate(F_y, mass, y, vy, dt)
    [theta, omega] = integrate(T_net, moment, theta, omega, dt)
    position = [x, y]
    velocity = [vx, vy]
    angle = [theta, omega]
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
