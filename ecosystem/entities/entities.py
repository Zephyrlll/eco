import random

# めんどくさいのでここで管理します
'''
r  ->  1日当たりの無機物の数の変動のため
sr ->  1日当たりの低分子有機物の数の変動のため
hr ->  1日当たりの高分子有機物の数の変動のため
l  ->  低分子有機物の発生率
h  ->  高分子有機物(有機物)の発生率
m  ->  微生物の発生率
'''
r = [i for i in range(-10, 20)]
lr = [i for i in range(-15, 1)]
hr = [i for i in range(-5, 1)]
l = [0 for _ in range(1000)] + [1]
h = [0 for _ in range(300)] + [1]
m = [0 for _ in range(100)] + [1]

hs = [i for i in range(-10, 10)]

class Composer:
    def __init__(self, jpname):
        self.jpname = jpname

    # 個体数マイナスはあり得ないから処理(めんどいからここで大気も処理)
    def itsimpossible(self, eco):
        s = eco.status
        if s["窒素"] < 0:
            s["窒素"] = 0
        if s["酸素"] < 0:
            s["酸素"] = 0
        if s["二酸化炭素"] < 0:
            s["二酸化炭素"] = 0
        if s["水"] < 0:
            s["水"] = 0
        if s["有機物"] < 0:
            s["有機物"] = 0
        if s["無機物"] < 0:
            s["無機物"] = 0
        if s["低分子有機物"] < 0:
            s["低分子有機物"] = 0
        if s["バクテリア"] < 0:
            s["バクテリア"] = 0
        if s["微生物"] < 0:
            s["微生物"] = 0
        if s["菌"] < 0:
            s["菌"] = 0
        if s["植物"] < 0:
            s["植物"] = 0
        if s["草食動物"] < 0:
            s["草食動物"] = 0
        if s["肉食動物"] < 0:
            s["肉食動物"] = 0
        if s["人間"] < 0:
            s["人間"] = 0
        if s["家畜"] < 0:
            s["家畜"] = 0
            

    # 生態数がっつり減少
    def ifthereisnpredators(self, eco):
        s = eco.status
        if s["肉食動物"] <= 0.9 and s["草食動物"] <= 0.9:
            s["人間"] //= 3
        elif s["肉食動物"] <= 0.9 or s["草食動物"] <= 0.9:
            s["人間"] //= 2

        if s["草食動物"] <= 0.9:
            s["肉食動物"] //= 3

        if s["植物"] <= 0.9:
            s["草食動物"] //= 3 

        if s["人間"] <= 0.9:
            s["家畜"] //=2
    

    # 低分子有機物の誕生
    def the_beginning_of_ecology(self, eco):
        status = eco.status
        if status["無機物"]:
            P = random.choice(l)
            if P:
                status["無機物"] -= 2
                status["低分子有機物"] += 1
            else:
                status["無機物"] += random.choice(r)


    # 高分子有機物の誕生(これを"有機物"として扱う)
    def the_second_stage(self, eco):
        status = eco.status
        if status["低分子有機物"] > 20:
            P = random.choice(h)
            if P:
                status["低分子有機物"] -= 2
                status["有機物"] += 1
            else:
                status["低分子有機物"] += random.choice(lr)
        

    # 微生物を別枠で制御
    def microbe_born(self, eco):
        status = eco.status
        if status["有機物"]:
            P = random.choice(m)
            if P:
                status["有機物"] += random.choice(hr)
                status["バクテリア"] += 1
            else:
                status["有機物"] += random.choice(hs)


    # 出生
    def process(self, eco):
        name = self.jpname
        status = eco.status
        needs = eco.needs
        POO = eco.POO
        kinds = eco.kinds

        if all([status[i] for i in needs[name]]):
            P = random.choice(POO[name])
            birth_coef = eco._env_effects.get("birth", 1.0)
            incr = 1.0 * birth_coef
            if status[name] > 3:
                # ブーストモード
                status[name] += incr*100
                kinds[name].append(random.choices(eco.kindsSTR, weights=eco.kindsSTR_weights)[0])
            elif P:
                status[name] += incr
                kinds[name].append(random.choices(eco.kindsSTR, weights=eco.kindsSTR_weights)[0])
    
    # 光合成
    def photosynthesis(self, eco):
        name = self.jpname
        s = eco.status
        
        metab = eco._env_effects.get("metabolism", 1.0)
        if name == "バクテリア" and s["バクテリア"]:
            s["酸素"] += 0.1 * s["バクテリア"] * metab
        elif name == "植物" and s["植物"]:
            s["酸素"] += 1 * s["植物"] * metab

    # 呼吸
    def respiration(self, eco):
        name = self.jpname
        s = eco.status
        if s["酸素"] <= 0:
            return
        metab = eco._env_effects.get("metabolism", 1.0)
        if s["酸素"] > 0:
            if name == "バクテリア" and s["バクテリア"]:
                s["酸素"] -= (0.01 * s["バクテリア"]) * metab
                s["二酸化炭素"] += (0.05 * s["バクテリア"]) * metab

            elif name == "微生物" and s['微生物']:
                s["酸素"] -= (0.01 * s["微生物"]) * metab
                s["二酸化炭素"] += (0.05 * s["微生物"]) * metab

            elif name == "菌" and s['菌']:
                s["酸素"] -= (0.01 * s["菌"]) * metab
                s["二酸化炭素"] += (0.05 * s["菌"]) * metab

            elif name == "植物" and s["植物"]:
                s["酸素"] -= (0.1 * s["植物"]) * metab
                s["二酸化炭素"] += (0.1 * s["植物"]) * metab

            elif name == "草食動物" and s["草食動物"]:
                s["酸素"] -= (0.2 * s["草食動物"]) * metab
                s["二酸化炭素"] += (0.3 * s["草食動物"]) * metab

            elif name == "肉食動物" and s["肉食動物"]:
                s["酸素"] -= (0.2 * s["肉食動物"]) * metab
                s["二酸化炭素"] += (0.3 * s["肉食動物"]) * metab

            elif name == "人間" and s['人間']:
                s["酸素"] -= (0.2 * s["人間"]) * metab
                s["二酸化炭素"] += (0.3 * s["人間"]) * metab

    # 食物連鎖
    def alive_or_dead(self, eco):
        name = self.jpname
        s = eco.status
        x = random.choice(eco.kill_target)
        y = random.choice(eco.drink_water)

        if s["人間"] < 1:
             s["家畜"] += x * -100000000

        if name == "草食動物" and s["草食動物"]:
            if s["植物"] > 0:
                s["植物"] += x
            else:
                s["草食動物"] += x

            if s["水"] > 0:
                s["水"] += y
            else:
                s["草食動物"] += y
        
        elif name == "肉食動物" and s["肉食動物"]:
            if s["草食動物"] > 0:
                s["草食動物"] += x
            else:

                s["肉食動物"] += x
            if s["水"] > 0:
                s["水"] += y
            else:
                s["肉食動物"] += y

        elif name == "人間" and s['人間']:
            if eco.society == "1.0":
                if s["草食動物"] > 0:
                    s["草食動物"] += x
                else:
                    s["人間"] += x

                if s["肉食動物"] > 0:
                    s["肉食動物"] += x
                else:
                    s["人間"] += x

                if s["植物"] > 0:
                    s["植物"] += x
                else:
                    s["人間"] += x

                if s["水"] > 0:
                    s["水"] += y
                else:
                    s["人間"] += y

            else:
                if s["植物"] > 0:
                    s["植物"] += x
                else:
                    s["人間"] += x

                if s["水"] > 0:
                    s["水"] += y
                else:
                    s["人間"] += y
                
                if s["家畜"] > 0:
                    s["家畜"] += y * s["人間"]
                else:
                    s["人間"] += x * s["人間"] * 0.1

            
    # work
    def act(self, eco):
        self.process(eco)
        self.photosynthesis(eco)
        self.respiration(eco)
        self.alive_or_dead(eco)
        self.the_beginning_of_ecology(eco)
        self.the_second_stage(eco)
        self.ifthereisnpredators(eco)
        self.itsimpossible(eco)

class Bacteria(Composer):     #バクテリア
        pass
class Microorganisms(Composer):      #微生物
        pass
class Fungus(Composer):     #菌
        pass
class Plant(Composer):     #植物
        pass
class Herbivore(Composer):     #草食動物
        pass
class Carnivore(Composer):     #肉食動物
        pass
class Human(Composer):     #人間
        pass