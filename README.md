# voiceroid_translation

（要望があったら詳細情報は追加しますが、
　概ねは以下の通りです）

## 導入
### 出来ること
英単語や英文をマイクに呟くと、茜ちゃん達に和訳を読んでもらえるよ！

### 注意事項
1. 和訳レベルは、現状Google翻訳です
2. あくまで実装例として見て、各自で実装するのを強くお勧めします
（参考サイトを見ながらであれば、かなり簡単ですので）
3. GoogleAPIを使用するため、極めて少額ですが実行にはお金がかかる場合があります。

## 本題
### 動作確認環境
Windows10 コマンドプロンプト

### 導入必要環境
VOICEROID2のソフトのいずれか(有料)
Python3系(on windows)

### 準備方法
1. GoogleAPIKeyの取得
2. GoogleSpeechToTextの有効化
3. config.py.formatファイルのkeyに、そのkeyを代入
4. config.py.formatファイルを、config.pyファイルに名称変更

### 実行方法
1. VOICEROID2 の起動
2. main.pyのあるフォルダで、>python main.py

## 蛇足
### コードの動作イメージ
マイク音声(英語)
↓
テキスト(英語)
↓
テキスト(日本語)
↓
ボイロ音声(日本語)

### 作った動機
1. 私的にこういうソフトが欲しかったので
2. GDG DevFest2018 に行ったら、GoogleAPIを使いたくなったので
3. Pythonで何か作りたかったので



## 参考サイト
### 主にコードに影響する内容
#### マイク音声（英語）→テキスト（英語）の手法
- [PythonでCloud Speech APIを叩いて音声をテキスト化](https://to-kei.net/python/google-cloud-speech-api/)
- [Google Cloud Speech API を使った音声の文字起こし手順](https://qiita.com/knyrc/items/7aab521edfc9bfb06625#)
- [Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/?hl=ja)
- [Qiita Pythonで音を監視して一定以上の音量を録音する](https://qiita.com/mix_dvd/items/dc53926b83a9529876f7)

#### テキスト（英語）→テキスト（日本語）の手法
- [Python – googletransを試してみました。](https://dev.classmethod.jp/beginners/python-py-googletrans/)
- [TRANSLATION API](https://cloud.google.com/translate/)

#### テキスト（日本語）→ボイスロイド音声 の手法
- [VOICEROID2(紲星あかり)をプログラムから動かしてみる](https://qiita.com/Teara/items/936733c9e7e47b5ebe79)
- [Windows10でpywinautoを使おうとしたらハマった](https://qiita.com/ponkio-o/items/409766b574f03d1d5a49)


### トラブルシューティングなどで参考にした内容
#### 色々
- [pyaudioのインストールで詰んだ時の対処法](https://qiita.com/musaprg/items/34c4c1e0e9eb8e8cc5a1)
- [google-api-python-clientとPython3でちょっと遊んでみる。](https://pandanote.info/?p=791)
- [Pythonで改行を含む文字列の出力、連結、分割、削除、置換](https://note.nkmk.me/python-string-line-break/)
- [Google Cloud Transition API - クイックスタート](https://cloud.google.com/kubernetes-engine/docs/quickstart?hl=ja)
- [Python2と3の互換性ライブラリ「Six」](https://kiwamiden.com/python-2-and-3-compatibility-library-six)
