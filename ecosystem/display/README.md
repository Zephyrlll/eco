# Display
メインループ中の、表示情報を定義する。クラスは使用しないが、明らかにカテゴリとして確立できたのでファイル分割をする。

## function
- display_status\
地球上の生態の数などを表示
- display_kinds\
各種、A~Zのタグをつけて保存する仕組みがあるので、それを表示
- display_atmosphere\
窒素、二酸化炭素、酸素の割合を表示
- display_hardware\
cpuやmemoryの状態を表示する

## variable
### display_status
- s\
現在の地球状態を取得し保存
- line\
表示する内容を定義
- hazards_str\
災害状況を保存

### display_kinds
- arr\
種類の数をリアルタイム取得し保存
- letters\
a~Zを定義
- parts\
空リストで表示用にあとで使う

### display_atmosphere
- s\
上と同じ
- vals\
s(最新の地球状態)をもとに[窒素,二酸化炭素,酸素]というリストを保存(実際は数値が入る)
- total\
ややこしいのでmust-seeで記述
- ratio\
ややこしいのでmust-seeで記述
- line\
上に同じ

### display_hardware
- cpu_now
- cpu_avg
- cpu_max
- mem
- line\
全ていうまでもない

## must-see
- display_atmosphereについて
```python
s = self.status
vals = [s["窒素"], s["二酸化炭素"], s["酸素"]]
total = sum(vals) if sum(vals) else 1.0
ratio = [v / total * 100 for v in vals]
```
s = 最新の地球状態\
vals = 大気成分の最新の値のみ入ったリストを生成\
total = もし合計がFalseであれば1.0を返し、Trueであればそのまま返すセーフティな仕組み\
ratioは、例えば[窒素 二酸化炭素, 酸素]が[100, 50, 50]とあったとき、\
100 / 200 * 100 = 50\
50 / 200 * 100 = 25\
50 / 200 * 100 = 25\
ratio = [50, 25, 25]となる。\
line = f"窒素:[ratio[0]:.1f]% .....となり以下のように表示される
```
    窒素:50%    二酸化炭素:25%    酸素:25%
```