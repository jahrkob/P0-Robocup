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

reflectionC = color_sensor.reflection(port.C)
reflectionD = color_sensor.reflection(port.D)

motor.run(port.A,-100)
black = 0

async def main():
    global black
    while True:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-650)
        elif 30 < reflectionD < 70:
            motor_pair.move(motor_pair.PAIR_1,15,velocity=-500)
        elif 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,-15,velocity=-500)
        elif 30 > reflectionD or 30 > reflectionC:
            black += 1
            await black_line_counter(black)

async def black_line_counter(black):
    if black == 1:
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
    if black == 2:
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
    if black == 3:
        await runloop.sleep_ms(200)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,400,-40,velocity=-300)
        await runloop.sleep_ms(500)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-300)
        await runloop.sleep_ms(500)
        motor.run(port.A,200)
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        while reflectionC > 30 and reflectionD > 30:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-650)
        elif 30 < reflectionD < 70:
            motor_pair.move(motor_pair.PAIR_1,15,velocity=-500)
        elif 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,-15,velocity=-500)
        motor_pair.stop(motor_pair.PAIR_1)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,-400,0,velocity=-500)
        await runloop.sleep_ms(1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,400,-100,velocity=-500)
        return
    if black == 4:
        return

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

runloop.run(main())

