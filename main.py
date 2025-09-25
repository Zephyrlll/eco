from pathlib import Path

from ecosystem.ecosystem.ecosystem import Ecosystem
from ecosystem.environment.environment import Drought, Flood, Wildfire, Earthquake
from ecosystem.utils.utils import load_status
from ecosystem.mainloop.mainloop import run_simulation, run_simulation_compact

import configparser


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.ini"
SAVE_PATH = BASE_DIR / "save.json"


config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8")
compactmode = config["Simulator"].get("compact", "0")



if __name__ == "__main__":
    # セーブ読み込み
    status, hazards_data = load_status(str(SAVE_PATH))
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
            eco.envsys.add_hazard(cls(days=hz["days"], config=config))
            
    if compactmode == "1":
        run_simulation_compact(eco)
    else:
        run_simulation(eco)