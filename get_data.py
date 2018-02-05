#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
各種ライブラリをインポート
'''
import numpy as np
import scipy as sp
import sys
import re
import json
import emoji
import MeCab
from time import sleep
from requests_oauthlib import OAuth1Session


'''
パースエンコーディングの文字コードを指定
'''
PARSE_TEXT_ENCODING = 'utf-8'


'''
Twitter AppsのConsumer KeyとAccess Token
'''
# CK = ""
# CS = ""
# AT = ""
# AS = ""


'''
直近１週間以内につぶやかれた日本語ツイートでRTを除いたものを取得
'''
API_URL = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended&exclude=retweets&lang=ja"
CLASS_LABEL = "__label__"


'''
メイン
'''
def main(count):
	keyword, emojiList = select_emoji()

	print("( " + str(keyword) + " ) を含むツイートを" + CLASS_LABEL + str(input_emotion) + ".txtに書き込み")

	for i in range(0, count, 1):
		tweets = get_tweet(keyword)
		surfaces = get_surfaces(tweets, emojiList)
		write_txt(surfaces, i)
		sleep(1)


'''
感情に対応する絵文字を取得
'''
def select_emoji():
	emojiList = []
	keywords = []

	f = open('emotion_emoji_list_5.csv')
	datas = f.readlines()
	f.close()

	for data in datas:
		emojis = data.strip().split("\t")
		for emotion in emojis[1].split(","):
			emojiList.append(emoji.emojize(emotion, use_aliases=True))
			if emojis[0] == input_emotion:
				keywords.append(emoji.emojize(emotion, use_aliases=True))
	return ' OR '.join(keywords), emojiList


'''
ツイート取得
'''
def get_tweet(keyword):

	# Twitterからkeywordに関連するツイートを取得
	params = {'q' : keyword, 'count' : 100}
	twitter = OAuth1Session(CK, CS, AT, AS)
	req = twitter.get(API_URL, params = params)
	results = []
	if req.status_code == 200:
		# JSONをパース
		tweets = json.loads(req.text)
		for tweet in tweets['statuses']:
			results.append(tweet['full_text'])
		return results
	else:
		print ("Error: %d" % req.status_code)


'''
品詞分解
'''
def separate_part(row, emojiList):

	# 各変数初期化
	results = []
	surf = []
	words = []
	nouns = []
	nouns_sahens = []
	adjective_verb = []
	verbs = []
	adjs = []
	auxiliary_verbs = []
	sinbols = []

	# ipadic-neologdとMecabを用いて品詞分解
	content = format_text(row)
	tagger = MeCab.Tagger(' -d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd')
	tagger.parse('')
	node = tagger.parseToNode(content)

	# 感情に関係する「動詞, 形容詞, 助動詞, 名詞サ変接続,
	# 名詞形容動詞語幹, 記号」のみをresultsに格納
	while node:
		pos = node.feature.split(",")[0]
		pos2 = node.feature.split(",")[1]
		word = node.feature.split(",")[6]
		if pos == "名詞":
			if pos2 == "サ変接続":
				nouns_sahens.append(word)
				results.append(word)
			elif pos2 == "形容動詞語幹":
				adjective_verb.append(word)
				results.append(word)
			nouns.append(word)
		elif pos == "動詞":
			verbs.append(word)
			results.append(word)
		elif pos == "形容詞":
			adjs.append(word)
			results.append(word)
		elif pos == "助動詞":
			auxiliary_verbs.append(word)
		elif pos == "記号":
			sinbols.append(word)
			if node.surface in emojiList:
				results.append(word)
		words.append(word)
		node = node.next

	# ツイートを品詞別にparsed_words_dictに格納
	parsed_words_dict = {
    	"all": words[1:-1],
    	"nouns": nouns,
    	"nouns_sahens": nouns_sahens,
    	"adjective_verb": adjective_verb,
    	"verbs": verbs,
    	"adjs": adjs,
    	"auxiliary_verbs": auxiliary_verbs,
    	"sinbols": sinbols
	}

	return results


'''
単語取得
'''
def get_surfaces(contents, emojiList):

	# 文書を分かち書きし単語単位に分割
	results = []
	for row in contents:
		results.append(separate_part(row, emojiList))
	return results

def write_txt(contents, i):

	# 評価モデル用のテキストファイルを作成する
	try:
		if(len(contents) > 0):
			fileName = "train_data/" + CLASS_LABEL + input_emotion + ".txt"
			labelText = CLASS_LABEL + input_emotion + ", "

			f = open(fileName, 'a')
			for row in contents:
				# 空行区切りの文字列に変換
				spaceTokens = " ".join(row);
				result = labelText + spaceTokens + "\n"
				# 書き込み
				f.write(result)
			f.close()
		print(str(i+1)+"回目: "+str(len(contents))+"行を書き込み")

	except Exception as e:
		print(str(i+1)+"回目: "+"テキストへの書き込みに失敗")
		print(e)


'''
文字整形
'''
def format_text(text):

	# ツイートから不要な情報を削除
	text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
	text=re.sub(r'@[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
	text=re.sub(r'&[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
	text=re.sub(';', "", text)
	text=re.sub('RT', "", text)
	text=re.sub('Rt', "", text)
	text=re.sub('ReTweet', "", text)
	text=re.sub('フォロー', "", text)
	text=re.sub('\n', " ", text)
	return text


'''
メイン
'''
if __name__ == '__main__':

	# 感情番号と繰り返し回数を入力
	argvs = sys.argv
	input_emotion = argvs[1]
	count = argvs[2]
	main(int(count))
