
class WeatherSystem:
    def __init__(self, weather):
        self.weather = weather

    def set(self, weather):
        self.weather = weather

    def clear(self):
        self.weather = "clear"
    
    def effect(self):
        w = self.weather
        # 共通設定事項
        delta_status = {
            "水": 0.0,
            "酸素": 0.0,
            "二酸化炭素": 0.0,
            "植物": 0.0,
        }
        mult = {"metabolism": 1.0, "birth": 1.0, "mortality": 1.0}
        # 気温への影響
        temp_offset = 0.0
        # 汚染度への影響
        pol_delta = 0.0

        # ペナルティ係数---
        if w == "clear":# 晴天
            pass

        elif w == "rain":# 雨
            delta_status["水"] += 5.0
            delta_status["植物"] += 0.5
            mult["birth"] *= 1.05
            temp_offset += -0.2
            pol_delta += -0.02

        elif w == "storm":# 嵐
            delta_status["水"] += 8.0
            delta_status["植物"] += -0.5
            mult["mortality"] *= 1.05
            temp_offset += -0.5
            pol_delta += 0.01

        elif w == "snow":# 雪
            delta_status["水"] += 1.0
            mult["metabolism"] *= 0.95
            mult["birth"] *= 0.90
            temp_offset += -2.0
        
        elif w == "heatwave":# 酷暑
            delta_status["水"] += -2.0
            mult["birth"] *= 1.05
            mult["mortality"] *= 1.08
            temp_offset += 3.0
            pol_delta += 0.02

        elif w == "coldwave":# 寒波 
            mult["metabolism"] *= 0.90
            mult["birth"] *= 0.85
            mult["mortality"] *= 1.05
            temp_offset += -3.0

        else:
            pass

        return delta_status, mult, temp_offset, pol_delta