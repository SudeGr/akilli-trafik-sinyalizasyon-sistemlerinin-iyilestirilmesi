import constant_definitions as constants
import numpy
import skfuzzy


def __calculate_duration_extension(path1_density, path2_density):
    fuzzy_input_range = numpy.arange(0, 101, 1)

    # Faz 1 ve faz 2 icin membership fonksiyonunu kullanarak fuzzy logic girdisi ayarlanir.
    path1_zero = skfuzzy.trapmf(fuzzy_input_range, [0, 0, 0, 0])
    path1_small = skfuzzy.trapmf(fuzzy_input_range, [0, 10, 20, 35])
    path1_medium = skfuzzy.trapmf(fuzzy_input_range, [20, 35, 50, 60])
    path1_high = skfuzzy.trapmf(fuzzy_input_range, [50, 60, 80, 90])
    path1_very_high = skfuzzy.trapmf(fuzzy_input_range, [80, 90, 100, 100])

    path2_zero = skfuzzy.trapmf(fuzzy_input_range, [0, 0, 0, 0])
    path2_small = skfuzzy.trapmf(fuzzy_input_range, [0, 10, 20, 35])
    path2_medium = skfuzzy.trapmf(fuzzy_input_range, [20, 35, 50, 60])
    path2_high = skfuzzy.trapmf(fuzzy_input_range, [50, 60, 80, 90])
    path2_very_high = skfuzzy.trapmf(fuzzy_input_range, [80, 90, 100, 100])

    # Faz 1 ve faz 2 icin Membership fonksiyon hazirlanir.
    path1_fix_zero = skfuzzy.interp_membership(fuzzy_input_range, path1_zero, path1_density)
    path1_fix_small = skfuzzy.interp_membership(fuzzy_input_range, path1_small, path1_density)
    path1_fix_medium = skfuzzy.interp_membership(fuzzy_input_range, path1_medium, path1_density)
    path1_fix_high = skfuzzy.interp_membership(fuzzy_input_range, path1_high, path1_density)
    path1_fix_very_high = skfuzzy.interp_membership(fuzzy_input_range, path1_very_high, path1_density)

    path2_fix_zero = skfuzzy.interp_membership(fuzzy_input_range, path2_zero, path2_density)
    path2_fix_small = skfuzzy.interp_membership(fuzzy_input_range, path2_small, path2_density)
    path2_fix_medium = skfuzzy.interp_membership(fuzzy_input_range, path2_medium, path2_density)
    path2_fix_high = skfuzzy.interp_membership(fuzzy_input_range, path2_high, path2_density)
    path2_fix_very_high = skfuzzy.interp_membership(fuzzy_input_range, path2_very_high, path2_density)

    print(f"path1_fix_zero = {path1_fix_zero}")
    print(f"path1_fix_small = {path1_fix_small}")
    print(f"path1_fix_medium = {path1_fix_medium}")
    print(f"path1_fix_high = {path1_fix_high}")
    print(f"path1_fix_very_high = {path1_fix_very_high}")
    print(f"path2_fix_zero = {path2_fix_zero}")
    print(f"path2_fix_small = {path2_fix_small}")
    print(f"path2_fix_medium = {path2_fix_medium}")
    print(f"path2_fix_high = {path2_fix_high}")
    print(f"path2_fix_very_high = {path2_fix_very_high}")

    # Varsayilan yesil sure faz basina 30 saniyedir.
    # Trafik yogunluguna gore bu deger faz basina 60 saniyeye kadar uzatilabilir.
    fuzzy_output_range = numpy.arange(0, 31, 1)

    extension_default = skfuzzy.trimf(fuzzy_output_range, [0, 0, 0])
    green_extension_small = skfuzzy.trimf(fuzzy_output_range, [0, 4, 8])
    green_extension_medium = skfuzzy.trimf(fuzzy_output_range, [4, 8, 14])
    green_extension_high = skfuzzy.trimf(fuzzy_output_range, [10, 14, 16])
    green_extension_very_high = skfuzzy.trimf(fuzzy_output_range, [14, 16, 20])
    green_extension_full = skfuzzy.trimf(fuzzy_output_range, [20, 22, 25])

    # Fuzzy logic kurallari
    rule_1 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_zero, path2_fix_zero),
                                   numpy.fmin(path1_fix_small, path2_fix_small)),
                        extension_default)
    rule_2 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_medium, path2_fix_medium),
                                   numpy.fmin(path1_fix_high, path2_fix_high)),
                        extension_default)
    rule_3 = numpy.fmin(numpy.fmin(path1_fix_very_high, path2_fix_very_high),
                        extension_default)
    rule_4 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_zero, path2_fix_small),
                                   numpy.fmin(path1_fix_zero, path2_fix_medium)),
                        green_extension_full)
    rule_5 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_small, path2_fix_zero),
                                   numpy.fmin(path1_fix_medium, path2_fix_zero)),
                        green_extension_full)
    rule_6 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_zero, path2_fix_high),
                                   numpy.fmin(path1_fix_high, path2_fix_zero)),
                        green_extension_full)
    rule_7 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_zero, path2_fix_very_high),
                                   numpy.fmin(path1_fix_very_high, path2_fix_zero)),
                        green_extension_full)
    rule_8 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_small, path2_fix_medium),
                                   numpy.fmin(path1_fix_medium, path2_fix_small)),
                        green_extension_small)
    rule_9 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_high, path2_fix_very_high),
                                   numpy.fmin(path1_fix_very_high, path2_fix_high)),
                        green_extension_small)
    rule_10 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_high, path2_fix_medium),
                                    numpy.fmin(path1_fix_medium, path2_fix_high)),
                         green_extension_medium)
    rule_11 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_very_high, path2_fix_medium),
                                    numpy.fmin(path1_fix_medium, path2_fix_very_high)),
                         green_extension_high)
    rule_12 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_small, path2_fix_high),
                                    numpy.fmin(path1_fix_high, path2_fix_small)),
                         green_extension_high)
    rule_13 = numpy.fmin(numpy.fmax(numpy.fmin(path1_fix_very_high, path2_fix_small),
                                    numpy.fmin(path1_fix_small, path2_fix_very_high)),
                         green_extension_very_high)

    enhancement_1 = numpy.fmax(rule_1, rule_2)
    enhancement_2 = numpy.fmax(enhancement_1, rule_3)
    enhancement_3 = numpy.fmax(rule_4, rule_5)
    enhancement_4 = numpy.fmax(rule_6, rule_7)
    enhancement_5 = numpy.fmax(enhancement_3, enhancement_4)
    enhancement_6 = numpy.fmax(enhancement_2, enhancement_5)
    enhancement_7 = numpy.fmax(rule_8, rule_9)
    enhancement_8 = numpy.fmax(enhancement_6, enhancement_7)
    enhancement_9 = numpy.fmax(enhancement_8, rule_10)
    enhancement_10 = numpy.fmax(rule_11, rule_12)
    enhancement_11 = numpy.fmax(enhancement_9, enhancement_10)
    enhancement_12 = numpy.fmax(enhancement_11, rule_13)

    extension = skfuzzy.defuzz(fuzzy_output_range, enhancement_12, 'centroid')
    return extension


def determine_durations(path1_density, path2_density):
    """Faz 1 ve Faz 2'deki trafik yogunlugunu baz alarak bulanik mantik kullanarak 
    her faz icin yesil isik suresini hesaplar."""

    try:
        time_extension = __calculate_duration_extension(path1_density, path2_density)

        # Default yesil isik suresi set edildi.
        path1_enhanced_duration = constants.default_green_duration
        path2_enhanced_duration = constants.default_green_duration

        # Yeni yesil isik suresleri set edildi.
        if path2_density > path1_density:
            path1_enhanced_duration = constants.default_green_duration - time_extension
            path2_enhanced_duration = constants.default_green_duration + time_extension
        elif path1_density > path2_density:
            path1_enhanced_duration = constants.default_green_duration + time_extension
            path2_enhanced_duration = constants.default_green_duration - time_extension

        formatted_path1_enhanced_duration = round(path1_enhanced_duration, 1)
        formatted_path2_enhanced_duration = round(path2_enhanced_duration, 1)

        print("\n********************* Durations *********************")
        print(f"Time extension = {time_extension}")
        print(f"Enhanced duration of path 1: {formatted_path1_enhanced_duration} sec")
        print(f"Enhanced duration of path 2: {formatted_path2_enhanced_duration} sec")

        return formatted_path1_enhanced_duration, formatted_path2_enhanced_duration

    except Exception as e:
        raise Exception("Hata Olustu: " + str(e))