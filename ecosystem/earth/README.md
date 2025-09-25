# Earth
地球の環境から生態活動へ与える補正を計算する

## function
- _\_\_init\_\__
- _\_gap_to_coef_
- _survival_by_temp_
- _survival_by_pollution_degree_
- _effects_

## variable
### init
- self.tenperature
- self.lowest_temperature
- self.maximum_temperature
- self.pollution_degree

### _gap_to_coef
- sofg
- hard
- floor
- span
- rate

### survival_by_temo
- __opt_t__
- __opt_lo__
- __opt_hi__
- gt
- gl
- gh
- c_t
- c_lo
- c_hi
- metabolism
- birth
- mortality

### survival_by_pollution_degree
- __o2_ratio__
- __co2_ratio__
- o2_coef
- co2_coef
- pol_coef
- metabolism
- birth
- mortality

### effects
- __status__
- n2
- co2
- o2
- total
- o2r
- co2r
- mt1
- br1
- mo1
- mt2
- br2
- mo2
- metabolism
- birth
- mortality

## must-see
最も複雑なコンポーネントなので、earth.pyを見ながら上から見ると良い。\

initでは、初期化を行うが、ここでは地球の最適な温度を定義する。たしかecosystemがこれを呼び出しており、値をconfig.iniから参照するようにしているのでそこで設定することができる。\

_gap_to_coefでは、ギャップをもとにペナルティ係数を返す。
softは10.0、hardは50.0と設定しているが、ここをいじると難易度に直結するかもしれない。\
ここではこの関数を解説しない。下のsurvival_by系でがっつりつかうので、そこで例と同時に見る。\
<hr>

#### survival_by_tempでは、気温によるペナルティを計算する。

```python
opt_t = 14.0
opt_lo = -60.0
opt_hi = 50.0
```
optから見てみる。今気づいたけど、ここで最適を再度設定してしまってるのでどこかで不一致が起きてるかも。ここでは現状の書いてある通り考える。opt_~は、optimalの略で、最適な値を定義する。t,lo,hiは、それぞれ気温の平均、lowest、highestの略だと思えばいい。つまりopt_t = 14.0とは、「最適な平均気温は14度」だと定義している。
<hr>

```python
gt = abs(self.temperature - opt_t)
gl = abs(self.lowest_temperature - opt_lo)
gh = abs(self.maximum_temperature - opt_hi)
```
続いてgは、gapのgで、そのごのt,l,hはそれぞれ上と同じような感じ。例えばgtは気温の現実と最適のギャップ。計算式については、絶対値(現在の気温 - 最適な気温)ということ。値を入れて考えると、現在が30度のとき、30 - 14 = 16、5度のときは、5 - 14 = -9でabsにより9となる。
<hr>

```python
c_t = self._gap_to_coef(gt, soft=10, hard=50)
c_lo = self._gap_to_coef(gl, soft=10, hard=50)
c_hi = self._gap_to_coef(gh, soft=10, hard=50)
```
続いてc_は、係数化計算していき保存する。cはcoefficientの略。ここで先ほどの_gap_to_coefを使っていく。\
例えば気温が24度なら10度ずれているので、gap <= softで1.0、25度なら11でsoft <= gap <= hardでspan=30.0,rate=(11-10)/30=0.3333、max(0.1, 1.0-(1.0-0.1)*0.3333)=0.7なので、係数は0.7になる。
<hr>

```python
metabolism = max(0.1, (c_t * 1.2 + c_lo * 0.9 + c_hi * 0.9) / 3.0)
birth      = max(0.1, min(c_t, c_lo, c_hi))
mortality  = max(0.1, min(c_t, c_lo, c_hi))
```
続いてreturnの上三行については、例を見ればわかりやすい。\
気温が24度なら10度ずれているので、gap <= softで1.0、25度なら11でsoft <= gap <= hardでspan=30.0,rate=(11-10)/30=0.3333、max(0.1, 1.0-(1.0-0.1)*0.3333)=0.7なので、係数は0.7になる。

<hr>
survival_by_pollution_degreeも同じようなもの。
<hr>

### effectsについて
ここでは気温と汚染のペナルティ係数を統合して返す感じ。\
最低でも0.1にとどまる。