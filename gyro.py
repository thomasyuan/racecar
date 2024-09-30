import controller
import smbus
import time
from utils import start_daemon_thread  # Import the start_daemon_thread function

# I2C bus and address
I2C_BUS = 1
IMU_ADDRESS = 0x68  # Example I2C address for MPU6050

# MPU6050 Registers and their addresses
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# Calibration offsets (initially set to zero)
CALIBRATION_OFFSET_X = 0.0
CALIBRATION_OFFSET_Y = 0.0
CALIBRATION_OFFSET_Z = 0.0

# Gyro sensitivity (LSB/dps)
GYRO_SENSITIVITY = 131.0  # Assuming ±250 dps

MONITOR_INTERVAL = 0.05

# Initialize I2C bus
bus = smbus.SMBus(I2C_BUS)

def initialize_gyro():
    # Write to power management register to wake up the MPU6050
    bus.write_byte_data(IMU_ADDRESS, PWR_MGMT_1, 0)
    # Write to sample rate register
    bus.write_byte_data(IMU_ADDRESS, SMPLRT_DIV, 7)
    # Write to configuration register
    bus.write_byte_data(IMU_ADDRESS, CONFIG, 0)
    # Write to gyro configuration register
    bus.write_byte_data(IMU_ADDRESS, GYRO_CONFIG, 24)
    # Write to interrupt enable register
    bus.write_byte_data(IMU_ADDRESS, INT_ENABLE, 1)

def read_gyro_data():
    # Read raw gyro data
    gyro_x = read_raw_data(GYRO_XOUT_H) / GYRO_SENSITIVITY
    gyro_y = read_raw_data(GYRO_YOUT_H) / GYRO_SENSITIVITY
    gyro_z = read_raw_data(GYRO_ZOUT_H) / GYRO_SENSITIVITY

    # Apply calibration offsets
    gyro_x -= CALIBRATION_OFFSET_X
    gyro_y -= CALIBRATION_OFFSET_Y
    gyro_z -= CALIBRATION_OFFSET_Z

    return gyro_x, gyro_y, gyro_z

def read_raw_data(addr):
    # Read two bytes of data from the given address
    high = bus.read_byte_data(IMU_ADDRESS, addr)
    low = bus.read_byte_data(IMU_ADDRESS, addr + 1)
    # Combine the two bytes
    value = ((high << 8) | low)
    # Convert to signed value
    if value > 32768:
        value -= 65536
    return value

def calibrate_gyro(samples=500):
    global CALIBRATION_OFFSET_X, CALIBRATION_OFFSET_Y, CALIBRATION_OFFSET_Z
    sum_x = 0
    sum_y = 0
    sum_z = 0
    for _ in range(samples):
        gyro_x, gyro_y, gyro_z = read_gyro_data()
        sum_x += gyro_x
        sum_y += gyro_y
        sum_z += gyro_z
        time.sleep(0.01)  # Small delay between samples
    CALIBRATION_OFFSET_X = sum_x / samples
    CALIBRATION_OFFSET_Y = sum_y / samples
    CALIBRATION_OFFSET_Z = sum_z / samples
    print(f"Calibration offsets: X={CALIBRATION_OFFSET_X}, Y={CALIBRATION_OFFSET_Y}, Z={CALIBRATION_OFFSET_Z}")

def main():
    try:
        monitor_gyro()
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        bus.close()

def monitor_gyro():
    initialize_gyro()
    calibrate_gyro()
    while True:
        gyro_x, gyro_y, gyro_z = read_gyro_data()
        controller.handle_gyro({"gyro_x": gyro_x, "gyro_y": gyro_y, "gyro_z": gyro_z})
        #print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")
        time.sleep(MONITOR_INTERVAL)

def start():
    start_daemon_thread(monitor_gyro)

def exit():
    bus.close()

if __name__ == "__main__":
    main()