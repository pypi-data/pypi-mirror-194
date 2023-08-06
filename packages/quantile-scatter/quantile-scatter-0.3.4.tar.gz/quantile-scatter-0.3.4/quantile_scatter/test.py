
# 分位点散布図 [quantile_scatter]
# 【動作確認 / 使用例】

import sys
import fies
import math
import random
from sout import sout
from ezpip import load_develop
# 分位点散布図 [quantile_scatter]
quantile_scatter = load_develop("quantile_scatter", "../", develop_flag = True)

# ダミーデータ
x_ls = [(4 * random.random() - 2) ** 3
	for _ in range(1000)]
y_ls = [math.sin(x) + random.random() * 0.5
	for x in x_ls]

# 分位点散布図の描画 [quantile_scatter]
data = quantile_scatter.plot(
	x = x_ls,	# 横軸数値リスト
	y = y_ls,	# 縦軸数値リスト
	min_bin_ratio = 1/20,	# 最小グループ割合 (最も小さいグループのレコード数が全体に占める割合)
	ile_ls = [0.25, 0.5, 0.75],	# どこの分位点を出すか
	mean = True,	# 平均も出力する
	show = True,	# False指定でグラフを出力しない (データ集計のみ)
)

# debug
sout(data)

# ダミーデータ
x_ls += [None]
y_ls += [1.3]

# 分位点散布図の描画 [quantile_scatter]
data = quantile_scatter.plot(
	x = x_ls,	# 横軸数値リスト
	y = y_ls,	# 縦軸数値リスト
	min_bin_ratio = 1/20,	# 最小グループ割合 (最も小さいグループのレコード数が全体に占める割合)
	ile_ls = [0.25, 0.5, 0.75],	# どこの分位点を出すか
	mean = True,	# 平均も出力する
	show = True,	# False指定でグラフを出力しない (データ集計のみ)
	missing_values = [None],	# 欠損としてあつかう値の指定
)

# 元データ
from matplotlib import pyplot as plt
plt.scatter(x_ls, y_ls)
plt.show()

# 名義尺度データ
fruits = ['melon', 'cherry', 'apple', 'pomegranate', 'lime', 'quince', 'lychee', 'chirimuya', 'carambola', 'chestnut', 'strawberry', 'granadilla', 'kiwi', 'coconut', 'pawpaw', 'date', 'lemon', 'pineapple', 'pear', 'jujube']
x_ls = [random.choice(fruits)
	for _ in range(1000)]
y_ls = [int(random.choice(x) in "ae")
	for x in x_ls]

# 分位点散布図の描画 [quantile_scatter]
data = quantile_scatter.plot(
	x = x_ls,	# 横軸数値リスト
	y = y_ls,	# 縦軸数値リスト
	min_bin_ratio = 1/20,	# 最小グループ割合 (最も小さいグループのレコード数が全体に占める割合)
	ile_ls = [0.25, 0.5, 0.75],	# どこの分位点を出すか
	mean = True,	# 平均も出力する
	show = True,	# False指定でグラフを出力しない (データ集計のみ)
)


# 欠損値のテスト
fruits = ['melon', 'cherry', 'apple', None]
x_ls = [random.choice(fruits)
	for _ in range(1000)]
y_ls = [(0 if x is None else int(random.choice(x) in "ae"))
	for x in x_ls]

# 分位点散布図の描画 [quantile_scatter]
data = quantile_scatter.plot(
	x = x_ls,	# 横軸数値リスト
	y = y_ls,	# 縦軸数値リスト
	min_bin_ratio = 1/20,	# 最小グループ割合 (最も小さいグループのレコード数が全体に占める割合)
	ile_ls = [0.25, 0.5, 0.75],	# どこの分位点を出すか
	mean = True,	# 平均も出力する
	show = True,	# False指定でグラフを出力しない (データ集計のみ)
	missing_values = [None],	# 欠損としてあつかう値の指定
)
