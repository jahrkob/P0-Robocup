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
black = 7

async def main():
    global black
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
    if black == 4:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)


        return
    if black == 5:
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


    if black == 6:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-500)
        await runloop.sleep_ms(1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,1500,20,velocity=-600)
        await runloop.sleep_ms(1000)
        return

    if black == 7:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)

    if black == 8:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,2400,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(3000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,50,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)
        motor.run(port.A,200)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,1500,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(2000)
        while True:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor.run(port.A,-200)
            if color_sensor.color(port.C) or color_sensor.color(port.D) is color.BLUE:
                motor_pair.move_for_degrees(motor_pair.PAIR_1,-1100,0,velocity=-500)
                await runloop.sleep_ms(2500)
                motor_pair.stop
                await runloop.sleep_ms(500)
                motor.run(port.A,200)
                await runloop.sleep_ms(1000)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,-500,0,velocity=-500)
                motor.run(port.A,-200)
                await runloop.sleep_ms(1000)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,-1000,100,velocity=-500)
                await runloop.sleep_ms(1200)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,1500,0,velocity=-400,acceleration=500)
                await runloop.sleep_ms(5000)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-400,acceleration=500)
                await runloop.sleep_ms(1000)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,1000,0,velocity=-400,acceleration=500)
                await runloop.sleep_ms(1000)


      
                return


        motor_pair.stop(motor_pair.PAIR_1)


runloop.run(main())





#fuck

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
black = 7

async def klemme():
    while True:
        motor.run(port.A,-200)
        await runloop.sleep_ms(3000)
        return False


async def main():
    global black
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
    if black == 4:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)


        return
    if black == 5:
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


    if black == 6:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-500)
        await runloop.sleep_ms(1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,1500,20,velocity=-600)
        await runloop.sleep_ms(1000)
        return

    if black == 7:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,200,100,velocity=-400,acceleration=500)
        await runloop.sleep_ms(1000)

    if black == 8:
        motor_pair.move_for_degrees(motor_pair.PAIR_1,2200,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(3000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,350,20,velocity=-400,acceleration=200)
        await runloop.sleep_ms(2000)
        motor.run(port.A,200)
        motor_pair.move_for_degrees(motor_pair.PAIR_1,1500,0,velocity=-400,acceleration=500)
        await runloop.sleep_ms(2000)
        while True:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor.run(port.A,-500)
            if color_sensor.color(port.C) or color_sensor.color(port.D) is color.BLUE:
                motor_pair.move_for_degrees(motor_pair.PAIR_1,-1300,0,velocity=-500)
                await runloop.sleep_ms(2500)
                motor_pair.stop
                await runloop.sleep_ms(500)
                motor.run_for_time(port.A,duration=1000,velocity=200)
                await runloop.sleep_ms(1000)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,-500,0,velocity=-500)
                motor.run(port.A,-200)
                await runloop.sleep_ms(1000)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,1100,100,velocity=-500)
                await runloop.sleep_ms(1200)
                motor_pair.move_for_degrees(motor_pair.PAIR_1,1500,0,velocity=-400,acceleration=500)
                await runloop.sleep_ms(6000)



      
                return


        motor_pair.stop(motor_pair.PAIR_1)


runloop.run(main())

