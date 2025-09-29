from hub import motion_sensor, sound, port
import runloop
import motor_pair
import motor
import color_sensor
import color
import distance_sensor
import sys

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

checkpoint = 0

"""----------------------------------------
------------- MUSIC SECTION ---------------
----------------------------------------"""
# Darth Vader Theme notes and durations
darth_notes = [
    392, 392, 392, 311, 466, 392, 311, 466, 392,
    587, 587, 587, 622, 466, 369, 311, 466, 392,
    784, 392, 392, 784, 739, 698, 659, 622, 659,
    415, 554, 523, 493, 466, 440, 466,          
    311, 369, 311, 466, 392, 311, 466, 392,     
    587, 587, 587, 622, 466, 369, 311, 466, 392,
    392, 311, 466, 392                            
]

darth_durations = [
    300, 150, 150, 150, 150, 150, 150, 150, 600,
    300, 150, 150, 150, 150, 150, 150, 150, 600,
    300, 150, 150, 300, 150, 150, 150, 150, 600,
    150, 150, 150, 150, 150, 150, 600,          
    150, 150, 150, 150, 150, 150, 150, 600,     
    300, 150, 150, 150, 150, 150, 150, 150, 900,
    600, 150, 150, 1200                           
]

# Super Mario Bros Main Theme
mario_notes = [
    659, 659, 0, 659, 0, 523, 659, 0, 784, 0, 392
]

mario_durations = [
    # Intro line
    200, 200, 100, 200, 100, 200, 300, 100, 350, 200, 300
]

async def song_start():
    # Play Mario theme once
    for i in range(len(mario_notes)):
        if mario_notes[i] > 0:# 0 represents rest/pause
            sound.beep(mario_notes[i], mario_durations[i])
        await runloop.sleep_ms(mario_durations[i])
runloop.run(song_start())

async def song():
    # Play Darth Vader's theme once
    for i in range(len(darth_notes)):
        sound.beep(darth_notes[i], darth_durations[i])
        await runloop.sleep_ms(darth_durations[i])

"""----------------------------------------
------------ FUNCTION SECTION -------------
----------------------------------------"""
# Makes sure the claw is closed
def claw(n):
    motor.run_for_degrees(port.A,n,200)

# Turn via motion sensor
def until_gyro(stering,interval,speed,acc=500):
    while motion_sensor.tilt_angles()[0] not in range(interval,interval+50):
        motor_pair.move(motor_pair.PAIR_1,-stering,velocity=-speed,acceleration=acc)

# Drive without line function
def until_line(stering,speed):
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while 70 < reflectionD and 70 < reflectionC:
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)
        motor_pair.move(motor_pair.PAIR_1,-stering,velocity=-speed)

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

# Checkpoint 1 (Right turn)
async def cp1():
    motor_pair.move(motor_pair.PAIR_1,-20,velocity=-600)
    await runloop.sleep_ms(200)
    until_line(7,600)
    return

# Checkpoint 2 (Left turn)
async def cp2():
    motor_pair.move(motor_pair.PAIR_1,5,velocity=-600)
    await runloop.sleep_ms(200)
    until_line(-5,600)
    return

# Checkpoint 3 (Move first bottle)
async def cp3():
    motion_sensor.reset_yaw(0)
    until_gyro(100,-400,300,500)
    
    claw(200)

    until_line(0,300)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while (color_sensor.color(port.C) != color.BLACK) or (color_sensor.color(port.D) != color.BLACK):
        c_col = color_sensor.color(port.C)
        d_col = color_sensor.color(port.D)
        reflectionC = color_sensor.reflection(port.C)
        reflectionD = color_sensor.reflection(port.D)

        if (c_col == color.BLUE) and (d_col == color.BLUE):
            await motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-500)
            break
        if 30 < reflectionD < 70 and 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-400)
        elif 30 < reflectionD < 70:
            motor_pair.move(motor_pair.PAIR_1,35,velocity=-400)
        elif 30 < reflectionC < 70:
            motor_pair.move(motor_pair.PAIR_1,-35,velocity=-400)

    motor_pair.stop(motor_pair.PAIR_1)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-600,0,velocity=-400)
    claw(-200)
    until_gyro(-100,300,300,500)
    until_line(0,600)

# Checkpoint 4 (Left turn to ramp)
async def cp4():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,500,0,velocity=-400,acceleration=500)
    until_gyro(-100,700,300,500)
    motor_pair.stop(motor_pair.PAIR_1)
    return

# Checkpoint 5 (Ramp)
async def cp5():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,1000,0,velocity=-700)
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
            await motor_pair.move_for_degrees(motor_pair.PAIR_1,1200,0,velocity=-500)
            until_gyro(-50,300,300,500)
            return

# Checkpoint 6 (Choose correct line)
async def cp6():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-500)
    until_gyro(-5,240,600,1000)
    return

# Checkpoint 7 (Turn left to "bullseye")
async def cp7():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,400,0,velocity=-400,acceleration=500)
    until_gyro(-100,400,300,500)
    return

# Checkpoint 8 (Bullseye)
async def cp8():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,1150,0,velocity=-400,acceleration=500)
    until_gyro(-20,250,300,500)
    claw(200)
    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    while True:
        if reflectionC > 30 and reflectionD > 30:
            reflectionC = color_sensor.reflection(port.C)
            reflectionD = color_sensor.reflection(port.D)
            motor_pair.move(motor_pair.PAIR_1,0,velocity=-200,acceleration=500)
        else:
            break

    claw(-200)
    await runloop.sleep_ms(1000)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-1300,0,velocity=-300)
    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(500)
    claw(200)
    await runloop.sleep_ms(1000)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,-1000,0,velocity=-500)
    claw(-200)
    
    until_gyro(-60,1700,300,500)

    reflectionC = color_sensor.reflection(port.C)
    reflectionD = color_sensor.reflection(port.D)
    until_line(0,500)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1,200,0,velocity=-500)
    until_line(-100,300)
    return

# Checkpoint 9 (Drive around bottle 1)
async def cp9():
    motion_sensor.reset_yaw(0)
    until_gyro(100,-250,300,500)
    until_line(-10,500)

# Checkpoint 10 (Move between walls)
async def cp10():
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,1000,0,velocity=-500, acceleration=500)

    until_gyro(-100,250,300,500)

    afstand = distance_sensor.distance(port.B)
    while afstand >= 255 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500)
        afstand = distance_sensor.distance(port.B)
    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(500)
    until_gyro(100,-130,300,500)
    until_line(-3,500)


# Checkpoint 11 (Drive around bottle 2)
async def cp11():
    motion_sensor.reset_yaw(0)
    until_gyro(100,-300,300,500)
    until_line(-10,500)

# Checkpoint 12 (Runway)
async def cp12():
    await motor_pair.move_for_degrees(motor_pair.PAIR_1,200,21,velocity=-300, acceleration=500)
    afstand = distance_sensor.distance(port.B)
    while afstand >=1550 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500, acceleration=500)

    motor_pair.stop(motor_pair.PAIR_1)
    await runloop.sleep_ms(1000)

    afstand = distance_sensor.distance(port.B)
    while afstand >=1550 or afstand == -1:
        afstand = distance_sensor.distance(port.B)
        motor_pair.move(motor_pair.PAIR_1,0,velocity=-500, acceleration=500)
    motor_pair.stop(motor_pair.PAIR_1)
    runloop.run(song())
    sys.exit()

"""----------------------------------------
------------ MAIN RUN SECTION -------------
----------------------------------------"""
async def run_cp(checkpoint):
    if checkpoint == 0:
        runloop.run(cp0())
    elif checkpoint == 1:
        runloop.run(cp1())
    elif checkpoint == 2:
        runloop.run(cp2())
    elif checkpoint == 3:
        runloop.run(cp3())
    elif checkpoint == 4:
        runloop.run(cp4())
    elif checkpoint == 5:
        runloop.run(cp5())
    elif checkpoint == 6:
        runloop.run(cp6())
    elif checkpoint == 7:
        runloop.run(cp7())
    elif checkpoint == 8:
        runloop.run(cp8())
    elif checkpoint == 9:
        runloop.run(cp9())
    elif checkpoint == 10:
        runloop.run(cp10())
    elif checkpoint == 11:
        runloop.run(cp11())
    elif checkpoint == 12:
        runloop.run(cp12())

"""----------------------------------------
-------------- TEST SECTION ---------------
----------------------------------------"""
runloop.run(follow_line())

"""
from hub import sound
import runloop

notes = {
    "C4": 261, "D4": 294, "E4": 329, "F4": 349,
    "G4": 392, "A4": 440, "B4": 494,
    "C5": 523, "D5": 587, "E5": 659, "F5": 698,
    "G5": 784, "A5": 880, "B5": 988,
}

durations = {
    "eighth": 200,
    "quarter": 400,
    "half": 800,
    "whole": 1600,
}

async def play_song(song):
    for note, length in song:
        if note == "REST":
            await runloop.sleep_ms(durations[length])# silence
        else:
            await sound.beep(notes[note], durations[length])
twinkle = [
    ("C4", "quarter"), ("C4", "quarter"), ("G4", "quarter"), ("G4", "quarter"),
    ("A4", "quarter"), ("A4", "quarter"), ("G4", "half"),

    ("F4", "quarter"), ("F4", "quarter"), ("E4", "quarter"), ("E4", "quarter"),
    ("D4", "quarter"), ("D4", "quarter"), ("C4", "half"),

    ("G4", "quarter"), ("G4", "quarter"), ("F4", "quarter"), ("F4", "quarter"),
    ("E4", "quarter"), ("E4", "quarter"), ("D4", "half"),

    ("G4", "quarter"), ("G4", "quarter"), ("F4", "quarter"), ("F4", "quarter"),
    ("E4", "quarter"), ("E4", "quarter"), ("D4", "half"),

    ("C4", "quarter"), ("C4", "quarter"), ("G4", "quarter"), ("G4", "quarter"),
    ("A4", "quarter"), ("A4", "quarter"), ("G4", "half"),

    ("F4", "quarter"), ("F4", "quarter"), ("E4", "quarter"), ("E4", "quarter"),
    ("D4", "quarter"), ("D4", "quarter"), ("C4", "whole"),
]

async def main():
    await play_song(twinkle)

runloop.run(main())
"""

"""
from hub import sound
import runloop

# Accurate Nyan Cat frequencies and durations
nyan_notes = [
    # First phrase
    1319, 1319, 1319, 2093, 1568,
    1319, 1319, 1319, 2093, 1568,
    1319, 1319, 1319, 2093, 1568, 1480, 1319,

    # Second phrase
    1175, 1175, 1175, 1976, 1568,
    1175, 1175, 1175, 1976, 1568,
    1175, 1175, 1175, 1976, 1568, 1480, 1319,

    # Third phrase
    2093, 2093, 2093, 1568, 1319,
    2093, 2093, 2093, 1568, 1319,
    2093, 2093, 2093, 1568, 1319, 1175, 1047
]

nyan_durations = [
    # First phrase
    100, 100, 100, 100, 200,
    100, 100, 100, 100, 200,
    100, 100, 100, 100, 100, 100, 100,

    # Second phrase
    100, 100, 100, 100, 200,
    100, 100, 100, 100, 200,
    100, 100, 100, 100, 100, 100, 100,

    # Third phrase
    100, 100, 100, 100, 200,
    100, 100, 100, 100, 200,
    100, 100, 100, 100, 100, 100, 400
]

async def main():
    # Play Nyan Cat forever!
    while True:
        for i in range(len(nyan_notes)):
            sound.beep(nyan_notes[i], nyan_durations[i])
            await runloop.sleep_ms(nyan_durations[i])
        # Short pause between loops
        await runloop.sleep_ms(100)

runloop.run(main())
"""

"""
from hub import sound
import runloop

# Zelda's Main Theme notes and durations
zelda_notes = [
    392, 392, 392, 311, 466, 392, 311, 466, 392,# Intro
    587, 587, 587, 622, 466, 369, 311, 466, 392,# Main theme part 1
    784, 392, 392, 784, 739, 698, 659, 622, 659,# Climbing part
    415, 554, 523, 493, 466, 440, 466,            # Descending part
    311, 369, 311, 466, 392, 311, 466, 392,        # Return to theme
    587, 587, 587, 622, 466, 369, 311, 466, 392,# Final phrase
    392, 311, 466, 392                            # Ending
]

zelda_durations = [
    300, 150, 150, 150, 150, 150, 150, 150, 600,# Intro
    300, 150, 150, 150, 150, 150, 150, 150, 600,# Main theme part 1
    300, 150, 150, 300, 150, 150, 150, 150, 600,# Climbing part
    150, 150, 150, 150, 150, 150, 600,            # Descending part
    150, 150, 150, 150, 150, 150, 150, 600,        # Return to theme
    300, 150, 150, 150, 150, 150, 150, 150, 900,# Final phrase
    600, 150, 150, 1200                            # Ending
]

async def main():
    # Play Zelda's theme once
    for i in range(len(zelda_notes)):
        sound.beep(zelda_notes[i], zelda_durations[i])
        await runloop.sleep_ms(zelda_durations[i])

    # Wait 3 seconds then play again
    await runloop.sleep_ms(3000)

runloop.run(main())
"""

"""
from hub import sound
import runloop

# Super Mario Bros Main Theme
mario_notes = [
    # Intro line
    659, 659, 0, 659, 0, 523, 659, 0, 784, 400
]
mario_durations = [
    # Intro line
    200, 200, 100, 200, 100, 200, 400, 100, 400, 400
]
async def main():
    # Play Mario theme once
    for i in range(len(mario_notes)):
        if mario_notes[i] > 0:# 0 represents rest/pause
            sound.beep(mario_notes[i], mario_durations[i])
        await runloop.sleep_ms(mario_durations[i])
runloop.run(main())
"""