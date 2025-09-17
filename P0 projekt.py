# LEGO slot:1 autostart
from hub import light_matrix
from hub import port
import runloop
import motor_pair
import motor
import color_sensor
from hub import port
import color

"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""

reflectionC = color_sensor.reflection(port.C)
reflectionD = color_sensor.reflection(port.D)

#motor.run_for_degrees(port.E,grader,hastighed) armen

black = 0

async def main():
    global black
    go = True
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)
    while go:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)

        if 30 < reflectionD < 80 and 30 < reflectionC < 80:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=300)
        elif 30 < reflectionD < 80:
            motor.run(port.E,-200)
            motor.run(port.F,100)
        elif 30 < reflectionC < 80:
            motor.run(port.E,-100)
            motor.run(port.F,200)
        elif 30 > reflectionD or 30 > reflectionC:
            black += 1
            black_1(black)
            break 

def black_1(black):
    print("black")
    if black == 1:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        while reflectionD >= 80 and reflectionC >= 80:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor.run(port.E,0)
            motor.run(port.F,0)
        else:
            runloop.run(main())
        return False
            
runloop.run(main())

"""
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
runloop.run(counter())
runloop.run(main())
"""





















#Martins test section
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
        if 30 < reflectionD < 80 and 30 < reflectionC < 80:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=300)
        elif 30 < reflectionD < 80:
            motor.run(port.E,-200)
            motor.run(port.F,100)
        elif 30 < reflectionC < 80:
            motor.run(port.E,-100)
            motor.run(port.F,200)
        elif 30 > reflectionD or 30 > reflectionC:
            black += 1
            await black_1(black)

async def black_1(black):
    if black == 1:
        motor_pair.move(motor_pair.PAIR_1,0,velocity=300)
        time.sleep(0.4)
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        while 80 < reflectionD and 80 < reflectionC:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor.run(port.E,-250)
            motor.run(port.F,150)
            reflectionD = color_sensor.reflection(port.D)
        else:
            print("fuck")
            motor_pair.stop(motor_pair.PAIR_1)
            motor.stop(port.E)
            motor.run(port.F,250)
            time.sleep(1)
            return

runloop.run(main())

"""
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
"""
