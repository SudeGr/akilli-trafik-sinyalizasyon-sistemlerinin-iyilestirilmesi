import constant_definitions as constants
import logger
import pandas


def calculate_path_densities(path1_standard_vehicle_num,
                             path1_long_vehicle_num,
                             path1_pedestrian_num,
                             path2_standard_vehicle_num,
                             path2_long_vehicle_num,
                             path2_pedestrian_num):
    """Agirlikli ortalama yontemi kullanilarak her bir fazdaki trafik yogunlugu hesaplanir."""

    try:
        path1_density = 0
        path2_density = 0

        path1_weight = (
                path2_pedestrian_num * constants.pedestrian_weight +
                path1_standard_vehicle_num * constants.standard_vehicle_weight +
                path1_long_vehicle_num * constants.long_vehicle_weight
        )

        path2_weight = (
                path1_pedestrian_num * constants.pedestrian_weight +
                path2_standard_vehicle_num * constants.standard_vehicle_weight +
                path2_long_vehicle_num * constants.long_vehicle_weight
        )

        total_weight = (
                path1_standard_vehicle_num * constants.standard_vehicle_weight +
                path1_long_vehicle_num * constants.long_vehicle_weight +
                path1_pedestrian_num * constants.pedestrian_weight +
                path2_standard_vehicle_num * constants.standard_vehicle_weight +
                path2_long_vehicle_num * constants.long_vehicle_weight +
                path2_pedestrian_num * constants.pedestrian_weight
        )

        if path1_weight > 0:
            path1_density = (path1_weight / total_weight) * 100

        if path2_weight > 0:
            path2_density = (path2_weight / total_weight) * 100

        path1_density = round(path1_density, 2)
        path2_density = round(path2_density, 2)

        return path1_density, path2_density
    except Exception as e:
        raise Exception("Hata Olustu: " + str(e))


def determine_enhancement_success_rate():
    """Sabit zamanli trafik sinyalizasyon sistemlerine oranla fuzzy logic 
    algoritmasinin sagladigi iyilestirme yuzdesini hesaplar. Error hesaplama yontemi kullanilir."""

    try:
        # Arac ve yaya bekleme sureleri excel dosyalarindan okunur.
        enhanced_signaling_data_file = constants.base_path+constants.files_path+constants.enhanced_signaling_excel_name
        enhanced_data = pandas.read_excel(enhanced_signaling_data_file, sheet_name=None)

        enhanced_vehicle_sheet = enhanced_data['Vehicles']
        enhanced_vehicle_max = enhanced_vehicle_sheet.groupby('vehicle_id')['waiting_times_sec'].max().reset_index()
        total_enhanced_vehicle_waitings = enhanced_vehicle_max['waiting_times_sec'].sum()

        enhanced_pedestrian_sheet = enhanced_data['Pedestrians']
        enhanced_pedestrian_max = enhanced_pedestrian_sheet.groupby('pedestrian_id')['waiting_times_sec'].max().reset_index()
        total_enhanced_pedestrian_waitings = enhanced_pedestrian_max['waiting_times_sec'].sum()

        fixed_signaling_data_file = constants.base_path + constants.files_path + constants.fixed_signaling_excel_name
        fixed_data = pandas.read_excel(fixed_signaling_data_file, sheet_name=None)

        fixed_vehicle_sheet = fixed_data['Vehicles']
        fixed_vehicle_max = fixed_vehicle_sheet.groupby('vehicle_id')['waiting_times_sec'].max().reset_index()
        total_fixed_vehicle_waitings = fixed_vehicle_max['waiting_times_sec'].sum()

        fixed_pedestrian_sheet = fixed_data['Pedestrians']
        fixed_pedestrian_max = fixed_pedestrian_sheet.groupby('pedestrian_id')['waiting_times_sec'].max().reset_index()
        total_fixed_pedestrian_waitings = fixed_pedestrian_max['waiting_times_sec'].sum()

        total_weight = constants.standard_vehicle_weight + constants.pedestrian_weight

        # Arac ve yayalar icin agirlikli toplam hesaplanir.
        fixed_signaling_weighted_sum = (
                (constants.vehicle_weight * total_fixed_vehicle_waitings +
                 constants.pedestrian_weight * total_fixed_pedestrian_waitings) / total_weight
        )

        enhanced_signaling_weighted_sum = (
                (constants.vehicle_weight * total_enhanced_vehicle_waitings +
                 constants.pedestrian_weight * total_enhanced_pedestrian_waitings) / total_weight
        )

        # Algoritmanin basari yuzdesi hesaplanir.
        success_rate = ((fixed_signaling_weighted_sum - enhanced_signaling_weighted_sum)
                        / fixed_signaling_weighted_sum) * 100

        success_rate = round(success_rate, 4)

        logger.log_success_rate(success_rate=f"{success_rate}")

        print("Fixed time signaling durations: ")
        print(f"  Vehicles: {total_fixed_vehicle_waitings}")
        print(f"  Pedestrians: {total_fixed_pedestrian_waitings}\n")
        print("Enhanced signaling durations: ")
        print(f"  Vehicle: {total_enhanced_vehicle_waitings}")
        print(f"  Pedestrians: {total_enhanced_pedestrian_waitings}\n")
        print(f"Succes rate: {success_rate}%")

    except Exception as e:
        raise Exception("Hata Olustu: " + str(e))
