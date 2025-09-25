from hub import motion_sensor
from hub import port
import runloop
import motor_pair
import motor
import color_sensor
import color
import distance_sensor
import sys

# INITIALIZE VARIABLES AND MOTORS
"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""

"""----------------------------------------
------------ VARIABLE SECTION -------------
----------------------------------------"""
motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

reflectionC = color_sensor.reflection(port.C)
reflectionD = color_sensor.reflection(port.D)

checkpoint = 0

"""----------------------------------------
------------ FUNCTION SECTION -------------
----------------------------------------"""
# Makes sure the claw is closed
motor.run(port.A,-100)

# Turn via motion sensor
def until_gyro(stering,interval):
    while motion_sensor.tilt_angles()[0] not in range(interval,interval+50):
        motor_pair.move(motor_pair.PAIR_1,-stering,velocity=-300, acceleration=500)

# Drive without line function
def until_line(stering,speed):
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while 70 < reflectionD and 70 < reflectionC:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,-stering,velocity=-speed)
        
# Follow line function
async def follow_line():
    global checkpoint
    while True:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-500)
        elif 30 < reflectionD < 70:
            motor_pair.move(motor_pair.PAIR_1,15,velocity=-500)
        elif 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,-15,velocity=-500)
        elif 30 > reflectionD or 30 > reflectionC:
            checkpoint += 1
            await run_cp(checkpoint)

# The function used on the runway
def runway():
    afstand = distance_sensor.distance(port.B)
    while afstand >=1550 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500, acceleration=500)


"""----------------------------------------
----------- CHECKPOINT SECTION ------------
----------------------------------------"""
# Start Course
async def cp0():
    return

# Checkpoint 1 (Right turn)
async def cp1():
    motor_pair.move(motor_pair.PAIR_1,-10,velocity=-600)
    await runloop.sleep_ms(200)
    until_line(7,600)
    return

# Checkpoint 2 (Left turn)
async def cp2():
    motor_pair.move(motor_pair.PAIR_1,5,velocity=-600)
    await runloop.sleep_ms(200)
    until_line(-5,600)
    return

# Checkpoint 3 (Move first bottle)
async def cp3():
    motion_sensor.reset_yaw(0)
    until_gyro(100,-400)
    motor.run(port.A,200)

    until_line(0,300)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while (color_sensor.color(port.C) != color.BLACK) or (color_sensor.color(port.D) != color.BLACK):
        c_col = color_sensor.color(port.C)
        d_col = color_sensor.color(port.D)
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)

        if (c_col == color.BLUE) and (d_col == color.BLUE):
            await motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-500)
            break
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-400)
        elif 30 < reflectionD < 70:
            motor_pair.move(motor_pair.PAIR_1,35,velocity=-400)
        elif 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,-35,velocity=-400)

    motor_pair.stop(motor_pair.PAIR_1)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-600,0,velocity=-400)
    motor.run(port.A,-200)
    until_gyro(-100,300)
    until_line(0,600)

# Checkpoint 4 (Left turn to ramp)
async def cp4():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-400,acceleration=500)
    until_gyro(-100,700)
    motor_pair.stop(motor_pair.PAIR_1)
    return

# Checkpoint 5 (Ramp)
async def cp5():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,1000,0,velocity=-700)
    while True:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-500)
        elif 30 < reflectionD < 70:
            motor_pair.move(motor_pair.PAIR_1,15,velocity=-500)
        elif 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,-15,velocity=-500)
        else:
            await motor_pair.move_for_degrees(motor_pair.PAIR_1,1200,0,velocity=-500)
            until_gyro(-50,300)
            return

# Checkpoint 6 (Choose correct line)
async def cp6():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-500)
    until_gyro(-5,270)
    return

# Checkpoint 7 (Turn left to "bullseye")
async def cp7():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-400,acceleration=500)
    until_gyro(-100,400)
    return

# Checkpoint 8 (Bullseye)
async def cp8():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,1150,0,velocity=-400,acceleration=500)
    until_gyro(-20,250)
    motor.run(port.A,200)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)

    while True:
        if reflectionC > 30 and reflectionD > 30:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-400,acceleration=500)
        else:
            break

    motor.run(port.A,-200)
    await runloop.sleep_ms(500)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-1300,0,velocity=-300)
    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(500)
    motor.run(port.A,200)
    await runloop.sleep_ms(500)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-1000,0,velocity=-500)
    motor.run(port.A,-200)

    until_gyro(-60,1700)

    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    until_line(0,500)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1,200,0,velocity=-500)
    until_line(-100,300)
    return

# Checkpoint 9 (Drive around bottle 1)
async def cp9():
    motion_sensor.reset_yaw(0)
    until_gyro(100,-250)
    until_line(-10,500)

# Checkpoint 10 (Move between walls)
async def cp10():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,1000,0,velocity=-500, acceleration=500)

    until_gyro(-100,250)

    afstand = distance_sensor.distance(port.B)
    while afstand >= 255 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500)
        afstand = distance_sensor.distance(port.B)
    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(500)
    until_gyro(100,-130)
    until_line(-3,500)
    

# Checkpoint 11 (Drive around bottle 2)
async def cp11():
    motion_sensor.reset_yaw(0)
    until_gyro(100,-300)
    until_line(-10,500)

# Checkpoint 12 (Runway)
async def cp12():
    #until_gyro(-100,1700)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,200,21,velocity=-300, acceleration=500)
    afstand = distance_sensor.distance(port.B)
    while afstand >=1550 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500, acceleration=500)

    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(1000)

    afstand = distance_sensor.distance(port.B)
    while afstand >=1550 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500, acceleration=500)
    motor_pair.stop(motor_pair.PAIR_1)
    sys.exit()

"""----------------------------------------
------------ MAIN RUN SECTION -------------
----------------------------------------"""
async def run_cp(checkpoint):
    if checkpoint == 0:
        runloop.run(cp0())
    elif checkpoint == 1:
        runloop.run(cp1())
    elif checkpoint == 2:
        runloop.run(cp2())
    elif checkpoint == 3:
        runloop.run(cp3())
    elif checkpoint == 4:
        runloop.run(cp4())
    elif checkpoint == 5:
        runloop.run(cp5())
    elif checkpoint == 6:
        runloop.run(cp6())
    elif checkpoint == 7:
        runloop.run(cp7())
    elif checkpoint == 8:
        runloop.run(cp8())
    elif checkpoint == 9:
        runloop.run(cp9())
    elif checkpoint == 10:
        runloop.run(cp10())
    elif checkpoint == 11:
        runloop.run(cp11())
    elif checkpoint == 12:
        runloop.run(cp12())

"""----------------------------------------
-------------- TEST SECTION ---------------
----------------------------------------"""
runloop.run(follow_line())




"""
cp9

motor_pair.move_for_degrees(motor_pair.PAIR_1,100,-100,velocity=-500, acceleration=500)
    await runloop.sleep_ms(1000)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while reflectionC and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-400,acceleration=500)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,200,-100,velocity=-500, acceleration=500)
    await runloop.sleep_ms(1000)
    while reflectionC and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-400,acceleration=500)
    return
"""
