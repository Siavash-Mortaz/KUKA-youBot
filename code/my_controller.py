from controller import Robot, DistanceSensor, Motor, Camera
import math
# time in [ms] of a simulation step
timestep = 64

max_speed = 3
pickFlag = 0
greenFlag = 0
color_name = ''
BoxDetec = 0
TableDetect = 0
type = ''
objectID = 0

# create the Robot instance.
robot = Robot()

# initialize devices


c = robot.getDevice('camera')
c.enable(timestep)
c.recognitionEnable(timestep)
camera_width = c.getWidth()
# Inizialize base motors.
wheels = []
whNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getDevice(whNames[i]))


for wheel in wheels:
    # Activate controlling the motors setting the velocity.
    # Otherwise by default the motor expects to be controlled in force or position,
    # and setVelocity will set the maximum motor velocity instead of the target velocity.
    wheel.setPosition(float('+inf'))


# Initialize arm motors.

armMotors = []
arNames = ['arm1', 'arm2', 'arm3', 'arm4', 'arm5']

for i in range(5):
    armMotors.append(robot.getDevice(arNames[i]))

# Set the maximum motor velocity.
armMotors[0].setVelocity(0.2)
armMotors[1].setVelocity(0.5)
armMotors[2].setVelocity(0.5)
armMotors[3].setVelocity(0.3)
# Initialize arm position sensors.
# These sensors can be used to get the current joint position and monitor the joint movements.
armPositionSensors = []
arpNames = ['arm1sensor', 'arm2sensor',
            'arm3sensor', 'arm4sensor', 'arm5sensor']

for i in range(5):
    armPositionSensors.append(robot.getDevice(arpNames[i]))
    armPositionSensors[i].enable(timestep)


# Initialize gripper motors.
finger = robot.getDevice("finger::left")
# Set the maximum motor velocity.
finger.setVelocity(0.03)
# Read the miminum and maximum position of the gripper motors.
fingerMinPosition = finger.getMinPosition()
fingerMaxPosition = finger.getMaxPosition()

for wheel in wheels:
    wheel.setVelocity(0.0)

# firstObject = c.getRecognitionObjects()[0]
# id = firstObject.getId()


# *********************************Moving Functions*****************
# MOVE_FORWARD Function
def move_forward(wheels, speed):

    for wheel in wheels:
        wheel.setVelocity(speed)
# MOVE_LEFT Function


def move_left(wheels, x, speed):
    wheels[0].setVelocity(x * speed)
    wheels[1].setVelocity(-x*speed)
    wheels[2].setVelocity(x * speed)
    wheels[3].setVelocity(-x*speed)
# MOVE_RIGHT Function


def move_right(wheels, x, speed):
    wheels[0].setVelocity(-x*speed)
    wheels[1].setVelocity(x*speed)
    wheels[2].setVelocity(-x*speed)
    wheels[3].setVelocity(x*speed)

# Strafe_LEFT Function


def strafe_left(wheels, x, speed):
    wheels[0].setVelocity(x * speed)
    wheels[1].setVelocity(-x*speed)
    wheels[2].setVelocity(-x * speed)
    wheels[3].setVelocity(x*speed)
# Strafe_RIGHT Function


def strafe_right(wheels, x, speed):
    wheels[0].setVelocity(-x*speed)
    wheels[1].setVelocity(x*speed)
    wheels[2].setVelocity(x*speed)
    wheels[3].setVelocity(-x*speed)

# ******************Moving toward Object**************


def move_to_object(idx_object, threshold):
    object = objects[idx_object]
    reached = 0
    orient = 0
    position_on_image = object.getPositionOnImage()
    relative_position = object.getPosition()
    ori = object.getOrientation()
    print(position_on_image[0])
    print(f'id={object.getId()}')

    print(f'Orientation_1: {ori[0]}')
    print(f'Orientation_2: {ori[1]}')
    print(f'Orientation_3: {ori[2]}')

    if position_on_image[0] != camera_width / 2:
        # ... turn either left or right to center it
        if position_on_image[0] < camera_width / 2:
            print("Object is on the left, rotating left")
            move_left(wheels, 0.8, max_speed)
        elif position_on_image[0] > camera_width / 2:
            print("Object is on the right, rotating right")
            move_right(wheels, 0.8, max_speed)
    else:
        # Object is central. If it's distant, approach it
        if relative_position[0] > threshold:
            print("Object is frontal, advancing")
            move_forward(wheels, max_speed)

        else:
            print(round(relative_position[0], 2))
            print("Destination reached")
            move_forward(wheels, 0)
            orient = ori[1]
            print(f'orii: {orient}')
            reached = 1

    return reached, orient
# ****************************************************
# ***************Pick Up The Object ******************


def pick_up_object(ori):
    # Open gripper.
    ori = ori/0.02
    print(f'ecend Orii: {ori}')
    pick = 0
    finger.setPosition(fingerMaxPosition)
    armMotors[0].setPosition(0.02)
    armMotors[1].setPosition(-0.95)  # arm2(max=-1.13)
    armMotors[2].setPosition(-1.35)  # arm3(max=-2.64)
    armMotors[3].setPosition(-0.8)  # arm4(max=-1.78)
    # armMotors[4].setPosition(-0.4)  #arm4(max=-2.95)
    armMotors[4].setPosition(ori)  # arm4(max=-2.95)
    robot.step(100 * timestep)
    finger.setPosition(0.010)
    robot.step(50 * timestep)
    armMotors[0].setPosition(2.94)
    armMotors[1].setPosition(0)
    robot.step(20 * timestep)
    pick = 1
    return pick
# **********************************************************
# ************************Put Down the Object *****************


def put_down_object():
    armMotors[0].setPosition(-0.01)
    armMotors[1].setPosition(-0.5)  # arm2(-1.13,1.57)
    armMotors[2].setPosition(0.0)  # arm3(-2.64,2.55)
    armMotors[3].setPosition(-1.78)  # arm4(-1.78,1.78)
    robot.step(300 * timestep)
    finger.setPosition(fingerMaxPosition)
    robot.step(50 * timestep)
    armMotors[0].setPosition(0.0)
    armMotors[1].setPosition(0.0)  # arm2(-1.13,1.57)
    armMotors[2].setPosition(0.0)  # arm3(-2.64,2.55)
    armMotors[3].setPosition(0.0)  # arm4(-1.78,1.78)
    putdown = 0
    return putdown


# ******************************************************
# **********************Detect BOXES*****************
def detect_boxes(objects):
    b_detect = 0
    idx_object = 0
    color_code = 0
    for i in range(len(objects)):
        color = objects[i].getColors()
        if color[0] == 1 or color[1] == 1 or color[2] == 1:
            if color[0] == 1:
                color_code = 1
            elif color[1] == 1:
                color_code = 2
            elif color[2] == 1:
                color_code = 3
            b_detect = 1
            idx_object = i
            break
    return idx_object, b_detect, color_code

# *************************DETECT TABLE***************


def detect_tables(objects, color_code):
    t_detect = 0
    idx_object = 0
    for i in range(len(objects)):
        color = objects[i].getColors()
        if color[0] == 0.5:
            if color_code == 1:
                t_detect = 1
                idx_object = i
                print('Red Table!')
            break

        if color[1] == 0.5:
            if color_code == 2:
                t_detect = 1
                idx_object = i
                print('Green Table!')
            break

        if color[2] == 0.5:
            if color_code == 3:
                t_detect = 1
                idx_object = i
                print('Blue Table!')
            break
        # if color[0]==0.5 or color[1]==0.5 or color[2]==0.5:
        #     t_detect=1
        #     idx_object=i
        #     break
    return idx_object, t_detect


# ***********************************************************************


# feedback loop: step simulation until receiving an exit event
while robot.step(timestep) != -1:

    objects = c.getRecognitionObjects()

    # move_forward(wheels,max_speed)
    # for object in objects:
    #     print(object.getId())

    # move_right(wheels,0.8,max_speed)
    if len(objects) == 0:
        print("No object found. Searching...")
        move_right(wheels, 0.8, max_speed)
    else:
        if pickFlag == 0:

            print("object found.")
            # print(f'i={idx}')
            # print('1')
            idx, BoxDetec, color_id = detect_boxes(objects)
            # print('2')
            if BoxDetec == 1 and idx is not None:
                reach, ori = move_to_object(idx, 0.15)
                if reach == 1:
                    pickFlag = pick_up_object(ori)

                # print(f'Box ID[{i}]= {objects[i].getId()}')
            else:
                print('Not Box!')
                move_right(wheels, 0.8, max_speed)
        else:
            idx_t, TabDetect = detect_tables(objects, color_id)
            if TabDetect == 1 and idx_t is not None:
                print('The Table Found')
                reach_t, _ = move_to_object(idx_t, 0.2)
                if reach_t == 1:
                    pickFlag = put_down_object()
                # reach=move_to_object(idx,0.2)
                # if reach==1:
                #     pickFlag=pick_up_object()

                # print(f'Box ID[{i}]= {objects[i].getId()}')
            else:
                print('Not Table!')
                move_right(wheels, 0.8, max_speed)
