---
layout: default
title: メモページ
---

# 量が溜まってきたら整理すること　＞　未来の自分

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
- json.load()
### OpenCV
#### cap.set()が効かない
- カメラidが合っているか確認する。(0だと思っていたら仮想デバイスに押されて1になってることがある）
### Blender
#### socketでプロセス間通信をしようとすると止まる。
- スクリプト実行するまでblenderはほかの動作を止める。
- したがって別のスレッドを立てて実行する必要がある。

#### 毎回忘れるクロスシムの手順
1. 布を用意する。<br>
 a. 厚みのないメッシュ、Subdivision Surfaceで頂点を増やしておく。<br>
 b. `Physics`→`Cloth`をクリックしてクロスシムを有効化。<br>
2. 布と相互作用するオブジェクトを用意する。<br>
 a. `Physics`→`Collision`をクリックして衝突判定を有効化する。<br>
 
#### 毎回忘れるオブジェクト毎のレンダリングと合成
- Compositingのレンダーレイヤーはビュー単位でインプットを取り扱う
- ビューは右上から選択する。デフォルトでView Layer
1. View Layerを複製する。
   - 分けたい数だけ複製する。
   - 現在の状態から分けたいなら、Copy Settingを選択すると表示するレイヤーの状態がコピーされて楽。
2. 編集したいView Layerを選択した状態で、Outliner(オブジェクトの一覧)から表示したいオブジェクトだけにチェックを入れる。
   - 可視状態はView Layerごとに管理している。
3. レンダリング後、Compositing画面で、Render Layerノードを複製し、下部のView Layerを所望のレイヤーに変更する。
4. `Color`→`Z combine`ノードを追加し、分離したViewのImageとZ値を繋ぐと合成してくれる。
- 背景を削除する際、`Film`->`Transparent`で消すと全部のViewから消えて不便。個別に設定できない。
   - 一度背景ありでレンダリングしてしまってから、Z値でしきい値を取って削除する。
   - 特に何も考えなくても、`Z combine`に入れる時に最も優先度が低くなる(Z->\inf)ので勝手に消えてくれる。
   
#### 影だけレンダリングしたい場合の設定
##### Eeveeの場合
- マテリアルで設定する。Alpha設定を影に反映されないようにし、Alpha=0とすればよい。
1. `Material` -> `Settings` -> `Blend Mode`を`Alpha Clip`
2. `Material` -> `Settings` -> `Shadow Mode`を`Opaque`
3. `Material` -> `Surface` -> `Alpha`を`0`にする
##### Cyclesの場合
- オブジェクトの設定でレイトレ時に無視するようにする。
1. `Object Properties` -> `Visibility` -> `Ray Visibility` -> `Camera`のチェックを外す

#### BVHについて
##### 概要
- モーキャプのアニメーションとArmatureのセット

##### 使い方
- File -> Import -> .bvh　だけでOK
- ImportされたArmatureにアニメーションがついてるので、今持ってるモデルにそのまま使える訳じゃない。
##### トレースする場合に逆回転する
- オイラー角じゃなくてクォータニオンを使う
[参考 dskjal様](https://dskjal.com/blender/eular-vs-quaternion-on-blender.html)



### VScode
#### 実行時にfailed to launch (exit code: 1)となる
- 既にほかの用途でVScodeを使っている場合、WSLで実行していないか確認する。
- ローカルにインストールしているならsettings.jsonのshellは`"C:/WINDOWS/System32/wsl.exe"`ではなく`"C:/WINDOWS/System32/cmd.exe"`にする。
- 切り替え面倒だな...
