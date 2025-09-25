import random
from .global_environment.season.season import SeasonSystem
from .global_environment.weather.weather import WeatherSystem
from .global_environment.hazard.hazard import Hazard, Flood, Earthquake, Drought, Wildfire


class EnvironmentSystem:
    def __init__(self, eco, hemisphere):
        self.eco = eco
        self.season = SeasonSystem(hemisphere)
        self.weather = WeatherSystem("clear")
        self.hazards = []
        # 実効係数
        self._last_mult = {"metabolism": 1.0, "birth": 1.0, "mortality": 1.0}

    def set_hemisphere(self, hemisphere):
        self.season.hemisphere = hemisphere

    def set_weather(self, w):
        self.weather.set(w)

    def clear_weather(self):
        self.weather.clear()

    def add_hazard(self, hz):
        self.hazards.append(hz)

    # 1日分の集計
    def _aggregate(self):
        month = int(self.eco.status.get("月", 1))
        # 季節
        s_mult, s_temp, = self.season.effect(month)
        # 天気
        w_delta, w_mult, w_temp, w_pol = self.weather.effect()
        # 災害
        d_status = dict(w_delta)
        mult = {
            "metabolism": s_mult["metabolism"] * w_mult["metabolism"],
            "birth": s_mult["birth"] * w_mult["birth"],
            "mortality": s_mult["mortality"] * w_mult["mortality"],
        }
        temp_offset = s_temp + w_temp
        pol_delta = w_pol

        alive_haz = []
        for hz in self.hazards:
            h_ds, h_m, h_t, h_p = hz.effect()
            for k, v in h_ds.items():
                d_status[k] = d_status.get(k, 0.0) + v
            for k in mult:
                mult[k] *= h_m.get(k, 1.0)
            temp_offset += h_t
            pol_delta += h_p
            if hz.tick():
                alive_haz.append(hz)
        self.hazards = alive_haz

        # 係数の下限上限の安全課
        for k in mult:
            mult[k] = max(0.1, min(2.0, mult[k]))
        temp_offset = max(-10.0, min(10.0, temp_offset))
        pol_delta = max(-0.2, min(0.2, pol_delta))
        return d_status, mult, temp_offset, pol_delta
    
    # Ecosystem.step()の冒頭で呼ぶ、地球/資源の前処理
    def apply_pre(self):
        ds, mult, toff, pdel = self._aggregate()
        s = self.eco.status
        
        # 資源・個体群の加算(必要なもののみ)
        for k, v in ds.items():
            if k in s:
                s[k] += v

        # 地球の状態を微調整
        self.eco.earth.temperature = float(self.eco.earth.temperature) + toff
        self.eco.earth.pollution_degree = max(0.0, min(1.0, float(self.eco.earth.pollution_degree) + pdel))

        # 一旦保持してEarthCondition.effectsのあと掛け合わせる
        self._last_mult = mult

    # EarthCondition.effects()の結果にさらに掛ける
    def multipliers(self):
        return dict(self._last_mult)