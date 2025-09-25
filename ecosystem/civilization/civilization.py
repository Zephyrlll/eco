import random
class Civilization:
    '''
    人類の文明レベルを現実のSocietyレベルのように管理するクラス。
    '''
    # 初期化
    def __init__(self, level):
          self.level = level
    
    # Societyレベル進捗計算
    def calculate(self, population):
        soc = self.level
        def should_advance(scale):
            if population <= 0:
                return False
            base = max(int(scale // max(1, population)), 1)
            return random.choices([0, 1], weights=[base, 1])[0] == 1

        # 右の値分の1の確率で進化する。人口が少ないとほぼ無理
        if soc == "1.0" and should_advance(1_000_000):
            soc = "2.0"
        elif soc == "2.0" and should_advance(1_000_000_000):
            soc = "3.0"
        elif soc == "3.0" and should_advance(1_000_000_000_000):
            soc = "4.0"
        elif soc == "4.0" and should_advance(1_000_000_000_000_000):
            soc = "5.0"
        elif soc == "5.0" and should_advance(1_000_000_000_000_000_000):
            soc = "6.0"
        self.level = soc
        return soc
    
    # Societyレベルごとの活動 --未実装
    def activities(self):
        soc = self.level
        if soc == "1.0":
            main = ("野生動物狩り", "山菜狩り")
            sub = ()

        elif soc == "2.0":
            main = ("農業")
            sub = ("家畜", "山菜狩り", "集団生活")

        elif soc == "3.0":
            main = ("工業", "集団生活")
            sub = ("家畜", "山菜狩り","農業")

        elif soc == "4.0":
            main = ("情報", "集団生活", "工業")
            sub = ("家畜", "山菜狩り", "農業", "サイバー空間")

        elif soc == "5.0":
            main = ("AI", "集団生活", "情報", "サイバー空間")
            sub = ("家畜", "山菜狩り", "農業")

        elif soc == "6.0":
            main = ("AI", "宇宙", "情報", "サイバー空間")
            sub = ("家畜", "集団生活", "山菜狩り", "農業")

        return main, sub