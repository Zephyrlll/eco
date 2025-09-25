import sys, string, psutil
from ..utils.utils import unit_fmt

# 地球ステータス
def display_status(self):
    s = self.status
    def u(x):
        return unit_fmt(x)
    # 表示部分
    line = (
        f"{int(s['年']):6d}年{int(s['月']):2d}月{int(s['日']):2d}日"
        f"窒素:{u(s['窒素']).ljust(7)}二酸化炭素:{u(s['二酸化炭素']).ljust(7)}酸素:{u(s['酸素']).ljust(7)}"
        f"有機物:{u(s['有機物']).ljust(7)} 無機物{u(s['無機物']).ljust(7)} 水{u(s['水']).ljust(7)}"
        f"バクテリア:{u(s['バクテリア']).ljust(7)}微生物:{u(s['微生物']).ljust(7)}菌:{u(s['菌']).ljust(7)}"
        f"植物:{u(s['植物']).ljust(7)}草食動物:{u(s['草食動物']).ljust(7)}肉食動物:{u(s['肉食動物']).ljust(7)}人間:{u(s['人間']).ljust(7)}家畜:{u(s['家畜']).ljust(7)}"
    )

    # 災害表示
    # 災害中なら災害名と残り日数を表示
    if self.envsys.hazards:
        hazards_str = ", ".join([f"{hz.name} 残り({hz.days})日" for hz in self.envsys.hazards])
    else:
        hazards_str = "なし"
    line += f" 災害:{hazards_str}"

    sys.stdout.write("\r" + line + " " * 20)
    sys.stdout.flush()

# 生態毎種類数
def display_kids(self, kind):
    arr = self.kinds[kind]
    letters = list(string.ascii_uppercase)
    parts = []
    for i in letters:
        parts.append(f"{i}:{str(unit_fmt(arr.count(i))).ljust(6)}")
    sys.stdout.write("\r" + kind + " " + " ".join(parts))
    sys.stdout.flush()

# 大気成分
def display_atmosphere(self):
    s = self.status
    vals = [s["窒素"], s["二酸化炭素"], s["酸素"]]
    total = sum(vals) if sum(vals) else 1.0
    ratio = [v / total * 100 for v in vals]
    line = f"    窒素:{ratio[0]:.1f}%    二酸化炭素:{ratio[1]:.1f}%    酸素:{ratio[2]:.1f}%"
    sys.stdout.write("\r" + line.center(230))
    sys.stdout.flush()

# ハードウェア情報
def display_hardware(self):
    cpu_now = psutil.cpu_percent(interval=0.25)
    self.cpu_window.append(float(cpu_now))
    cpu_avg = sum(self.cpu_window) / len(self.cpu_window)
    cpu_max = max(self.cpu_window)
    mem = psutil.virtual_memory().percent
    line = f"CPU: NOW.{cpu_now:5.1f}%   AVG.{cpu_avg:5.1}%   MAX.{cpu_max:5.1f}   Memory: {mem:5.1f}%"
    sys.stdout.write("\r" + line.center(230))
    sys.stdout.flush()