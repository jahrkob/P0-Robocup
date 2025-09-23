#!/usr/bin/env pybricks-micropython
from hub import light_matrix, motion_sensor
from hub import port
import runloop
import motor_pair
import motor
import color_sensor
from hub import port
import color
import time
import distance_sensor

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

checkpoint = 6

"""----------------------------------------
------------ FUNCTION SECTION -------------
----------------------------------------"""
# Makes sure the claw is closed
motor.run(port.A,-100)

# Turn via motion sensor
def until(z,x):
    while motion_sensor.tilt_angles()[0] not in range(x,x+50):
        motor_pair.move(motor_pair.PAIR_1,-z,velocity=-400)

# Arm squeeze function
async def arm_squeeze():
    while True:
        motor.run(port.A,-200)
        await runloop.sleep_ms(3000)
        return False

# Drive without line function
def drive_no_line():
    """ Vi skal tilføje koden her """
    pass

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
            global checkpoint
            checkpoint += 1
            await run_cp(checkpoint)

"""----------------------------------------
----------- CHECKPOINT SECTION ------------
----------------------------------------"""
# Start Course
async def cp0():
    return

# Checkpoint 1(...)
async def cp1():
    motor_pair.move(motor_pair.PAIR_1,-10,velocity=-600)
    await runloop.sleep_ms(200)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while 70 < reflectionD and 70 < reflectionC:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,-7,velocity=-600)
    else:
        return

# Checkpoint 2(...)
async def cp2():
    motor_pair.move(motor_pair.PAIR_1,5,velocity=-600)
    await runloop.sleep_ms(200)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)

    while 70 < reflectionD and 70 < reflectionC:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,5,velocity=-600)
        reflectionD = color_sensor.reflection(port.D)
    else:
        return

# Checkpoint 3(...)
async def cp3():
    motion_sensor.reset_yaw(0)
    until(25,-600)
    motor.run(port.A,200)

    reflectionD = color_sensor.reflection(port.D)
    while reflectionD > 70:
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,300,0,velocity=-300)

    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while color_sensor.color(port.C) or color_sensor.color(port.D)!= color.BLACK:
        color_sensor.color(port.C)
        color_sensor.color(port.D)
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        if color_sensor.color(port.C) and color_sensor.color(port.D) is color.BLUE:
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
    until(-100,300)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)

    while reflectionC > 70 and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,0,velocity=-600)
    else:
        return

# Checkpoint 4(...)
async def cp4():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-400,acceleration=500)
    until(-100,700)
    motor_pair.stop(motor_pair.PAIR_1)
    return

# Checkpoint 5(...)
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
            until(-50,300)
            return

# Checkpoint 6(...)
async def cp6():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-500)
    until(-5,270)
    return

# Checkpoint 7(...)
async def cp7():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-400,acceleration=500)
    until(-100,400)
    return

# Checkpoint 8(...)
async def cp8():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,1300,0,velocity=-400,acceleration=500)
    until(-20,250)
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
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-1200,0,velocity=-300)
    motor_pair.stop(motor_pair.PAIR_1)
    motor.run(port.A,200)
    await runloop.sleep_ms(500)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-1000,0,velocity=-500)
    motor.run(port.A,-200)
    
    until(-60,1500)

    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while reflectionC > 70 and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-400,acceleration=500)

    motor_pair.move_for_degrees(motor_pair.PAIR_1,200,0,velocity=-500)
    await runloop.sleep_ms(1000)
    until(100,400)
    return

# Checkpoint 9(...)
async def cp9():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,100,-100,velocity=-500, acceleration=500)
    await runloop.sleep_ms(700)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while reflectionC > 70 and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,10,velocity=-500, acceleration=500)
    return

# Checkpoint 10(...)
async def cp10():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,1000,0,velocity=-500, acceleration=500)
    await runloop.sleep_ms(2000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,100,100,velocity=-200, acceleration=500)
    await runloop.sleep_ms(2000)

    afstand = distance_sensor.distance(port.B)
    while afstand >= 255 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500)

    motor_pair.move_for_degrees(motor_pair.PAIR_1,150,-100,velocity=-200,acceleration=500)
    await runloop.sleep_ms(2000)

    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while reflectionC > 70 and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,2,velocity=-500, acceleration=500)

    return

# Checkpoint 11(...)
async def cp11():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,140,-100,velocity=-500, acceleration=500)
    await runloop.sleep_ms(900)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while reflectionC > 70 and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,10,velocity=-500, acceleration=500)
    return


# Checkpoint 12(...)
async def cp12():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,100,54,velocity=-500, acceleration=500)
    await runloop.sleep_ms(500)
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
    quit

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