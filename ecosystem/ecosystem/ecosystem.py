from ..entities.entities import Bacteria, Microorganisms, Fungus, Plant, Herbivore, Carnivore, Human
from ..entities.entities import Composer
from ..environment.environment import EnvironmentSystem, Drought, Flood, Wildfire, Earthquake
from ..civilization.civilization import Civilization
from ..earth.earth import EarthCondition
# from ..utils.utils import unit_fmt
# from ..display.display import display_atmosphere, display_hardware, display_kids, display_status
# from ..other.other import autosave_tick, csv_log, save

import string, configparser

s = Composer.the_beginning_of_ecology
b = Composer.the_second_stage

'''
・ローマ字禁止
・外部から直接使わないメソッド名は_から始める。for文も同様に
・なるべく組み込み関数使う
・冗長を許す
・デコレーターなるべく使う
'''

#===ANSI colors===
RED = '\033[31m'
CYAN = '\033[36m'
END = '\033[0m'
#===ターミナルのパス表示削除===
print("\033[2A                                                                                                                                                                               ")



class Ecosystem:
    '''
    生態系シミュレータの基盤
    '''
    def __init__(self, earth_status, society):
        config = configparser.ConfigParser()
        config.read(r"C:\Users\admin\Documents\生態系\ecosystem_simulator\config.ini", encoding="utf-8")
        self.config = config["OptimalEarthCondition"]
        '''
        # デフォルトステータス
        default_status = {
            "年": 0, "月": 0, "日": 1,
            "窒素": 1000000, "酸素": 0, "二酸化炭素": 1000000,
            "水": 1000000, "有機物": 1000000, "無機物": 1000000,
            "バクテリア": 0, "微生物": 0, "菌": 0,
            "植物": 0, "草食動物": 0, "肉食動物": 0,
            "人間": 0, "家畜": 0
        }
        '''
        # self.status = default_status.copy()
        self.status = earth_status
        # self.status.update(earth_status)
        self.society = society
        self.civ = Civilization(society)
        # ここでシビア度を変えられる。iniで設定できるようにしたい。 --多分実装できた
        self.earth = EarthCondition(
            temperature=float(self.config["temperature"]), # 平均気温
            lowest_temperature=float(self.config["lowest_temperature"]), # 最低気温
            maximum_temperature=float(self.config["maximum_temperature"]), # 最高気温
            pollution_degree=float(self.config["pollution_degree"]), # 汚染度
        )
        self._env_effects = {"metabolism": 1.0, "birth": 1.0, "mortality":1.0}# 代謝、出生、死亡率

        # シミュレーションconfig
        self.kill_target = [100,0, 0, 0,  0, -1, -1] # 各生態の捕食対象の1日の狩り数
        self.drink_water = [100,0, 0, -1, -1, -1] # 上の水版 --ほんとはがっつり動的にしたいけど一旦randomで疑似的に
        kindsSTR = string.ascii_letters # 生態にA~Zでタグ付け。下は確率機
        self.kindsSTR = list(kindsSTR[26:])
        self.kindsSTR_weights = [10000,4000,3000,2000,1500,1300,1200,1100,1000,900,
        800,700,600,500,500,300,300,150,150,75,75,50,25,10,1,0.1]# 数値が低いほど出ずらい。A~Zの26に対応する。
        

        # 生態発生条件
        # これらがないと発生しない。植物以降、その手前のものが存在していない限り発生しない。食物連鎖を維持する。
        self.needs = {
            "バクテリア":['水','有機物'],
            "微生物":['酸素','有機物','水','無機物'],
            "菌":['酸素', '水', 'バクテリア','有機物','無機物'],
            "植物":['酸素','二酸化炭素','無機物','窒素','水'],
            "草食動物":['酸素','二酸化炭素','植物','有機物','無機物','水','窒素'],
            "肉食動物":['酸素','二酸化炭素','草食動物','有機物','無機物','水','窒素'],
            "人間":['酸素','二酸化炭素','植物','有機物','無機物','水','窒素','草食動物','肉食動物'],
            "家畜":['酸素','二酸化炭素','植物','有機物','無機物','水','窒素','人間']
        }

        # 生態発生確率
        #[1,0,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,0,0,0,0,0,0,0,0,0,0,00,,00,0........]みたいな感じ
        #ここのバランス調整が難しすぎる
        self.POO = {
            "バクテリア": [1] + [0 for _ in range(1000)],
            "微生物": [1] + [0 for _ in range(100)],
            "菌": [1] + [0 for _ in range(100)],
            "植物": [1] + [0 for _ in range(1)],
            "草食動物": [1] + [0 for _ in range(1)],
            "肉食動物": [1] + [0 for _ in range(1)],
            "人間": [1] + [0 for _ in range(1)],
            "ランダム": [0, 1, -1]
        }

        # タグ付け済み生物の保存先
        self.kinds = {k: [] for k in ["バクテリア", "微生物", "菌", "植物", "草食動物", "肉食動物", "人間"]}
        '''
        self.kinds = {
            "バクテリア": [],
            "微生物": []
            .
            .
        }
        '''

        # 生態の概念追加とjpname(日本語名)を付与しリスト化
        self.entities = [
            Bacteria("バクテリア"), Microorganisms("微生物"), Fungus("菌"),
            Plant("植物"), Herbivore("草食動物"), Carnivore("肉食動物"), Human("人間")
        ]

        # シミュレーション時の機能用変数
        self.cpu_window = []             # for hardware display
        self.save_frequency = 500        # for auto save
        self._save_counter = 0           # for auto save
        self._loop_counter = 0           # for auto save and option recommends
        self._cpu_avg_for_recommend = [] # for option recommends
        self._caf_rate = 0.0             # for option recommends

        # 地球環境用
        self.envsys = EnvironmentSystem(self, hemisphere="north")
        self.season = self.envsys.season

    # 他クラスからのアクセサとして
    def get_status(self):
        return self.status
    
    # ---シミュレーションコア----

    # 日付計算
    def advance_day(self):
        s = self.status
        s["日"] += 1
        if s["日"] >= 30:
            if s["月"] >= 12:
                s["年"] += 1
                s["月"] = 1
            else:
                s["月"] += 1
            s["日"] = 1

    # 寿命
    '''
    複雑化してしまった。
    人間の寿命は文明レベル(Society)によって上下する。高いほど長生きしやすい。
    base =  Society→"6.0": 1.0←寿命係数    これを基準にSocietyに伴って寿命が下がる。
    .get(self.society, 0.75)で現在のsocietyを基に寿命係数をゲットする。念のため辞書にない場合は0.75を返す。
    env = self._env_effects.get("mortality", 1.0) で環境の死亡率を取得。これも念のため1.0を返す。
    human_survive = (0.5 * base) + (0.5 * base * env) で人間の生存率を計算。baseとenvの平均を取っている。
    例えばbaseが0.8、envが0.5なら(0.5*0.8)+(0.5*0.8*0.5)=0.4+0.2=0.6となる。
    これを人間の寿命にかける。s["人間"] *= 0.95*human_survive
    例えば上の例なら0.95*0.6=0.57となり、人間は1年で43%死ぬことになる。
    他の生態は環境の死亡率のみで決まる。例えばenvが0.5なら50%死ぬ。
    人間に関しては結構シビアかもしれない。ただSocietyが6.0であれば逆に減りが少ないかも？難しい
    '''
    def lifespan_tick(self):
        s = self.status
        # 文明レベル係数(高いほど医療技術や食糧が充実するため)
        base = {"6.0": 1.0, "5.0": 0.95, "4.0": 0.9, "3.0": 0.8, "2.0": 0.75, "1.0": 0.7}.get(self.society, 0.75)
        # 環境の死亡係数(悪いほど小さい)
        env = self._env_effects.get("mortality", 1.0)
        # env < 1 で死亡強化
        human_survive = (0.5 * base) + (0.5 * base * env)
        s["人間"] *= 0.95*human_survive
        s["肉食動物"] *= 0.6*env
        s["草食動物"] *= 0.7*env
        s["植物"] *= 0.95*env

    # Society2以上で家畜が生成
    def domestication_tick(self):
        s = self.status
        if s["人間"]:
            if self.society in {"2.0", "3.0", "4.0", "5.0", "6.0"}:
                s["家畜"] += 0.1 * s["人間"]

    # 植物がなかなか増えないので機械的にブースト
    def small_plant_boost(self):
        s = self.status
        if abs(s["植物"]) >= 1 and abs(s["植物"]) < 20:
            s["植物"] += 3

    # 一日の流れ
    def step(self):
        '''
        上のメソッドを見ながら理解する。複雑化してしまったがこれでいい。
        '''
        # 文明進行
        if self.status["人間"]:
            self.society = self.civ.calculate(self.status["人間"])

        # 環境の更新
        self.envsys.apply_pre()

        # 地球環境からペナルティ係数を更新
        self._env_effects = self.earth.effects(self.status)
        base_effects = self.earth.effects(self.status)

        # 季節天気災害の係数を乗算
        ext = self.envsys.multipliers()
        '''
        例えば、max(0.1, min(2.0, 0.8 * 1.2)) = 0.96
        0.1は最低値。例えば右が0.01とかになっても0.1になる。
        2.0は最高値。例えば右が3.0とかになっても2.0になる。
        '''
        self._env_effects = {
            "metabolism": max(0.1, min(2.0, base_effects["metabolism"] * ext["metabolism"])),
            "birth":      max(0.1, min(2.0, base_effects["birth"] * ext["birth"])),
            "mortality":  max(0.1, min(2.0, base_effects["mortality"] * ext["mortality"])),
        }

        # 時の流れ
        self.advance_day()

        # 各生態の働き
        for i in self.entities:
            i.act(self)

        # 寿命
        if self.status["日"] == 29:
            self.lifespan_tick()
        self.domestication_tick()
        self.small_plant_boost()


        
    #@
    # 環境をセットする。
    # def set_environment(self, *, temperature=None, lowest_temperature=None, maximum_temperature=None, pollution_degree=None):
    #     if temperature is not None:
    #         self.earth.temperature = float(temperature)

    #     if lowest_temperature is not None:
    #         self.earth.lowest_temperature = float(lowest_temperature)

    #     if maximum_temperature is not None:
    #         self.earth.maximum_temperature = float(maximum_temperature)

    #     if pollution_degree is not None:
    #         self.earth.pollution_degree = float(pollution_degree)
