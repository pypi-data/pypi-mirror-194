
# 分位点散布図 [quantile_scatter]
# 【動作確認 / 使用例】

import sys
import erf
import math
import numpy as np
from sout import sout

# xの型に応じて処理を分岐
def judge_x_type(x_ls, missing_values):
	# 欠損の除去
	clean_x_ls = [x for x in x_ls if x not in missing_values]
	# 文字列かどうかのリスト
	is_str_set = set([(type(x) == type("")) for x in clean_x_ls])
	if len(is_str_set) != 1: raise Exception("[error] Consistency error in the type of x value.")
	return ("nominal" if True in is_str_set else "number")

# 欠損の分離
def div_missing(x_ls, y_ls, missing_values):
	clean_x_ls, clean_y_ls, missing_x_ls, missing_y_ls = [], [], [], []
	for x, y in zip(x_ls, y_ls):
		if x in missing_values:
			missing_x_ls.append(x)
			missing_y_ls.append(y)
		else:
			clean_x_ls.append(x)
			clean_y_ls.append(y)
	return (clean_x_ls, clean_y_ls, missing_x_ls, missing_y_ls)

# 最終groupが下限サイズに満たない場合直前のgroupと統合
def last_group_unify(ret_ls, min_bin_size):
	org_group_n = len(ret_ls)
	# 1group以下のときは処理しない
	if org_group_n <= 1: return ret_ls
	# 最終groupの大きさをチェック
	if len(ret_ls[-1]) < min_bin_size:
		return ret_ls[:-2] + [ret_ls[-2] + ret_ls[-1]]
	return ret_ls

# 数値横軸をグループに分割
def num_grouping(arg_ls, min_bin_ratio):
	data_n = len(arg_ls)
	min_bin_size = math.ceil(data_n * min_bin_ratio)
	@erf(IndexError = "_OUT_OF_RANGE")
	def get_x(i): return arg_ls[i][0]
	ret_ls = []
	prev_idx, idx = 0, min_bin_size
	while True:
		# 終了判定
		if idx > data_n:
			ret_ls.append(arg_ls[prev_idx:idx])
			break
		# 同率の値を同じグループに含める
		if get_x(idx-1) == get_x(idx):
			idx += 1
		else:
			ret_ls.append(arg_ls[prev_idx:idx])
			prev_idx = idx
			idx += min_bin_size
	# 最終groupが下限サイズに満たない場合直前のgroupと統合
	ret_ls = last_group_unify(ret_ls, min_bin_size)
	return ret_ls

# 各名義の出現頻度を調べる
def gen_rank_ls(x_ls):
	cnt_dic = {}
	for x in x_ls:
		if x not in cnt_dic: cnt_dic[x] = 0
		cnt_dic[x] += 1
	rank_ls = [(k, cnt_dic[k]) for k in cnt_dic]
	rank_ls.sort(key = lambda e: e[1], reverse = True)
	return rank_ls

# 横軸値に従ってグルーピング
def x_grouping(x_ls, y_ls, min_bin_ratio, missing_values):
	# xの型に応じて処理を分岐
	x_type = judge_x_type(x_ls, missing_values)
	if x_type == "number":	# 数値
		# 欠損の分離
		div_res = div_missing(x_ls, y_ls, missing_values)
		(clean_x_ls, clean_y_ls, missing_x_ls, missing_y_ls) = div_res
		# x昇順に整序
		zip_ls = list(zip(clean_x_ls, clean_y_ls))
		zip_ls.sort(key = lambda e: e[0])
		# 数値横軸をグループに分割
		grouped_zip_ls = num_grouping(zip_ls, min_bin_ratio)
		# 各グループの横軸値を集約
		group_ls = [
			{
				"x": np.mean([x for x, y in group]),
				"y_ls": [y for x, y in group]
			}
			for group in grouped_zip_ls
		]
		# 欠損グループの追加
		if len(missing_y_ls) > 0:
			group_ls.append({"x": "missing", "y_ls": missing_y_ls})
	elif x_type == "nominal":	# 名義尺度
		# 欠損を"missing"に変換
		if "missing" in x_ls: raise Exception('[quantile-scatter error] The string "missing" is reserved as a special string to express missingness and cannot be used in the nominal scale.')
		x_ls = [("missing" if x in missing_values else x) for x in x_ls]
		# 各名義の出現頻度を調べる
		rank_ls = gen_rank_ls(x_ls)
		# ランキング上位のkeyを一覧
		top_keys = [k for k, cnt in rank_ls if cnt / len(x_ls) >= min_bin_ratio]
		top_keys_dic = {k: True for k in top_keys}
		# 値の一覧をグループにくくる
		group_dic = {}
		for x, y in zip(x_ls, y_ls):
			key = (x if x in top_keys_dic else "others")
			if key not in group_dic: group_dic[key] = []
			group_dic[key].append(y)
		# 成果物の形を整える
		keys = (top_keys + ["others"] if "others" in group_dic else top_keys)
		group_ls = [
			{"x": key, "y_ls": group_dic[key]}
			for key in keys	# top_keys の順序に従う
		]
	else:
		raise Exception("[error] invalid x_type.")
	return group_ls, x_type

# x軸のmissingをxy系列から除去
def del_missing_from_xy(org_x, org_y):
	show_x, show_y = [], []
	for x, y in zip(org_x, org_y):
		if x == "missing": continue
		show_x.append(x)
		show_y.append(y)
	return show_x, show_y

# matplotlibで可視化 [quantile_scatter]
def visualize(arg_data, x_type):
	from matplotlib import pyplot as plt
	for one_data in arg_data:
		show_x, show_y = one_data["x"], one_data["y"]
		if x_type == "number": show_x, show_y = del_missing_from_xy(one_data["x"], one_data["y"])	# x軸のmissingをxy系列から除去
		# 描画
		plt.plot(
			show_x, show_y,
			label = one_data["label"],
			marker = ".", markersize = 8
		)
	# 描画処理
	plt.legend()
	if show_x != one_data["x"]:	# x_typeがnumberでかつmissingが除去されている場合
		plt.title("missing value is not plotted")	# タイトルとして警告文を挿入
	if x_type == "nominal":
		plt.xticks(rotation=90)
		plt.tight_layout()
	plt.show()

# 1ラベル分のグラフデータ生成
def one_label_sum(
	group_ls,	# グループ化されたデータ
	sum_func,	# データ集計関数
	label	# 凡例に掲載するデータ説明
):
	# xの取り出し
	show_x_ls = [group["x"] for group in group_ls]
	# yの計算 (sum_funcでgroup内y値を集計)
	show_y_ls = [
		sum_func(group["y_ls"])
		for group in group_ls
	]
	# データ数のリストの作成
	data_n_ls = [len(group["y_ls"]) for group in group_ls]
	# データをパッケージングして返却
	return {
		"label": label,
		"x": show_x_ls,
		"y": show_y_ls,
		"data_n": data_n_ls,
	}

# 分位点散布図の描画 [quantile_scatter]
def plot(
	x,	# 横軸数値リスト
	y,	# 縦軸数値リスト
	min_bin_ratio = 1/20,	# 最小グループ割合 (最も小さいグループのレコード数が全体に占める割合)
	ile_ls = [0.25, 0.5, 0.75],	# どこの分位点を出すか
	mean = False,	# 平均も出力する
	show = True,	# False指定でグラフを出力しない (データ集計のみ)
	missing_values = [],	# 欠損としてあつかう値の指定
):
	# 横軸値に従ってグルーピング
	group_ls, x_type = x_grouping(x, y, min_bin_ratio, missing_values)
	# 返却するデータ
	ret_data = []
	# 各分位点を集計
	for ile in ile_ls:
		# 今回のデータ集計方法
		sum_func = lambda arg_y_ls: np.quantile(arg_y_ls, ile)
		# 1ラベル分のグラフデータ生成
		ret_data.append(one_label_sum(
			group_ls,	# グループ化されたデータ
			sum_func,	# データ集計関数
			label = str(ile)	# 凡例に掲載するデータ説明
		))
	# 平均を集計
	if mean is True:
		# 1ラベル分のグラフデータ生成
		ret_data.append(one_label_sum(
			group_ls,	# グループ化されたデータ
			sum_func = lambda arg_y_ls: np.mean(arg_y_ls),	# データ集計関数
			label = "mean"	# 凡例に掲載するデータ説明
		))
	# matplotlibで可視化 [quantile_scatter]
	if show is True:
		visualize(ret_data, x_type)
	return ret_data
