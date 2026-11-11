from machine import Pin, PWM
from servo_translator import translate
import time

# these pins are for J1 J2 and J3
# check that the shoulder, elbow and wrist are plugged in this order
shoulder = PWM(Pin(0))
elbow = PWM(Pin(1))
wrist = PWM(Pin(2))

shoulder.freq(50)
elbow.freq(50)
wrist.freq(50)


def move_servo(servo, angle):
    servo.duty_u16(translate(angle))
    time.sleep(0.1)


def parse_gcode(line):
    line = line.strip()
    pieces = line.split()
    return pieces


def execute_command(pieces):
    if len(pieces) == 0:
        return

    command = pieces[0]

    if command == "G1":
        for item in pieces[1:]:
            if item.startswith("S"):
                angle = float(item[1:])
                move_servo(shoulder, angle)
            if item.startswith("E"):
                angle = float(item[1:])
                move_servo(elbow, angle)

    if command == "M3":
        move_servo(wrist, 30)  # pen down

    if command == "M5":
        move_servo(wrist, 0)  # pen up

    if command == "M18":
        shoulder.deinit()
        elbow.deinit()
        wrist.deinit()


def read_gcode(filename):
    with open(filename, "r") as file:
        for line in file:
            pieces = parse_gcode(line)
            print(pieces)  # helps see what is happening
            execute_command(pieces)


def main():
    read_gcode("line.gcode")


main()
