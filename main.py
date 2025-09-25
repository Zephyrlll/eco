from ecosystem.ecosystem.ecosystem import Ecosystem
from ecosystem.environment.environment import Drought, Flood, Wildfire, Earthquake
from ecosystem.utils.utils import load_status
from ecosystem.mainloop.mainloop import run_simulation, run_simulation_compact

import configparser
config = configparser.ConfigParser()
config.read(r"C:\Users\admin\Documents\生態系\ecosystem_simulator\config.ini", encoding="utf-8")
compactmode = config["Simulator"]["compact"]



if __name__ == "__main__":

    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini', encoding='utf-8')

    # セーブ読み込み
    status, hazards_data = load_status('save.json')
    # インスタンス
    eco = Ecosystem(status, society="2.0")

    # 災害復元
    name_to_class = {
        "干ばつ": Drought,
        "洪水": Flood,
        "山火事": Wildfire,
        "地震": Earthquake,
    }
    for hz in hazards_data:
        cls = name_to_class.get(hz["name"])
        if cls:
            eco.envsys.add_hazard(cls(days=hz["days"]))
            
    if compactmode == "1":
        run_simulation_compact(eco)
    else:
        run_simulation(eco)