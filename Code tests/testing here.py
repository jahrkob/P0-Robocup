from hub import port, light_matrix
import runloop
import motor_pair
import motor
import color_sensor
import distance_sensor

"""
Port E og F er de 2 små motorer
Port A er den store motor
Port C og D er farvesensorer (C er den venstre farvesensor)
Port B er afstandssensor
"""

# Par de to små motorer
motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

# --- Kalibrering (justér disse værdier til din robot) ---
TURN_90_WHEEL_DEG   = 420   # hjulgrader for ca. 90° højredrej (steering=+100)
TURN_180_WHEEL_DEG  = 2 * TURN_90_WHEEL_DEG
BUMP_FORWARD_DEG    = 180   # “en lille smule” ligeud
DRIVE_VELOCITY      = 280
TURN_VELOCITY       = 220
CATCH_DISTANCE_MM   = 170   # afstand hvor kloen skal aktiveres

black = 0

async def klo():
    light_matrix.write("Klo")

    # Åbn kloen
    await motor.run_for_degrees(port.A, 180, 360)
    await runloop.sleep_ms(1000)

    # Luk kloen
    await motor.run_for_degrees(port.A, -180, 360)

    # Hold tryk med små "ryk" (uendelig)
    while True:
        await motor.run_for_degrees(port.A, -10, 200)
        await runloop.sleep_ms(200)

# --- Hjælpefunktioner til manøvrer ---
def turn_right_90():
    # Fuld højrestyring, drej i ca. 90° (tunet via TURN_90_WHEEL_DEG)
    motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, TURN_90_WHEEL_DEG, velocity=TURN_VELOCITY)

def turn_around_180():
    motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, TURN_180_WHEEL_DEG, velocity=TURN_VELOCITY)

def forward_small():
    motor_pair.move_for_degrees(motor_pair.PAIR_1, 0, BUMP_FORWARD_DEG, velocity=DRIVE_VELOCITY)

async def drive_forward_until_object(threshold_mm=CATCH_DISTANCE_MM):
    # Kør frem og tjek afstand løbende
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=DRIVE_VELOCITY)
    while True:
        d = distance_sensor.distance(port.B)
        if d != -1 and d <= threshold_mm:
            # Stop E/F før vi griber
            motor.stop(port.E)
            motor.stop(port.F)
            return
        await runloop.sleep_ms(20)

async def black_line_counter():
    global black
    if black == 1:
        # Din oprindelige 1. sort-linje-adfærd (uændret)
        motor_pair.move(motor_pair.PAIR_1, 20, velocity=300)
        while True:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            if 60 < reflectionD and 60 < reflectionC:
                motor.run(port.E, -250)
                motor.run(port.F, 200)
            else:
                break

    elif black == 2:
        # === Det du bad om ===
        turn_right_90()                 # 1) Drej 90° til højre
        forward_small()                 # 2) Kør en lille smule frem
        turn_around_180()               # 3) Vend 180°
        await drive_forward_until_object()  # 4) Kør frem til objekt registreres
        await klo()                     # 5) Grib med kloen (bliver i “klem”-loop)

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
            # Hvis du vil ramme black==2 specifikt, kan du:
            #   a) tælle op (black += 1) ELLER
            #   b) springe direkte til 2 (black = 2)
            # Her tæller vi op, så både 1. og 2. sortlinje kan bruges.
            black = 2
            await black_line_counter()

runloop.run(main())
