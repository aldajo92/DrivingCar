import smbus
import time

bus = smbus.SMBus(1)
address = 0x05

def bytes_to_int(values):
    result = 0
    mask = 0
    for value in values:
        result += (value << mask)
        mask += 8
    return result

time_ref = time.time()
while True:
    try:
        current_time = time.time() - time_ref
        data = bus.read_i2c_block_data(address,0,2)
        value = bytes_to_int(data)
        print("time: {:0.2f}, value: {}".format(current_time, value))
        time.sleep(0.01)
    except OSError:
        pass
#         print("connection error")