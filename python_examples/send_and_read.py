from threading import Thread
import time
import pygame
import Adafruit_PCA9685

import smbus

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

bus = smbus.SMBus(1)
address = 0x05

zero_input = 330
input_value = zero_input

def bytes_to_int(values):
    result = 0
    mask = 0
    for value in values:
        result += (value << mask)
        mask += 8
    return result


def read_data():
    time_ref = time.time()
    while True:
        try:
            global input_value
            current_time = time.time() - time_ref
            data = bus.read_i2c_block_data(address, 0, 2)
            value = bytes_to_int(data)
#             print("time: {:0.2f}, value: {}, input: {}".format(current_time, value, input_value))
            time.sleep(0.01)
        except OSError:
            pass


def joystick_events():
    pygame.init()

    pygame.joystick.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    done = False

    while done == False:
        global input_value
        for event in pygame.event.get():  # User did something
            if event.type == pygame.JOYBUTTONDOWN:
                done = True
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

        axis_y = -joystick.get_axis(1)

        if axis_y > 0:
            input_value = zero_input + (axis_y * 100)
        else:
            input_value = zero_input

        time.sleep(0.001)
    
def send_input():
    global input_value
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(60)
    while True:
        pwm.set_pwm(0, 0, int(input_value))
        print("sent {}".format(input_value))
        time.sleep(0.5)
            


if __name__ == "__main__":
    thread_reader = Thread(target=read_data)
    thread_joystick = Thread(target=joystick_events)
    thread_input = Thread(target=send_input)

    thread_reader.start()
    thread_joystick.start()
    thread_input.start()

    thread_reader.join()
    thread_joystick.join()
    thread_input.join()