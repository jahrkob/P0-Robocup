from hub import port, light_matrix
import runloop
import motor_pair
import motor
import color_sensor
import distance_sensor
import color
import time

"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""

# Par de to små motorer
motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

# Globale tilstande
black = 0

async def klo():
    light_matrix.write("Klo")

    # Åbn kloen
    await motor.run_for_degrees(port.A, 180, 360)
    await runloop.sleep_ms(1000)

    # Luk kloen
    await motor.run_for_degrees(port.A, -180, 360)

    # Hold tryk med små "ryk"
    while True:
        await motor.run_for_degrees(port.A, -10, 200)
        await runloop.sleep_ms(200)

async def black_line_counter():
    global black
    if black == 1:
        # Kør lidt frem
        motor_pair.move(motor_pair.PAIR_1, 20, velocity=300)

        # Drej/ret indtil begge sensorer ser "lys" (over ~60)
        while True:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            if 60 < reflectionD and 60 < reflectionC:
                motor.run(port.E, -250)
                motor.run(port.F, 200)
            else:
                break

    elif black == 2:
        # --- black_2 ---
        motor_pair.move(motor_pair.PAIR_1, 0, velocity=280)
        await runloop.sleep_ms(2000)
        # VIGTIGT: giv grader OG hastighed
        motor_pair.move_for_degrees(motor_pair.PAIR_1, 90, 360)
        motor_pair.move(motor_pair.PAIR_1, 0, velocity=280)
        motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, 360)

        dist = distance_sensor.distance(port.B)
        if dist != -1 and dist <= 170:
            await klo()

async def main():
    global black
    go = True
    while go:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)

        if 30 < reflectionD < 80 and 30 < reflectionC < 80:
            motor_pair.move(motor_pair.PAIR_1, 0, velocity=300)
        elif 30 < reflectionD < 80:
            motor.run(port.E, -200)
            motor.run(port.F, 100)
        elif 30 < reflectionC < 80:
            motor.run(port.E, -100)
            motor.run(port.F, 200)
        elif reflectionD < 30 or reflectionC < 30:
            black = 2
            await black_line_counter()

runloop.run(main())
