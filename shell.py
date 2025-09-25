import csv
import subprocess
import sys
import time
from pathlib import Path

import art
import configparser
import keyboard
from rich.console import Console
from rich.table import Table
from rich.progress import track
# for i in track(range(100)):
#     sleep(0.1)  # デモ用


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.ini"
MAIN_PATH = BASE_DIR / "main.py"


config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8")


item = ["窒素", "酸素", "二酸化炭素", "水", "有機物", "無機物",
        "バクテリア", "微生物", "菌", "植物", "草食動物", "肉食動物",
        "人間", "家畜",
        "metabolism", "birth", "mortality",
        "temperature", "pollution"]

Drought = {
    "窒素" : 0.0,
    "酸素" : 0.0,
    "二酸化炭素" : 0.0,
    "水" : -5.0,
    "有機物" : 0.0,
    "無機物" : 0.0,
    "バクテリア" : 0.0,
    "微生物" : 0.0,
    "菌" : 0.0,
    "植物" : -1.0,
    "草食動物" : 0.0,
    "肉食動物" : 0.0,
    "人間" : -1.0,
    "家畜" : 0.0,
    "metabolism" : 0.95,
    "birth" : 0.90,
    "mortality" : 1.05,
    "temperature" : +1.0,
    "pollution" : + 0.01,
}

Flood = {
    "窒素" : 0.0,
    "酸素" : 0.0,
    "二酸化炭素" : 0.0,
    "水" : +10.0,
    "有機物" : 0.0,
    "無機物" : 0.0,
    "バクテリア" : 0.0,
    "微生物" : 0.0,
    "菌" : 0.0,
    "植物" : -2.0,
    "草食動物" : 0.0,
    "肉食動物" : 0.0,
    "人間" : -1.0,
    "家畜" : 0.0,
    "metabolism" : 0.98,
    "birth" : 0.95,
    "mortality" : 1.05,
    "temperature" : +0.5,
    "pollution" : + 0.05,
}

Wildfire = {
    "窒素" : 0.0,
    "酸素" : +1.0,
    "二酸化炭素" : -1.0,
    "水" : -1.0,
    "有機物" : 0.0,
    "無機物" : 0.0,
    "バクテリア" : 0.0,
    "微生物" : 0.0,
    "菌" : 0.0,
    "植物" : -3.0,
    "草食動物" : 0.0,
    "肉食動物" : 0.0,
    "人間" : -1.0,
    "家畜" : 0.0,
    "metabolism" : 1.02,
    "birth" : 0.92,
    "mortality" : 1.08,
    "temperature" : +0.5,
    "pollution" : + 0.05,
}

Earthquake = {
    "窒素" : 0.0,
    "酸素" : 0.0,
    "二酸化炭素" : 0.0,
    "水" : 0.0,
    "有機物" : 0.0,
    "無機物" : 0.0,
    "バクテリア" : 0.0,
    "微生物" : 0.0,
    "菌" : 0.0,
    "植物" : 0.0,
    "草食動物" : 0.0,
    "肉食動物" : 0.0,
    "人間" : -1.0,
    "家畜" : 0.0,
    "metabolism" : 1.0,
    "birth" : 0.95,
    "mortality" : 1.03,
    "temperature" : 0.0,
    "pollution" : 0.0,
}

Hazards = {
            "Drought": Drought,
            "Flood": Flood,
            "Wildfire": Wildfire,
            "Earthquake": Earthquake
        }

def _load_hazard_defaults():
    for hazard_name, values in Hazards.items():
        if hazard_name not in config:
            continue
        section = config[hazard_name]
        for key in values:
            if key in section:
                try:
                    values[key] = float(section[key])
                except ValueError:
                    # 不正値は既存のデフォルトを維持する
                    pass


_load_hazard_defaults()


console = Console()
ascii_art = art.text2art("Ecosystem   Simulator")
banner = console.print(f"{ascii_art}\nhelp()でコマンド一覧を見ることができます。\n", style="bold green")



def make_savefile(text: str = ""):
    # for _ in track(li):
    #     sleep(0.01)  # デモ用
    return "セーブファイルを作成しました。続いて設定を行うには'setup()'を実行してください。"

def setting(hazard_key, hazard_label, use_default):
    if use_default:
        print(f"{hazard_label}の設定をすべてデフォルトで設定しました。")
        return

    print("\n必ずfloat型で入力してください。不正な値を入力した場合はデフォルト値になります。")
    print("デフォルトでよい場合は何も打ち込まずにエンターを押してください。")
    for resource in item:
        current = Hazards[hazard_key][resource]
        raw = input(f"{hazard_label}(default={current}): ")
        if not raw.strip():
            continue
        try:
            Hazards[hazard_key][resource] = float(raw)
        except ValueError:
            print("不正な値が入力されたため、デフォルト値を維持します。")


def _write_hazard_config():
    config.read(CONFIG_PATH, encoding="utf-8")
    for hazard_name, values in Hazards.items():
        if hazard_name not in config:
            config[hazard_name] = {}
        for key, value in values.items():
            config[hazard_name][key] = str(value)
    with CONFIG_PATH.open('w', encoding='utf-8') as configfile:
        config.write(configfile)
    
def setup():
    print("災害の一日あたりの影響を設定を行います。")
    config.read(CONFIG_PATH, encoding="utf-8")
    _load_hazard_defaults()

    prompts = (
        ("Drought", "干ばつ"),
        ("Flood", "洪水"),
        ("Wildfire", "山火事"),
        ("Earthquake", "地震"),
    )

    for idx, (key, label) in enumerate(prompts):
        prefix = "初めに" if idx == 0 else "次に"
        default = input(
            f"{prefix}、{label}の影響を設定します。すべてデフォルトでよい場合は1を打ちエンターを、"
            "カスタムする場合は0を打ちエンターを押してください。: "
        ).strip()
        use_default = default == "1"
        setting(key, label, use_default)

    _write_hazard_config()
    print("設定が完了しました。")

RED = '\033[31m'
CYAN = '\033[36m'
END = '\033[0m'
GREEN = '\033[32m'

def check():
    import shutil, sys
    print("ターミナルサイズを測定します。開始するにはスペースを押し、エンターを押すことで終了できます。")
    while True:
        if keyboard.is_pressed("space"):
            break
        else:
            pass
    while True:
        if keyboard.is_pressed("enter"):
            break
        s = shutil.get_terminal_size()
        w = s.columns
        if w > 240:
            t = f"{CYAN}{w}{"  通常モードで開始できます  ".center(10)}{END}"
            mode = 0
        elif w >= 140:
            t = f"{GREEN}{w}{"コンパクトモードで開始します".center(10)}{END}"
            mode = 1
        else:
            t = f"{RED}{w}{"     最低でも140必要です     ".center(10)}{END}"
        sys.stdout.write(f"\r{t}")
        sys.stdout.flush()
    print("コンパクトモードで設定しました" if mode else "通常モードで設定しました")

    config.read(CONFIG_PATH, encoding="utf-8")
    config["Simulator"]["compact"] = str(mode)
    with CONFIG_PATH.open('w', encoding='utf-8') as configfile:
        config.write(configfile)

def help():
    # Table オブジェクトを作成
    table = Table()

    # カラムを追加
    table.add_column("command", justify="left", style="cyan", no_wrap=True)
    table.add_column("role", justify="left", style="magenta")
    table.add_column("detail", justify="left", style="green")

    # 行を追加
    table.add_row("save('任意')", "セーブファイルを作成", "セーブ作成する場合はまずこれをを行ってください")
    table.add_row("setup()", "configを書き込む", "必ずsave()の後に行ってください。")
    table.add_row("quit()", "終了", "シェルを終了します。")
    table.add_row("check()", "コンソールサイズ測定", "メインでは、ターミナルサイズによって挙動が変わるので、安定化を図ります。")
    table.add_row("start()", "メインを開始", "checkを行ってから始めるとよいです。")

    # 表を表示
    console.print(table)

def quit():
    exit()

def start():
    command = [sys.executable, str(MAIN_PATH)]
    try:
        subprocess.Popen(command)
    except FileNotFoundError:
        print("Pythonの実行ファイルが見つかりませんでした。環境を確認してください。")
    else:
        print("メインシミュレーションを別プロセスで起動しました。")
    

def Shell(banner='', namespace={}):
    import code
    code.interact(banner=banner, local=namespace)  # namespace: dictを渡す

if __name__ == '__main__':
    var = {}  # キー(実行コマンド): メソッドの形で渡す
    # コマンドを設定する
    var["save"] = make_savefile
    var["setup"] = setup
    var["help"] = help
    var["quit"] = quit
    var["start"] = start
    var["check"] = check

    Shell(banner=banner, namespace=var)  # shellの起動




# code.interact(banner=banner, local=local)