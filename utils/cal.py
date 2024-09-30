import statistics

data = [
    {"x": 0.18732089643629832, "y": 0.48024739510781744, "z": -0.34237198999187235},
    {"x": 0.1880675835746249, "y": 0.4811563323534359, "z": -0.34318994938420194},
    {"x": 0.18785654739526292, "y": 0.4804777765382715, "z": -0.3432130691001318},
    {"x": 0.1890381679389313, "y": 0.48067175572519083, "z": -0.34338931297709924},
    {"x": 0.18854961832061068, "y": 0.4814961832061069, "z": -0.3437175572519084},
    {"x": 0.18947328244274808, "y": 0.4811297709923664, "z": -0.34331297709923664},
    {"x": 0.18802051779151016, "y": 0.48083757639471847, "z": -0.34203138699635616},
    {"x": 0.18692941166906488, "y": 0.4816114298357909, "z": -0.3435032067663594},
    {"x": 0.18856488549618322, "y": 0.48248091603053433, "z": -0.3426641221374046},
    {"x": 0.18829007633587785, "y": 0.4816946564885496, "z": -0.3432977099236641}
]

def calculate_mean(data, axis):
    values = [d[axis] for d in data]
    return statistics.mean(values)

def calculate_std_dev(data, axis):
    values = [d[axis] for d in data]
    return statistics.stdev(values)

def filter_outliers(data, axis, threshold=2):
    mean = calculate_mean(data, axis)
    std_dev = calculate_std_dev(data, axis)
    filtered_data = [d for d in data if abs(d[axis] - mean) <= threshold * std_dev]
    return filtered_data

def filter_all_axes(data, threshold=2):
    filtered_data = data
    for axis in ['x', 'y', 'z']:
        filtered_data = filter_outliers(filtered_data, axis, threshold)
    return filtered_data

filtered_data = filter_all_axes(data)

mean_x = calculate_mean(filtered_data, 'x')
mean_y = calculate_mean(filtered_data, 'y')
mean_z = calculate_mean(filtered_data, 'z')

print(f"Mean value for Gyro X: {mean_x}")
print(f"Mean value for Gyro Y: {mean_y}")
print(f"Mean value for Gyro Z: {mean_z}")
