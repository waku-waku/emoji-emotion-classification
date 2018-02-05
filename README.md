## 絵文字付きツイート感情分析

```

1. python get_data.py 1 30 (1~6まで繰り返す)
2. python uniq.py {FILE_NAME} (同じツイートを削除し, 精度を高める)
3. cd test_data
4. cat __label__1.txt __label__2.txt __label__3.txt __label__4.txt
__label__5.txt __label__6.txt > model.txt
5. cd ..
6. python learning.py test_data/model.txt prod_models/model(fastTextにより学習)
7. python prediction.py "SENTENCE"


*パラメータ調整して学習する用*

`fasttext supervised -input train_data/model.txt -output prod_models/model -dim 10 -lr 0.1 -wordNgrams 2 -minCount 1 -bucket 10000000 -epoch 100 -thread 4`

`fasttext test prod_models/model.bin test_data/test.txt`


```

## 基本設定
1. Twitter Apps(apps.twitter.com)より, アプリケーションを作成し, Keys and  Access Tokensを取得する。
2. get_data.pyのCK,CS,AT,ASに1の取得したものを入力

## ライブラリ
使用したライブラリをインストールしてください

### 基本ライブラリ
- numpy
- scipy
- sys
- time
- json
- re

### ベクトル化及び学習
- fastText(https://github.com/facebookresearch/fastText)

### 日本語形態素解析
- mecab-python3(https://pypi.python.org/pypi/mecab-python3)

### Twitter API
- requests_oauthlib(https://github.com/requests/requests-oauthlib)

### 絵文字
- emoji(https://pypi.python.org/pypi/emoji/)


