from hub import port
import runloop
import motor_pair
import distance_sensor

import motor
from hub import port, light_matrix

"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""

motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

distance_sensor.distance(port.B)

async def klo():
    light_matrix.write("Klo")

    # Åbn kloen
    await motor.run_for_degrees(port.A, 180, 360)
    await runloop.sleep_ms(1000)

    # Luk kloen
    await motor.run_for_degrees(port.A, -180, 360)

    # "Klem hårdt": kør lidt ekstra ind i lukkeretningen
    # Dette skaber et konstant tryk
    while True:
        await motor.run_for_degrees(port.A, -10, 200)# små "ryk" for at holde presset
        await runloop.sleep_ms(200)

async def black_2():
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=280)
    await runloop.sleep_ms(2000)
    motor_pair.move_for_degrees(motor_pair.PAIR_1, 90, 0)
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=280)
    motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, 0)
    if distance_sensor.distance(port.B) is not -1 and distance_sensor.distance(port.B) <= 170:
        runloop.run(klo())
