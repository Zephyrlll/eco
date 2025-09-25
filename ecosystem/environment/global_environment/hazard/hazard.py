class Hazard:
    import configparser
    config = configparser.ConfigParser()
    config.read(r"C:\Users\admin\Documents\生態系\ecosystem_simulator\config.ini", encoding="utf-8")

    # 影響日数
    def __init__(self, days=1, name="Hazard"):
        self.days = days
        self.name = name

    # daysが減っても継続するならTrue
    def tick(self):
        self.days -= 1
        return self.days > 0
    
    def effect(self):
        return ({}, {"metabolism": 1.0, "birth": 1.0, "mortality": 1.0}, 0.0, 0.0)
    
class Drought(Hazard): # 干ばつ
    def __init__(self, days=10, config=None):
        super().__init__(days, name="干ばつ")
        self.config = config["Drought"]

    def effect(self):
        return (
            {"窒素": float(self.config["窒素"]), "酸素": float(self.config["酸素"]), "二酸化炭素": float(self.config["二酸化炭素"]), "水": float(self.config["水"]), "有機物": float(self.config["有機物"]), "無機物": float(self.config["無機物"]), "バクテリア": float(self.config["バクテリア"]), "微生物": float(self.config["微生物"]), "菌": float(self.config["菌"]), "植物": float(self.config["植物"]), "草食動物": float(self.config["草食動物"]), "肉食動物": float(self.config["肉食動物"]), "人間": float(self.config["人間"])},
            {"metabolism": float(self.config["metabolism"]), "birth": float(self.config["birth"]), "mortality": float(self.config["mortality"])},
            float(self.config["temperature"]),
            float(self.config["pollution"])
        )
class Flood(Hazard): # 洪水
    def __init__(self, days=10, config=None):
        super().__init__(days, name="洪水")
        self.config = config["Flood"]

    def effect(self):
        return (
            {"窒素": float(self.config["窒素"]), "酸素": float(self.config["酸素"]), "二酸化炭素": float(self.config["二酸化炭素"]), "水": float(self.config["水"]), "有機物": float(self.config["有機物"]), "無機物": float(self.config["無機物"]), "バクテリア": float(self.config["バクテリア"]), "微生物": float(self.config["微生物"]), "菌": float(self.config["菌"]), "植物": float(self.config["植物"]), "草食動物": float(self.config["草食動物"]), "肉食動物": float(self.config["肉食動物"]), "人間": float(self.config["人間"])},
            {"metabolism": float(self.config["metabolism"]), "birth": float(self.config["birth"]), "mortality": float(self.config["mortality"])},
            float(self.config["temperature"]),
            float(self.config["pollution"]),
        )
class Wildfire(Hazard): # 山火事
    def __init__(self, days=10, config=None):
        super().__init__(days, name="山火事")
        self.config = config["Wildfire"]

    def effect(self):
        return (
            {"窒素": float(self.config["窒素"]), "酸素": float(self.config["酸素"]), "二酸化炭素": float(self.config["二酸化炭素"]), "水": float(self.config["水"]), "有機物": float(self.config["有機物"]), "無機物": float(self.config["無機物"]), "バクテリア": float(self.config["バクテリア"]), "微生物": float(self.config["微生物"]), "菌": float(self.config["菌"]), "植物": float(self.config["植物"]), "草食動物": float(self.config["草食動物"]), "肉食動物": float(self.config["肉食動物"]), "人間": float(self.config["人間"])},
            {"metabolism": float(self.config["metabolism"]), "birth": float(self.config["birth"]), "mortality": float(self.config["mortality"])},
            float(self.config["temperature"]),
            float(self.config["pollution"]),
        )  
class Earthquake(Hazard): # 地震
    def __init__(self, days=10, config=None):
        super().__init__(days, name="地震")
        self.config = config["Earthquake"]

    def effect(self):
        return (
            {"窒素": float(self.config["窒素"]), "酸素": float(self.config["酸素"]), "二酸化炭素": float(self.config["二酸化炭素"]), "水": float(self.config["水"]), "有機物": float(self.config["有機物"]), "無機物": float(self.config["無機物"]), "バクテリア": float(self.config["バクテリア"]), "微生物": float(self.config["微生物"]), "菌": float(self.config["菌"]), "植物": float(self.config["植物"]), "草食動物": float(self.config["草食動物"]), "肉食動物": float(self.config["肉食動物"]), "人間": float(self.config["人間"])},
            {"metabolism": float(self.config["metabolism"]), "birth": float(self.config["birth"]), "mortality": float(self.config["mortality"])},
            float(self.config["temperature"]),
            float(self.config["pollution"]),
        )