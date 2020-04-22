JigglypuffOrKirby
====

プリンとカービィを見分けるAIを作成するために画像収集、各種加工を容易に行えるように作成したプログラムです。  
こちらで作成したデータをGoogle Colab上で学習させることでモデルを作成します。  
作成したモデルをこのプログラムに渡して使用することで画像の判定を行うこともできます。  

This program is made for making AI which distinguishes Jigglypuff and Kirby.  
It enable us to collect images and several preprocessing.  
After preparing training data, a model is created on Google Colab.  
This program can judge image by using created model.  

## Test Environment
- Python 3.6.5
- Mac OS X 10.14.6
- Flickr API 2.4.0
- Keras 2.2.4
- NumPy 1.16.3
- Pillow 6.0.0
- TensorFlow 1.15

## Function

#### ・Crawler
```
sample:
$ python3 JigglypuffOrKirby.py crawler -ch jigglypuff
```
APIを使用してFlickrの画像を収集します。  
実行場所にdownloadsというフォルダを作成して、収集した画像を保存します。  
https://www.flickr.com/services/api/ から登録をしてAPIキー(key, secret)を取得してください。  
flickrAPIkey.jsonというファイルを作成してJigglypuffOrKirby.pyと同じディレクトリに設置。  
ファイルの内容は以下のように記述してください。

It collects images from Flickr by API.  
This function makes "downloads" folder on current directory, and saves images on this folder.  
First, sign up your account on  
https://www.flickr.com/services/api/, then get API keys ( "key" and "secret" ).  
Next, create a file named flickrAPIkey.json and place it in same folder as JigglypuffOrKirby.py.  
That file content should be described as follows.  
```
{
    "key":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "secret":"xxxxxxxxxxxxxxxx"
}
```

#### ・trimming
```
sample:
$ python3 JigglypuffOrKirby.py trimming -in "downloads/flickr/jigglypuff/ downloads/flickr/kirby/"
```
<a href="https://github.com/qqwweee/keras-yolo3">keras-yolo3</a>の機能の一部を使用して収集した画像の中からプリン、カービィを検出してトリミングします。  
実行場所にtrimmer_checkedというフォルダを作成します。  
対象を検出できた画像はトリミングしてからtrimmed/{character}に、  
検出できなかった画像は未加工のままuntrimmed/{character}に振り分けられます。  
trimmed内に20%ほど、untrimmed内に数枚ほど検出漏れが発生するので、実行後人間の目で確認を行ってください。  
実行前にこちらで用意したモデルをダウンロードして以下のディレクトリに設置してください。  
注意:画像があるフォルダ名からプリンかカービィかを判断するため、フォルダ名はjigglypuffかkirbyである必要があります。

It uses a part of <a href="https://github.com/qqwweee/keras-yolo3">keras-yolo3</a> for finding and trimming jigglypuff or kirby.  
It makes "trimmer_checked" folder.  
When it can find object, an image will be trimmed and saved on trimmed/{character}.  
When it cannot find object, an image will be saved on untrimmed/{character} as it is.  
Overlooking happens about 20% on trimmed, several images on untrimmed,  
 so you should check these folders by yourself after execution of this function.  
Before execute this function, download models from following URLs and place these on directory below.  
Note: because this function decides which of jigglypuff and kirby to look for from input folder name,  
input folder name should be "jigglypuff" or "kirby".  
```
trimming/keras_yolo3/weights/
```
<a href="https://drive.google.com/open?id=1GxbvFY4_3LdtgX8lfSjL9L8z_4VH-oT9">trained_weights_final_kirby.h5 (235MB)</a>  
<a href="https://drive.google.com/open?id=1ItKajs-9IEpqBIQ3GSbPJxMUjI6-MY6D">trained_weights_final_jigglypuff.h5 (235MB)</a>  

#### ・resize
```
sample:
$ python3 JigglypuffOrKirby.py resize -in "trimmer_checked/trimmed/jigglypuff/ trimmer_checked/trimmed/kirby/" -wid 224 -hei 224
```

<a href="https://github.com/python-pillow/Pillow">Pillow</a>を使用して指定されたフォルダ内の全ての画像を指定されたサイズ(-wid:幅、-hei:高さ)に縮尺を無視して変更します。  
加工された画像はresized/{wid}_{hei}/{画像のあったフォルダ名}に保存されます。  

It uses <a href="https://github.com/python-pillow/Pillow">Pillow</a> for resizing images with assinged size(-wid: width, -hei:height).  
Resized images are saved on resized/{wid}_{hei}/{inputed folder name}.  

#### ・augmentation
```
sample:
$ python3 JigglypuffOrKirby.py augmentation -in "resized/224_224/jigglypuff/ resized/224_224/kirby/"
```

指定されたフォルダ内の画像を90度ずつ回転させたもの、  
縮小させて90度ずつ回転させたものを作成します。(1枚の画像から7枚水増しされる。)  
加工した画像はaugmented/{画像のあったフォルダ名}に保存されます。  
この機能は使わない方が学習の精度が高かったため、使わないことをお勧めします。  
水増しを行いたい場合は、KerasのImageDataGeneratorを使用した方が良いかもしれません。  

This function processes images on the inputed folder by rotating 90 degrees three times,   
then shrink it and rotate 90 degrees three times.(in the end, it creates seven images from one image.)  
Processed images are saved on augmented/{inputed folder name}  
When I executed learning, I got better result only when I didn't use this function, so I recommend not to use this function.  
If you want to augment images, you may have to use ImageDataGenerator of Keras.  

#### ・numpy_convert
```
sample:
python3 JigglypuffOrKirby.py numpy_convert -in "resized/224_224/jigglypuff/ resized/224_224/kirby/"
```

学習に使うためのnumpyファイルを作成するための機能です。  
指定された各フォルダの画像を(カテゴリ番号, ファイルパス)の形に変換してひとまとめにして、  
学習用データ:テスト用データ=8:2にシャッフルしてからnumpyファイルとして出力します。  
numpyファイルはnumpied/{wid}_{hei}/yyyymmddHHMM.npyとして保存されます。  

This function is used for making numpy file for learning.  
It converts to (category_number, file_path), and puts input images together.  
Then shuffles them into train:test=8:2, and outputs numpy file.  
That numpy file is saved as numpied/{wid}_{hei}/yyyymmddHHMM.npy.  

#### ・testdata_convert
```
sample:
python3 JigglypuffOrKirby.py testdata_convert -in "resized/224_224/jigglypuff/ resized/224_224/kirby/"
```

モデルの評価に使うためのnumpyファイルを作成するための機能です。  
指定された各フォルダの画像を(カテゴリ番号, ファイルパス)の形に変換してひとまとめにして、  
numpyファイルとして出力します。  
numpyファイルはtestdata_numpied/{wid}_{hei}/yyyymmddHHMM.npyとして保存されます。  

This function is used for making numpy file for evaluating models.  
It converts to (category_number, file_path), and puts input images together.  
Then outputs numpy file.  
That numpy file is saved as testdata_numpied/{wid}_{hei}/yyyymmddHHMM.npy.  

#### ・judge
```
sample:
python3 JigglypuffOrKirby.py judge -img /Users/shimizushinichi/Desktop/Jigglypuff.png
```

学習したモデルを使用して一枚の画像がプリンかカービィか判定する機能です。  
こちらで作成した正解率97.9%のモデルを以下のURLからダウンロードして、judge/に配置してください。  
他のモデルを使用したい場合は-modelにモデルのパスを指定して実行してください。  

This function judges between jigglypuff or kirby from one image file by learned model.  
Download model with 97.9% accuracy rate and place it on judge/.  
If you want to use other model, set the model path on -model argument.  

<a href="https://drive.google.com/open?id=1DSglhf5afP6DCWr91645SfbzfK44BOf4">model_jigglypufforkirby_forJudge.h5 (132MB)</a>  

#### ・learn (use Google Colab)

無料でGPUを使用することができるGoogle Colab上で学習を行います。  
まだ利用したことがない場合は<a href="https://colab.research.google.com/">Google Colaboratory</a>にアクセスして新規ノートブックを作成してください。  
GoogleドライブにColab Notebooksというフォルダが作られるので、  
ここに作成した各種numpyファイルとlearnフォルダ内のnotebook３つをアップロードしてください。  

以下の手順で学習を進めます。  

- JigglypuffOrKirby_learn_VGG16_transferlearning.ipynb で転移学習を行う。  
  ※input_numpyの値を変更する。  
  -> Colab Notebooks/model/transfer_learning/に10epoch毎のモデルが作成されます。  

- JigglypuffOrKirby_スコアチェック.ipynb で転移学習を行ったモデル20個の評価を行う。  
  ※eval_numpyの値を変更する。  
  -> 最も正解率が高かったモデルを確認します。  

- JigglypuffOrKirby_learn_VGG16_finetuning.ipynb で最も正解率が高いモデルのファインチューニングを行う。  
  ※input_numpyの値を変更する。  
  -> /Colab Notebooks/model/finetuning/に10epoch毎のモデルが作成されます。  

- JigglypuffOrKirby_スコアチェック.ipynb でファインチューニングを行ったモデル10個の評価を行う。  
  -> 最も正解率が高いモデルを確認します。これで学習は完了です。  

    注意:GPU使用制限がかかるため、Google Colab上で作業が終わったらこまめにタブを閉じた方が良いです。  
    作業を終えたタブを一日中開きっぱなしにしていたところ、約24hほどGPUの使用制限になりました。  

Use Google Colab for learning, because you can use GPU for free.  
If you haven't used Google Colab, access <a href="https://colab.research.google.com/">Google Colaboratory</a> and make a new notebook.  
Then, Colab Notebooks folder is created on your Google Drive.  
Upload numpy files and three notebooks on learn folder to Colab Notebooks folder.  

To proceed learing, follow the steps below.  


- By JigglypuffOrKirby_learn_VGG16_transferlearning.ipynb, execute transfer learning.  
  ※change the value of input_numpy  
  -> every 10 epochs, model is saved on Colab Notebooks/model/transfer_learning/  

- By JigglypuffOrKirby_スコアチェック.ipynb, evaluate 20 models executed transfer learning.  
  ※change the value of eval_numpy  
  -> Check the highest accuracy model.  

- By JigglypuffOrKirby_learn_VGG16_finetuning.ipynb, fine-tune the highest accuracy model.  
  ※change the value of input_numpy  
  -> every 10 epochs, model is saved on /Colab Notebooks/model/finetuning/  

- By JigglypuffOrKirby_スコアチェック.ipynb, evaluate 10 models which are finetuned.  
  -> Save the highest accuracy model. That's it.  

    Note:Considering GPU usage limits, you have to close tabs when you finish working on Google Colab.  
    When I left it for a whole day after I finished working, I got restricted using GPU for almost 24h.  
