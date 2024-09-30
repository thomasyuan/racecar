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

# Set interval for main loop
MAIN_LOOP_INTERVAL = 1

# Set interval for monitor loop
MONITOR_LOOP_INTERVAL = 0.1

# Calibration offsets
CALIBRATION_OFFSET_X = 0.18821109874011124
CALIBRATION_OFFSET_Y = 0.48118037926727825
CALIBRATION_OFFSET_Z = -0.3430691281628235

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
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

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

def main():
    initialize_gyro()
    try:
        while True:
            gyro_x, gyro_y, gyro_z = read_gyro_data()
            print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")
            time.sleep(MAIN_LOOP_INTERVAL)
    except KeyboardInterrupt:
        print("Measurement stopped by User")

def monitor_gyro():
    initialize_gyro()
    while True:
        controller.handle_gyro(*read_gyro_data())
        time.sleep(MONITOR_LOOP_INTERVAL)

def start_monitoring():
    start_daemon_thread(monitor_gyro)

if __name__ == "__main__":
    main()