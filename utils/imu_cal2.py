import smbus
from time import sleep
import statistics

# MPU6050 Registers and their addresses
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# Initialize I2C bus
bus = smbus.SMBus(1)
IMU_ADDRESS = 0x68

def MPU_Init():
    # Write to sample rate register
    bus.write_byte_data(IMU_ADDRESS, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(IMU_ADDRESS, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(IMU_ADDRESS, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(IMU_ADDRESS, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(IMU_ADDRESS, INT_ENABLE, 1)

def read_raw_data(addr):
    # Accelero and Gyro values are 16-bit
    high = bus.read_byte_data(IMU_ADDRESS, addr)
    low = bus.read_byte_data(IMU_ADDRESS, addr + 1)

    # Concatenate higher and lower value
    value = (high << 8) | low

    # To get signed value from mpu6050
    if value > 32767:
        value = value - 65536
    return value

def read_gyro():
    # Example function to read gyro data from MPU6050
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    Gx = gyro_x / 131.0
    Gy = gyro_y / 131.0
    Gz = gyro_z / 131.0

    return Gx, Gy, Gz

def filter_outliers(data, threshold=2):
    mean = statistics.mean(data)
    std_dev = statistics.stdev(data)
    # Filter out values that are more than 'threshold' standard deviations away from the mean
    filtered_data = [x for x in data if abs(x - mean) <= threshold * std_dev]
    return filtered_data

def calibrate_gyro(samples=1000):
    gyro_x_data = []
    gyro_y_data = []
    gyro_z_data = []

    print("Collecting gyro data for calibration...")
    for _ in range(samples):
        Gx, Gy, Gz = read_gyro()
        gyro_x_data.append(Gx)
        gyro_y_data.append(Gy)
        gyro_z_data.append(Gz)
        sleep(0.01)  # Read every 0.01 second

    # Filter out outliers
    gyro_x_data = filter_outliers(gyro_x_data)
    gyro_y_data = filter_outliers(gyro_y_data)
    gyro_z_data = filter_outliers(gyro_z_data)

    mean_x = statistics.mean(gyro_x_data)
    mean_y = statistics.mean(gyro_y_data)
    mean_z = statistics.mean(gyro_z_data)

    print(f"Mean value for Gyro X: {mean_x}")
    print(f"Mean value for Gyro Y: {mean_y}")
    print(f"Mean value for Gyro Z: {mean_z}")

    return mean_x, mean_y, mean_z

if __name__ == "__main__":
    MPU_Init()
    calibrate_gyro()