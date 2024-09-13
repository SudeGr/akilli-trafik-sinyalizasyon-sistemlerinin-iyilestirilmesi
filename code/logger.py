import datetime
import constant_definitions as const


def log_traffic(traffic_volume, path1_density, path2_density, path1_green_time, path2_green_time, current_minute):
    try:
        path = const.base_path + const.logs_path
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")

        with open(path, 'a') as f:
            if current_minute == 1:
                f.write(date_string + '\n' + '***-------------------------------------------------------***\n')
            f.write(f"Simulation Minute: {current_minute}\n")

            f.write('\tCounts:\n')
            f.write(f"\t\tStandard vehicles in path 1: {traffic_volume['path1_standard_vehicle_count']}\n")
            f.write(f"\t\tLong vehicles in path 1: {traffic_volume['path1_long_vehicle_count']}\n")
            f.write(f"\t\tPedestrians in path 1: {traffic_volume['path1_pedestrian_count']}\n")
            f.write(f"\t\tStandard vehicles in path 2: {traffic_volume['path2_standard_vehicle_count']}\n")
            f.write(f"\t\tLong vehicles in path 2: {traffic_volume['path2_long_vehicle_count']}\n")
            f.write(f"\t\tPedestrians in path 2: {traffic_volume['path2_pedestrian_count']}\n\n")

            f.write('\tDensities:\n')
            f.write(f"\t\tDensity of path 1: {path1_density}\n")
            f.write(f"\t\tDensity of path 2: {path2_density}\n\n")

            f.write('\tDurations:\n')
            f.write(f"\t\tGreen duration of path 1 (seconds): {path1_green_time}\n")
            f.write(f"\t\tGreen duration of path 2 (seconds): {path2_green_time}\n\n")

    except RuntimeError as e:
        raise RuntimeError(f"Hata Olustu: {e}")


def log_success_rate(success_rate):
    path = const.base_path + const.logs_path
    try:
        with open(path, 'a') as f:
            f.write("\tEnhancement:\n")
            f.write(f"\t\tPercentage enhancement: %{success_rate}\n\n\n\n")

    except FileNotFoundError:
        raise FileNotFoundError("Dosya bulunamadi!")
