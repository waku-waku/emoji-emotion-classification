#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import emoji
import fasttext as ft
import MeCab


class predict:

	def __init__(self):
		# モデル読み込み
		self.classifier = ft.load_model('prod_models/model.bin')

	def get_surfaces(self, content):
		"""
		文書を分かち書き
		"""
		tagger = MeCab.Tagger('')
		tagger.parse('')
		surfaces = []
		node = tagger.parseToNode(content)

		while node:
			surfaces.append(node.surface)
			node = node.next

		return surfaces


	def separate_part(self, row, emojiList):
		"""
		文書を分かち書きし単語単位に分割
		"""
		# content = format_text(row)
		tagger = MeCab.Tagger(' -d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd')
		tagger.parse('')
		# text = content.encode(PARSE_TEXT_ENCODING)
		# node = tagger.parseToNode(text)

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


		node = tagger.parseToNode(row)

		while node:
			pos = node.feature.split(",")[0]
			pos2 = node.feature.split(",")[1]
			# print(node.feature)
			# word = node.surface
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

		parsed_words_dict = {
	    	"all": words[1:-1], # 最初と最後には空文字列が入るので除去
	    	"nouns": nouns,
	    	"nouns_sahens": nouns_sahens,
	    	"adjective_verb": adjective_verb,
	    	"verbs": verbs,
	    	"adjs": adjs,
	    	"auxiliary_verbs": auxiliary_verbs,
	    	"sinbols": sinbols
		}
		# return parsed_words_dict
		print(results)
		return results


	def tweet_class(self, content):
		"""
		ツイートを解析して分類を行う
		"""
		emojiList = []

		f = open('emotion_emoji_list.csv') # 自作の感情データ
		datas = f.readlines()
		f.close()

		for data in datas:
			emojis = data.strip().split("\t")
			for emotion in emojis[1].split(","):
				emojiList.append(emoji.emojize(emotion, use_aliases=True))

		words = " ".join(self.separate_part(content, emojiList))
		estimate = self.classifier.predict_proba([words], k=6)[0][0]

		if estimate[0] == "__label__1,":
			print('喜び', estimate[1])
		elif estimate[0] == "__label__2,":
			print('悲しみ', estimate[1])
		elif estimate[0] == "__label__3,":
			print('怒り', estimate[1])
		elif estimate[0] == "__label__4,":
			print('驚き', estimate[1])
		elif estimate[0] == "__label__5,":
			print('嫌悪', estimate[1])
		elif estimate[0] == "__label__6,":
			print('恐れ', estimate[1])


if __name__ == '__main__':
	pre = predict()
	pre.tweet_class("".join(sys.argv[1:]))
