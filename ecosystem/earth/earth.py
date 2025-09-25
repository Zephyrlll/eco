class EarthCondition:
    '''
    地球の環境から、生態活動へ与える補正を計算する。
    減点方式で、ペナルティとなる係数を返す。
    最低でも0.1倍までしか下がらない。
    '''
    # 現状デフォルトしか使わないけど、初期値を現実ライクに。
    def __init__(self, temperature=14.0, lowest_temperature=-60.0, maximum_temperature=50.0, pollution_degree=0.0):
        self.temperature = float(temperature)
        self.lowest_temperature = float(lowest_temperature)
        self.maximum_temperature = float(maximum_temperature)
        self.pollution_degree = float(pollution_degree)

    # ギャップをもとにペナルティの係数を返す
    @staticmethod
    def _gap_to_coef(gap, soft=10.0, hard=50.0, floor=0.1):
        '''
        gap: 最適からのずれ
        soft: ここから減衰
        hard: ここでfloorまで低下
        '''
        if gap <= soft:
            return 1.0
        if gap >= hard:
            return floor
        
        span = hard - soft
        rate = (gap - soft) /span
        return max(floor, 1.0 - (1.0 - floor) * rate)
    

    # 気温によるペナルティ
    def survival_by_temp(self):
        # 最適
        opt_t = 14.0
        opt_lo = -60.0
        opt_hi = 50.0

        # ギャップ
        gt = abs(self.temperature - opt_t)
        gl = abs(self.lowest_temperature - opt_lo)
        gh = abs(self.maximum_temperature - opt_hi)

        # ギャップを元に係数化
        # 例えば気温が24度なら10度ずれているので、gap <= softで1.0、25度なら11でsoft <= gap <= hardでspan=30.0,rate=(11-10)/30=0.3333、max(0.1, 1.0-(1.0-0.1)*0.3333)=0.7なので、係数は0.7になる。
        c_t = self._gap_to_coef(gt, soft=10, hard=50)
        c_lo = self._gap_to_coef(gl, soft=10, hard=50)
        c_hi = self._gap_to_coef(gh, soft=10, hard=50)

        # まとめ
        # 上の11度の例をもとに説明すると、平均以外正常だとして、birthはmax(0.1, min(0.7, 1.0, 1.0))なので0.7。metabolismは(0.7*1.2 + 1.0*0.9 + 1.0*0.9)/3=0.88となる))
        metabolism = max(0.1, (c_t * 1.2 + c_lo * 0.9 + c_hi * 0.9) / 3.0)
        birth      = max(0.1, min(c_t, c_lo, c_hi))
        mortality  = max(0.1, min(c_t, c_lo, c_hi))
        return metabolism, birth, mortality
    
    # 汚染によるペナルティ
    def survival_by_pollution_degree(self, o2_ratio, co2_ratio):
        # 酸素
        if o2_ratio >= 0.20:
            o2_coef = 1.0
        elif o2_ratio >= 0.18:
            o2_coef = 0.8
        elif o2_ratio >= 0.15:
            o2_coef = 0.6
        else:
            o2_coef = 0.3

        # 二酸化炭素
        if co2_ratio <= 0.005:
            co2_coef = 1.0
        elif co2_ratio <= 0.01:
            co2_coef = 0.85
        elif co2_ratio <= 0.03:
            co2_coef = 0.6
        else:
            co2_coef = 0.3

        # 汚染
        pol_coef = max(0.5, 1.0 - 0.5 * max(0.0, min(1.0, self.pollution_degree)))

        # まとめ
        metabolism = min(o2_coef, co2_coef, pol_coef)
        birth      = min(o2_coef, co2_coef, pol_coef)
        mortality  = min(o2_coef, co2_coef, pol_coef)
        return metabolism, birth, mortality
    
    # 影響(ペナルティ係数を統合)
    def effects(self, status):
        # 大気情報を取得。一応なければ0.0
        n2  = float(status.get("窒素", 0.0))
        co2 = float(status.get("二酸化炭素", 0.0))
        o2  = float(status.get("酸素", 0.0))
        # ZeroDivizionErrorにならないように最低でも0.000000001を入れておく
        total = max(1e-9, n2 + co2 + o2)
        o2r = o2r = o2 / total
        co2r = co2 / total

        mt1, br1, mo1 = self.survival_by_temp()
        mt2, br2, mo2 = self.survival_by_pollution_degree(o2r, co2r)

        # 統合してecosystemへ返す
        metabolism = max(0.1, mt1 * mt2)
        birth      = max(0.1, br1 * br2)
        mortality  = max(0.1, mo1 * mo2)
        return {"metabolism": metabolism, "birth": birth, "mortality": mortality}