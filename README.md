# BookRollDL
BookRollで配布されているスライドをPDFとして保存できます．

## インストール方法
事前にPythonをインストールしておく必要があります．

リポジトリをクローンしてください．
```
git clone https://github.com/HaruhiroObora/BookRollDL
cd BookRollDL
```
または，このページの右上にあるCodeのボタンからzipを保存して展開してください．

仮想環境を作成してください．

Windowsの場合は
```
python -m venv .venv
.venv\Scripts\activate
```
Mac OS，Linuxの場合は
```
python3 -m venv .venv
source .venv/bin/activate
```
です．

必要なライブラリをインストールします．
```
pip install selenium beautifulsoup4 pymupdf pillow
```
Mac OSの場合はこれに加えて
```
brew install python-tk
```
も必要です．

## 実行方法
仮想環境を有効にしておきます．
Windowsの場合は
```
.venv\Scripts\activate
```
Mac OS，Linuxの場合は
```
source .venv/bin/activate
```
起動します．
```
python main.py
```
ブラウザとともに小さなウィンドウが表示されます．利用するLMSのボタンをクリックすると遷移します．ブラウザ上でログインを行ってください．

LMSでサイトを選択して，BookRollにアクセスします．保存したいスライドの1ページ目が表示された状態にしてください．

取り込み開始ボタンをクリックします．取り込み中は画面を操作しないようにしてください．自動的に全ページが保存され，しばらくするとファイルの保存画面が表示されます．名前をつけて保存してください．

ブラウザ上で再び別のスライドを表示して，取り込みを続けることができます．

## ライセンス
このプロジェクトは[MIT License](LICENSE)で公開されています．

NotoSansJPのフォントファイルを同梱しています．NotoSansJPは

著作権：Copyright 2014-2021 Adobe (http://www.adobe.com/)

ライセンス：[SIL Open Font License, Version 1.1](font/OFL.txt)

の下で配布されています．
