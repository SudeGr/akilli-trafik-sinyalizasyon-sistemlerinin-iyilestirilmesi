import calculations
import traci_configuration as traci


def main():
    try:
        # Sabit zamanli sinyalizasyon icin SUMO simulasyonu calistirilir.
        traci.run_fixed_time_signaling()

        # Iyilestirme algoritmasi calistirilir.
        traci.run_enhanced_signaling()

        # Fuzzy Logic kullanilarak iyilestirilmis sinyalizasyon sisteminin sabit zamanli sinyalizasyon 
        # sistemine gore iyilesme yuzdesini hesaplar.
        calculations.determine_enhancement_success_rate()
    except RuntimeError as e:
        print("Hata olustu:", str(e))


if __name__ == '__main__':
    main()
