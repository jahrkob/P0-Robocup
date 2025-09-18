from hub import light_matrix
from hub import port
import runloop
import motor_pair
import motor
import color_sensor
from hub import port
import color
import time

"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""


motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

reflectionC = color_sensor.reflection(port.C)
reflectionD = color_sensor.reflection(port.D)

black = 0

async def main():
    global black
    go = True
    while go:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-400)
        elif 30 < reflectionD < 70:
            motor.run(port.E,200)
            motor.run(port.F,-100)
        elif 30 < reflectionC < 70:
            motor.run(port.E,100)
            motor.run(port.F,-200)
        elif 30 > reflectionD or 30 > reflectionC:
            black += 1
            await black_line_counter(black)

async def black_line_counter(black):
    if black == 1:
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-1050)
        time.sleep(0.2)
        motor_pair.stop(motor_pair.PAIR_1)
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        while 70 < reflectionD and 70 < reflectionC:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor.run(port.E,150)
            motor.run(port.F,-250)
        else:
            return
    if black == 2:
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-1050)
        time.sleep(0.2)
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        while 70 < reflectionD and 70 < reflectionC:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor.run(port.E,350)
            motor.run(port.F,-300)
            reflectionD = color_sensor.reflection(port.D)
        else:
            return
    if black == 3:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        runloop.run(klo())
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,-30,velocity=-500)
        time.sleep(0.5)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,0,velocity=-500)
        time.sleep(0.5)
        while True:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            if 30 < reflectionD < 70 and 30 < reflectionC < 70:
                motor_pair.move(motor_pair.PAIR_1,0,velocity=-400)
            elif 30 < reflectionD < 70:
                motor.run(port.E,200)
                motor.run(port.F,-100)
            elif 30 < reflectionC < 70:
                motor.run(port.E,100)
                motor.run(port.F,-200)

async def klo():
    while True:
        afstand = distance_sensor.distance(port.B)
        print(afstand)
        if afstand is not -1 and afstand <= 170:
            while True:
                motor.run(port.A, -200)
        else:
            motor.run(port.A, 100)
        await runloop.sleep_ms(100)

runloop.run(klo())
runloop.run(main())



#huge fuck up
from hub import light_matrix
from hub import port
import runloop
import motor_pair
import motor
import color_sensor
from hub import port
import color
import time
import distance_sensor

"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""
motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

async def pis():
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)

        motor_pair.move_for_degrees(motor_pair.PAIR_1,550,0,velocity=-500)
        time.sleep(1)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,160,-100,velocity=-500)
        time.sleep(1)
        while True:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            afstand = distance_sensor.distance(port.B)
            if 30 < reflectionD < 70 and 30 < reflectionC < 70:
                motor_pair.move(motor_pair.PAIR_1,0,velocity=-400)
            elif afstand is not -1 and afstand <= 170:
                motor.run(port.A, -200)
            elif 30 < reflectionD < 70:
                motor.run(port.A, 100)
                motor.run(port.E,200)
                motor.run(port.F,-100)
            elif 30 < reflectionC < 70:
                motor.run(port.A, 100)
                motor.run(port.E,100)
                motor.run(port.F,-200)

runloop.run(pis())
