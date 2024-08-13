import traci

# Ścieżka do pliku konfiguracyjnego SUMO
sumo_cfg = "map.sumocfg"

# Uruchomienie SUMO jako subproces z użyciem TraCI
traci.start(["sumo", "-c", sumo_cfg])

# Przykładowa pętla symulacyjna
for step in range(1000):
    traci.simulationStep()

# Zakończenie połączenia z SUMO
traci.close()
