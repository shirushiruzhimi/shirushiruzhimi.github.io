---
layout: default
title: メモページ
---
# Python関係の忘備録
## 環境系
### Python
#### Pythonが動かない(MicrosoftStoreが開く)
- Windowsアップデートでパスの優先度が取られてしまっているので、『環境変数の編集』→『ユーザー環境変数』→『Path』を編集し、『...WindowsApp』を一番下に移動する。
### OpenCVが動かない
#### cv2.cv2 not found
- opencv-python をインストールする。`pip install opencv-python`
 - 既にインストールされている場合は、一度`pip uninstall opencv-python`してからもう一度実行する。
### TensorFlowが動かない
#### Session()がない
- TF2.0からはSessionが無くなったらしい。バージョンを1.xに落とせば動く。
### Anaconda
#### envが切り替えられない
- powershellを使っているとダメらしい。エラーすら出ないので気づき難いのが憎らしい。
- command promptあたりでやればよい。
 - 実際にやって出来た。
### JSON
#### 文字列を辞書にパースしたい
- json.loadd()
### OpenCV
#### cap.set()が効かない
- カメラidが合っているか確認する。(0だと思っていたら仮想デバイスに押されて1になってることがある）
### Blender
#### socketでプロセス間通信をしようとすると止まる。
- スクリプト実行するまでblenderはほかの動作を止める。
- したがって別のスレッドを立てて実行する必要がある。

### VScode
#### 実行時にfailed to launch (exit code: 1)となる
- 既にほかの用途でVScodeを使っている場合、WSLで実行していないか確認する。
- ローカルにインストールしているならsettings.jsonのshellは`"C:/WINDOWS/System32/wsl.exe"`ではなく`"C:/WINDOWS/System32/cmd.exe"`にする。
- 切り替え面倒だな...
