# Civilization
人類の文明レベルを現実のSocityレベル的に管理する

## function
- __init__
- calculate
- should_advance
- activities

## variable
- self.level
- soc
- population
- scale
- base
- main
- sub

## must-see
- should_advanceについて\
if 人口 が0人なら、文明レベル云々以前。
1 以上なら希望、base = max(int(scale(後述) // max(1, 人口)), 1)
return 例えば今soc=5.0なら,1000000000000000000 分の 1 * 人口で進化(baseはここの処理で使う)

- calculate()の流れ\
現在のSocietyを取得\
↓\
if soc == "1.0" and should_advance(1_000_000):
    soc = "2.0"
ここで、should_advanceが使用され、should_advanceの引数'base'はこの確率用の数値である。\
↓\
最新のsocを返す。


