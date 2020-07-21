# IBM Watson Speech to Textによるストリーミング音声文字変換

## 動作環境

Windows 10 Home 64bit + Python 3.8.3で動作を確認しています。

## 動作に必要なもの

### PyAudio

上記の環境では`pip install pyaudio`でインストールできなかったので、[ここ](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)から適切なバージョンのPyAudioをインストールしてください。
詳しいインストール方法は[ここ](https://stackoverflow.com/a/55630212)を参照してください。

### Watson Developer Cloud Python SDK

`pip`でインストールできます。
```sh
pip install ibm-watson
```

## Speech to Textの資格情報

IBM CloudのSpeech to Textのページのから、管理→資格情報→ダウンロードをクリックし、ダウンロードした`ibm-credentials.env`を`main.py`と同じディレクトリに配置してください。

## 実行方法

```sh
python main.py
```
で実行できます。
`Ctrl+c`で終了できます。
