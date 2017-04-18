"""
@Author Alex Chapman
3.27.17

Second iteration physics for bicycle-type vehicle

"""
import math


def update_physics(position, velocity, angle, steering, F_traction, mass,
                   moment, dt):
    """
    Function: Takes state variables and wheel forces and returns updated
              positions and velocities.

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
    L = 4  # Wheelbase in meters

    # a is distance from front wheel to center of gravity
    # b is distance from rear wheel
    a = 1/4
    b = 1 - a
    a = a*L
    b = b*L

    # renaming to clarify
    theta = angle[0]
    omega = angle[1]

    # Initialize all constant values: some are experimental numbers
    max_slip_angle = math.radians(20)

    # Physical Coefficients
    C_cornering = 4000
    C_drag = 0.45
    C_rolling = 30 * C_drag

    # Scalar Speed term
    speed = (velocity[0]**2 + velocity[1]**2)**.5

    # Unit vector in direction of car
    car_vector = [math.sin(theta), math.cos(theta)]

    # Comes up with signed coefficient for which direction the car is moving
    direction = velocity[0] * car_vector[0] + velocity[1] * car_vector[1]
    if not direction == 0:  # catch divide by zero errors
        direction = direction / abs(direction)

    if velocity[1] == 0:  # Catch divide by zero errors
        velocity[1] = .001

    # Angle of seperation between the vertical unit vector [0, -1] and the
    # velocity vector [v_x, v_y]
    beta = math.acos(-velocity[1] / (velocity[0]**2 + velocity[1]**2)**.5)
    # Case that catches the acos innaccuracies in the third and fourth quads.
    if velocity[0] > 0:
        beta = 2*math.pi - beta

    if speed < 5:
        base_speed = 5  # m/s
        velocity[0] = -base_speed * car_vector[0]
        velocity[1] = -base_speed * car_vector[1]
        steering = -steering
        # beta = 0
        # print(velocity[0], velocity[1])

    # speedometer print statement
    speed_mph = (int)(2.23694 * speed * 100) / 100
    # print(speed_mph, 'mph', end="\r")

    # Defines the difference between car's orientation and direction of travel
    angle_sep = theta - beta

    # Velocity in the car's frame of reference: longitudinal is forward / back
    # lateral is right / left. Forward and Right are positive, respectively.
    v_lat = math.sin(angle_sep) * speed
    v_long = math.cos(angle_sep) * speed

    # Below 1 m/s truncates angle calculations so as to reduce sign changes.
    if speed < .1:
        angle[1] = 0
        slip_angle_f = 0
        slip_angle_r = 0
    else:
        # Slip angle for front and rear tires
        slip_angle_f = steering - math.atan((a * omega + v_lat)/v_long)
        slip_angle_r = math.atan((b * omega + v_lat)/v_long)

        # Truncates force to that of maximum slip angle, immitating real func.
        if slip_angle_f > max_slip_angle:
            slip_angle_f = max_slip_angle
        elif slip_angle_f < -max_slip_angle:
            slip_angle_f = -max_slip_angle

        if slip_angle_r > max_slip_angle:
            slip_angle_r = max_slip_angle
        elif slip_angle_r < -max_slip_angle:
            slip_angle_r = -max_slip_angle

    # Calculate Forces
    F_drag = -C_drag * speed * direction
    F_rolling = -C_rolling * speed * direction

    F_l_front = C_cornering * slip_angle_f
    F_l_rear = C_cornering * slip_angle_r

    F_long_wheels = -1 * math.sin(steering) * F_l_front
    F_lat_wheels = math.cos(steering) * F_l_front + F_l_rear

    # Sum longitudinal and lateral forces
    F_long = F_traction + F_drag + F_rolling - F_long_wheels
    F_lat = F_lat_wheels

    # Translate lat and long forces into real-world x-y plane
    F_x = math.sin(theta) * F_long + math.cos(theta) * F_lat
    F_y = math.cos(theta) * F_long - math.sin(theta) * F_lat

    # Calculate Net Torque
    Net_Torque = F_l_front * a - F_l_rear * b

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
