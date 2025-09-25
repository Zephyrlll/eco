import time
import psutil
import keyboard
import subprocess
import sys
from pathlib import Path

from ..display.display import display_atmosphere, display_hardware, display_kids, display_status
from ..other.other import save, autosave_tick, csv_log

import configparser


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.ini"


config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8")
compactmode = config["Simulator"].get("compact", "0")

if compactmode == "1":
    from ..display.display_compact import display_status_ecology, display_status_other, display_atmosphere, display_hardware
else:
    from ..display.display import display_atmosphere, display_hardware, display_kids, display_status


# ゴッドモード
def godmode(eco):
    eco.status["植物"] += 1000000
    eco.status["草食動物"] += 1000000
    eco.status["肉食動物"] += 1000000
    eco.status["人間"] += 1000000


def run_simulation(eco): # not compact mode
    while True:
        eco._loop_counter += 1
        autosave_tick(eco)
        if eco._loop_counter % 10 == 0:
            csv_log(eco)

        if keyboard.is_pressed("1"):
            eco.step(); display_kids(eco, "バクテリア")
        elif keyboard.is_pressed("2"):
            eco.step(); display_kids(eco, "微生物")
        elif keyboard.is_pressed("3"):
            eco.step(); display_kids(eco, "菌")
        elif keyboard.is_pressed("4"):
            eco.step(); display_kids(eco, "植物")
        elif keyboard.is_pressed("5"):
            eco.step(); display_kids(eco, "草食動物")
        elif keyboard.is_pressed("6"):
            eco.step(); display_kids(eco, "肉食動物")
        elif keyboard.is_pressed("7"):
            eco.step(); display_kids(eco, "人間")
        elif keyboard.is_pressed("a"):
            eco.step(); display_atmosphere(eco)
        elif keyboard.is_pressed("h"):
            eco.step(); display_hardware(eco)
        elif keyboard.is_pressed("q"):
            save(eco, '../save.json')
            subprocess.Popen([sys.executable, "main.py"])
            sys.exit()
            break
        elif keyboard.is_pressed("g"):
            eco.step(); godmode(eco); display_status(eco)
        # elif keyboard.is_pressed("o"):
        #     eco.step(); display_kids(eco, )
        else:
            eco.step(); display_status(eco)

        if eco._loop_counter % 1000 == 0:
            cpu_now = psutil.cpu_percent(interval=0.1)
            eco._cpu_avg_for_recommend.append(float(cpu_now))
            eco._caf_rate = sum(eco._cpu_avg_for_recommend) / len(eco._cpu_avg_for_recommend)

        # 保険
        if eco._loop_counter % 2 == 0:
            time.sleep(0.001)



def run_simulation_compact(eco): # compact mode
    while True:
        eco._loop_counter += 1
        autosave_tick(eco)
        if eco._loop_counter % 10 == 0:
            csv_log(eco)

        if keyboard.is_pressed("o"):
            eco.step(); display_status_other(eco)
        elif keyboard.is_pressed("a"):
            eco.step(); display_atmosphere(eco)
        elif keyboard.is_pressed("h"):
            eco.step(); display_hardware(eco)
        elif keyboard.is_pressed("q"):
            save(eco, '../save.json')
            subprocess.Popen([sys.executable, "main.py"])
            sys.exit()
            break
        elif keyboard.is_pressed("g"):
            eco.step(); godmode(eco); display_status(eco)
        # elif keyboard.is_pressed("o"):
        #     eco.step(); display_kids(eco, )
        else:
            eco.step(); display_status_ecology(eco)

        if eco._loop_counter % 1000 == 0:
            cpu_now = psutil.cpu_percent(interval=0.1)
            eco._cpu_avg_for_recommend.append(float(cpu_now))
            eco._caf_rate = sum(eco._cpu_avg_for_recommend) / len(eco._cpu_avg_for_recommend)

        # 保険
        if eco._loop_counter % 2 == 0:
            time.sleep(0.001)