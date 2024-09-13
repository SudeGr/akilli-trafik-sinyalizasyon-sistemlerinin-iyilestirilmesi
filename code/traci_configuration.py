import traci
import os
import sys
import pandas
import calculations
import constant_definitions as constants
import logger
import fuzzy_logic


def __start_sumo():
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("Lutfen, 'SUMO_HOME' degiskenini tanimlayin!")

    sumo_binary = "sumo"
    sumo_config = constants.base_path + constants.sumo_path
    sumo_cmd = [sumo_binary, "-c", sumo_config, "--start"]

    traci.start(sumo_cmd)


def __record_vehicle_waitings(data_frame):
    for vehicle in traci.vehicle.getIDList():
        vehicle_waiting_time = traci.vehicle.getWaitingTime(vehicle)
        data_frame.loc[len(data_frame)] = [vehicle, vehicle_waiting_time]

    return data_frame


def __record_pedestrian_waitings(data_frame):
    for person in traci.person.getIDList():
        pedestrian_waiting_time = traci.person.getWaitingTime(person)
        data_frame.loc[len(data_frame)] = [person, pedestrian_waiting_time]

    return data_frame


def __determine_standart_long_vehicle_number(vehicle_ids):
    standard_vehicle_num = 0
    long_vehicle_num = 0

    try:
        for vehicle_id in vehicle_ids:
            vehicle_type = traci.vehicle.getTypeID(vehicle_id)
            if vehicle_type == "standard_vehicle":
                standard_vehicle_num += 1
            elif vehicle_type == "long_vehicle":
                long_vehicle_num += 1

    except Exception as e:
        raise Exception(f"Arac bilgisi okunurken hata olustu: {vehicle_id}: {e}")

    return standard_vehicle_num, long_vehicle_num


def __get_current_vehicle_pedestrian_count():
    # Her bir faz icin arac sayisi alinir.
    north_vehicle_ids = traci.edge.getLastStepVehicleIDs("north_leave")
    south_vehicle_ids = traci.edge.getLastStepVehicleIDs("south_leave")
    east_vehicle_ids = traci.edge.getLastStepVehicleIDs("east_leave")
    west_vehicle_ids = traci.edge.getLastStepVehicleIDs("west_leave")

    (north_standard_vehicle_num, north_long_vehicle_num) = __determine_standart_long_vehicle_number(
        north_vehicle_ids)
    (south_standard_vehicle_num, south_long_vehicle_num) = __determine_standart_long_vehicle_number(
        south_vehicle_ids)
    (east_standard_vehicle_num, east_long_vehicle_num) = __determine_standart_long_vehicle_number(
        east_vehicle_ids)
    (west_standard_vehicle_num, west_long_vehicle_num) = __determine_standart_long_vehicle_number(
        west_vehicle_ids)

    path1_standard_vehicle_num = north_standard_vehicle_num + south_standard_vehicle_num
    path1_long_vehicle_num = north_long_vehicle_num + south_long_vehicle_num
    path2_standard_vehicle_num = east_standard_vehicle_num + west_standard_vehicle_num
    path2_long_vehicle_num = east_long_vehicle_num + west_long_vehicle_num

    # Her bir faz icin yolcu sayisi alinir.
    c0_pedestrian_num = len(traci.edge.getLastStepPersonIDs(":main_junction_c0"))
    c1_pedestrian_num = len(traci.edge.getLastStepPersonIDs(":main_junction_c1"))
    c2_pedestrian_num = len(traci.edge.getLastStepPersonIDs(":main_junction_c2"))
    c3_pedestrian_num = len(traci.edge.getLastStepPersonIDs(":main_junction_c3"))
    north_arrive_pedestrian_num = len(traci.edge.getLastStepPersonIDs("north_arrive"))
    north_leave_pedestrian_num = len(traci.edge.getLastStepPersonIDs("north_leave"))
    south_arrive_pedestrian_num = len(traci.edge.getLastStepPersonIDs("south_arrive"))
    south_leave_pedestrian_num = len(traci.edge.getLastStepPersonIDs("south_leave"))
    east_leave_pedestrian_num = len(traci.edge.getLastStepPersonIDs("east_leave"))
    east_arrive_pedestrian_num = len(traci.edge.getLastStepPersonIDs("east_arrive"))
    west_leave_pedestrian_num = len(traci.edge.getLastStepPersonIDs("west_leave"))
    west_arrive_pedestrian_num = len(traci.edge.getLastStepPersonIDs("west_arrive"))

    path1_pedestrian_num = (north_arrive_pedestrian_num + north_leave_pedestrian_num +
                            south_arrive_pedestrian_num + south_leave_pedestrian_num +
                            c0_pedestrian_num + c2_pedestrian_num)
    path2_pedestrian_num = (east_leave_pedestrian_num + east_arrive_pedestrian_num +
                            west_leave_pedestrian_num + west_arrive_pedestrian_num +
                            c1_pedestrian_num + c3_pedestrian_num)

    return path1_standard_vehicle_num, path1_long_vehicle_num, path1_pedestrian_num, path2_standard_vehicle_num, \
           path2_long_vehicle_num, path2_pedestrian_num


def __get_current_green_duration(current_time):
    (path1_standard_vehicle_count,
     path1_long_vehicle_count,
     path1_pedestrian_count,
     path2_standard_vehicle_count,
     path2_long_vehicle_count,
     path2_pedestrian_count) = __get_current_vehicle_pedestrian_count()

    # Faz 1 ve faz 2 trafik yogunluklari hesaplanir.
    (path1_density, path2_density) = calculations.calculate_path_densities(
        path1_standard_vehicle_num=path1_standard_vehicle_count,
        path1_long_vehicle_num=path1_long_vehicle_count,
        path1_pedestrian_num=path1_pedestrian_count,
        path2_standard_vehicle_num=path2_standard_vehicle_count,
        path2_long_vehicle_num=path2_long_vehicle_count,
        path2_pedestrian_num=path2_pedestrian_count)

    # Yesil isik sureleri hesaplanir.
    (phase1_duration, phase2_duration) = fuzzy_logic.determine_durations(
        path1_density=path1_density,
        path2_density=path2_density)

    traffic_volume = {'path1_standard_vehicle_count': path1_standard_vehicle_count,
                      'path1_long_vehicle_count': path1_long_vehicle_count,
                      'path1_pedestrian_count': path1_pedestrian_count,
                      'path2_standard_vehicle_count': path2_standard_vehicle_count,
                      'path2_long_vehicle_count': path2_long_vehicle_count,
                      'path2_pedestrian_count': path2_pedestrian_count}

    logger.log_traffic(traffic_volume=traffic_volume, path1_density=path1_density,
                       path2_density=path2_density, path1_green_time=phase1_duration,
                       path2_green_time=phase2_duration, current_minute=current_time)

    return phase1_duration, phase2_duration


def __set_path_durations(phase1_duration, phase2_duration):
    traffic_light_id = traci.trafficlight.getIDList()[0]
    traffic_light_def = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)

    phases = traffic_light_def[0].phases
    phases[0].duration = phase2_duration  # east-west yesil
    phases[3].duration = phase1_duration  # north-south yesil

    logic = traci.trafficlight.Logic(traffic_light_def[0].programID, traffic_light_def[0].type,
                                     traffic_light_def[0].currentPhaseIndex, phases=phases)
    traci.trafficlight.setProgramLogic(traffic_light_id, logic)


def run_enhanced_signaling():
    """Iyilestirilmis yesil isik sureleri Traci araciligiyla SUMO simulasyonuna saglanir ve simulasyon calistirilir.
    Araclarin ve yayalarin bekleme sureleri kaydedilir."""

    try:
        __start_sumo()

        vehicle_data_frame = pandas.DataFrame(columns=['vehicle_id', 'waiting_times_sec'])
        pedestrian_data_frame = pandas.DataFrame(columns=['pedestrian_id', 'waiting_times_sec'])

        # Flow'u baslatmak icin sumo simulasyonu calistirilir.
        for _ in range(2):
            traci.simulationStep()

        # Sumo simulasyonu 5 dakika boyunca calistirlir.
        for i in range(1, constants.simulation_time + 1):
            (path1_green_duration, path2_green_duration) = __get_current_green_duration(current_time=i)

            if i > 0:
                __set_path_durations(path1_green_duration, path2_green_duration)

            for j in range(constants.one_minute):
                traci.simulationStep()
                vehicle_data_frame = __record_vehicle_waitings(vehicle_data_frame)
                pedestrian_data_frame = __record_pedestrian_waitings(pedestrian_data_frame)

        traci.close()

        # Verileri excel dosyasina kadeder.
        excel_name = constants.base_path + constants.files_path + constants.enhanced_signaling_excel_name
        with pandas.ExcelWriter(excel_name) as writer:
            vehicle_data_frame.to_excel(writer, sheet_name='Vehicles', index=False)
            pedestrian_data_frame.to_excel(writer, sheet_name='Pedestrians', index=False)

    except FileNotFoundError:
        raise FileNotFoundError("Dosya bulunamadi!")
    except Exception as e:
        raise Exception(f"Hata Olustu: {str(e)}")


def run_fixed_time_signaling():
    """Sabit zaman sistem icin sumo simulasyonu calistirilir."""

    try:
        __start_sumo()

        traffic_light_id = traci.trafficlight.getIDList()[0]
        program_def = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)

        phases = program_def[0].phases
        phases[0].duration = constants.fixed_phase2_green_duration  # east-west yesil
        phases[3].duration = constants.fixed_phase1_green_duration  # north-south yesil
        logic = traci.trafficlight.Logic(program_def[0].programID, program_def[0].type,
                                         program_def[0].currentPhaseIndex, phases=phases)
        traci.trafficlight.setProgramLogic(traffic_light_id, logic)

        vehicle_data_frame = pandas.DataFrame(columns=['vehicle_id', 'waiting_times_sec'])
        pedestrian_data_frame = pandas.DataFrame(columns=['pedestrian_id', 'waiting_times_sec'])

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            vehicle_data_frame = __record_vehicle_waitings(vehicle_data_frame)
            pedestrian_data_frame = __record_pedestrian_waitings(pedestrian_data_frame)

        traci.close()

        excel_name = constants.base_path + constants.files_path + constants.fixed_signaling_excel_name
        with pandas.ExcelWriter(excel_name) as writer:
            vehicle_data_frame.to_excel(writer, sheet_name='Vehicles', index=False)
            pedestrian_data_frame.to_excel(writer, sheet_name='Pedestrians', index=False)
    except Exception as e:
        raise Exception(f"Hata Olustu: {str(e)}")
