"""Birden fazla Python dosyasinda kullanilan sabit tanimlari ve pathleri icerir."""

base_path = '/home/ubuntu/Desktop/2209a'
sumo_path = '/sumo/real-life/traffic_junction_test.sumocfg'
logs_path = '/files/logs.txt'
files_path = '/files/'

fixed_signaling_excel_name = 'fixed_waiting_times.xlsx'
enhanced_signaling_excel_name = 'enhanced_waiting_times.xlsx'

north_south = 1
east_west = 2

vehicle_weight = 1
pedestrian_weight = 1
standard_vehicle_weight = 1
long_vehicle_weight = 1.2

simulation_time = 5  # minute
one_minute = 60  # second

default_green_duration = 30
default_yellow_duration = 3

cycle_duration = 60  # second
fixed_phase1_green_duration = 20  # north-south green
fixed_phase2_green_duration = 40  # east-west green