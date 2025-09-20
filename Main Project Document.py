# !/usr/bin/env micropython
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

motor.run(port.A,-100)

checkpoint = 8

"""----------------------------------------
------------ FUNCTION SECTION -------------
----------------------------------------"""

# Arm squeeze function
async def arm_squeeze():
    while True:
        motor.run(port.A,-200)
        await runloop.sleep_ms(3000)
        return False

# Drive without line function
async def drive_no_line():
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
            checkpoint += 1
            await run_cp(checkpoint)

"""----------------------------------------
----------- CHECKPOINT SECTION ------------
----------------------------------------"""
# Start Course
async def cp0():
    return

# Checkpoint 1  (...)
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

# Checkpoint 2  (...)
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

# Checkpoint 3  (...)
async def cp3():
    motor_pair.stop(motor_pair.PAIR_1)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,300,-25,velocity=-400,acceleration=500)
    motor.run(port.A,200)
    await runloop.sleep_ms(500)
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
            motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-500)
            await runloop.sleep_ms(1000)
            break
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-400)
        elif 30 < reflectionD < 70:
            motor_pair.move(motor_pair.PAIR_1,35,velocity=-400)
        elif 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,-35,velocity=-400)
    motor_pair.stop(motor_pair.PAIR_1)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,-1000,0,velocity=-400)
    await runloop.sleep_ms(1500)
    motor.run(port.A,-200)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,400,90,velocity=-400)
    await runloop.sleep_ms(1000)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)

    while reflectionC > 70 and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,0,velocity=-600)
    else:
        return

# Checkpoint 4  (...)
async def cp4():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-400,acceleration=500)
    await runloop.sleep_ms(1000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-400,acceleration=500)
    await runloop.sleep_ms(1000)
    return

# Checkpoint 5  (...)
async def cp5():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,1000,0,velocity=-700)
    await runloop.sleep_ms(1500)
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
            motor_pair.move_for_degrees(motor_pair.PAIR_1,1700,0,velocity=-500)
            await runloop.sleep_ms(2000)
            motor_pair.move_for_degrees(motor_pair.PAIR_1,400,50,velocity=-500)
            await runloop.sleep_ms(1000)
            return

# Checkpoint 6  (...)
async def cp6():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-500)
    await runloop.sleep_ms(1000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,800,20,velocity=-500)
    await runloop.sleep_ms(1000)

    return

# Checkpoint 7  (...)
async def cp7():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-400,acceleration=500)
    await runloop.sleep_ms(1000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-400,acceleration=500)
    await runloop.sleep_ms(1000)

# Checkpoint 8  (...)
async def cp8():
    motor_pair.move_for_degrees(motor_pair.PAIR_1,2000,0,velocity=-400,acceleration=500)
    await runloop.sleep_ms(3000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,350,18,velocity=-300)
    await runloop.sleep_ms(2000)
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
    motor.run(port.A, -200)
    await runloop.sleep_ms(500)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,-1300,0,velocity=-300)
    await runloop.sleep_ms(3500)
    motor_pair.stop
    await runloop.sleep_ms(1500)
    motor.run(port.A,200)
    await runloop.sleep_ms(1000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,-500,0,velocity=-500)
    motor.run(port.A,-200)
    await runloop.sleep_ms(1000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,600,60,velocity=-500)
    await runloop.sleep_ms(1000)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while reflectionC and reflectionD > 70:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-400,acceleration=500)
    
    motor_pair.move_for_degrees(motor_pair.PAIR_1,200,0,velocity=-500)
    await runloop.sleep_ms(1000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-500)
    await runloop.sleep_ms(1000)
    return

# Checkpoint 9  (...)
async def cp9():
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
        
"""----------------------------------------
------------ MAIN RUN SECTION -------------
----------------------------------------"""
def run_cp():
    global checkpoint
    if checkpoint == 0:
        cp0()
    elif checkpoint == 1:
        cp1()
    elif checkpoint == 2:
        cp2()
    elif checkpoint == 3:
        cp3()
    elif checkpoint == 4:
        cp4()
    elif checkpoint == 5:
        cp5()
    elif checkpoint == 6:
        cp6()
    elif checkpoint == 7:
        cp7()
    elif checkpoint == 8:
        cp8()
    elif checkpoint == 9:
        cp9()
    """
    elif checkpoint == 10:
        cp10()
    elif checkpoint == 11:
        cp11()
    elif checkpoint == 12:
        cp12()
    elif checkpoint == 13:
        cp13()
    """

"""----------------------------------------
-------------- TEST SECTION ---------------
----------------------------------------"""
runloop.run(follow_line())