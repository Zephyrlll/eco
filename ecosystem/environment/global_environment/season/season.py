class SeasonSystem:
    def __init__(self, hemisphere):
        # 半球
        self.hemisphere = hemisphere

    # 半球ごと月をずらす
    def _nomalize_month(self, month):
        m = int(month)
        if self.hemisphere == "south":
            m = ((m + 6 - 1) % 12) + 1
        return m
    
    # 月を基に季節を設定
    def detect(self, month):
        m = self._nomalize_month(month)
        if m in (3, 4, 5):
            return "spring"
        elif m in (6, 7, 8):
            return "summer"
        elif m in (9, 10, 11):
            return "fall"
        else:
            return "winter"

    # 季節ごとの影響
    def _spring(self):
        return {"metabolism": 1.05, "birth": 1.15, "mortality": 0.95}, + 1.0

    def _summer(self):
        return {"metabolism": 1.10, "birth": 1.00, "mortality": 1.00}, + 2.0

    def _fall(self):
        return {"metabolism": 1.00, "birth": 0.95, "mortality": 1.00}, - 0.5

    def _winter(self):
        return {"metabolism": 0.90, "birth": 0.85, "mortality": 1.00}, - 2.0
    
    # 影響を反映するために
    def effect(self, month):
        s = self.detect(month)
        if s == "spring":
            return self._spring()
        elif s == "summer":
            return self._summer()
        elif s == "fall":
            return self._fall()
        else:
            return self._winter()