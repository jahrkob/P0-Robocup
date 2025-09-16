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
            global black
            black += 1
            await black_1()

async def black_1():
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    motor.run(port.E,-150)
    motor.run(port.F,200)
    while reflectionD >= 80 and reflectionC >= 80:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor.run(port.E,-100)
        motor.run(port.F,200)
    else:
        # runloop.run(main())
        return

runloop.run(main())

if black == 1:
    runloop.run(black_1())

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