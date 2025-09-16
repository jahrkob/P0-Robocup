# LEGO slot:1 autostart
from hub import light_matrix
from hub import port
import runloop
import motor_pair
import motor
import color_sensor
from hub import port
import color

#testing

"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""

reflectionC = color_sensor.reflection(port.C)
reflectionD = color_sensor.reflection(port.D)

#motor.run_for_degrees(port.E,grader,hastighed) armen

async def main():
    global black
    go = True
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)
    while go:
        reflectionC = color_sensor.reflection(port.C)
        print("C")
        print(reflectionC)
        reflectionD = color_sensor.reflection(port.D)
        print("D")
        print(reflectionD)

        if  40 < reflectionD < 80 and 40 < reflectionC < 80:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=300)
        elif 40 < reflectionD < 80:
            motor.run(port.E,-200)
            motor.run(port.F,100)
        elif 40 < reflectionC < 80:
            motor.run(port.E,-100)
            motor.run(port.F,200)
        elif 40 > reflectionD or 40 > reflectionC:
            black += 1

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
