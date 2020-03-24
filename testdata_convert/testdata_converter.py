import os
import numpy as np
from PIL import Image
import pickle
import datetime

def categorizer(input_dirs):
    """input_dirs内の画像ファイルを(カテゴリ名, ファイルパス)の配列にします。

        Output:以下のようなカテゴリ数次元配列となる。
        [[(カテゴリ1,ファイルパス1),(カテゴリ1,ファイルパス2),(カテゴリ1,ファイルパス3)],
        [(カテゴリ2,ファイルパス1),(カテゴリ2,ファイルパス2),(カテゴリ2,ファイルパス3)]]
    """
    categorized_file_list = []

    for input_dir in input_dirs:
        # カテゴリ名はフォルダ名から抽出する。もし末尾が/で終わる形で入力されたら取り除く。
        if input_dir[-1] == "/":
            input_dir = input_dir[:-1]
        category_name = os.path.basename(input_dir)
        #カテゴリ名を数字に変換する。
        category_num = convert_category_to_num(category_name)
        # input_dir内の画像ファイル一覧を取得
        file_list = os.listdir(input_dir)
        # 拡張子を確認した上で、(カテゴリ名、ファイルパス)を配列に格納する。
        for img_dir in file_list:
            _, ext = os.path.splitext(img_dir)
            if ext in {".png", ".jpg", ".jpeg"}:
                img_dir_path = input_dir + "/" + img_dir
                categorized_file_list.append((category_num, img_dir_path))

    return categorized_file_list

def convert_category_to_num(input_category):
    """同ディレクトリのcategory_listを参照してカテゴリ名を数字に変換する。
        jigglypuff
        kirby
        と書かれていれば、jigglypuff->0, kirby->1
    """
    file_dir = os.path.join(os.path.dirname(__file__), "category_list.txt")
    with open(file_dir) as f:
        category_list = f.readlines()
    for idx, category_name in enumerate(category_list):
        if input_category == category_name.strip():
            return idx
    raise Exception("カテゴリ名({})が見つかりません。{}を確認してください。".format(input_category, file_dir))

def convert_to_numpy(input_list):
    """[(カテゴリ, ファイルパス),...]という配列を受け取り、
    ファイルパスをnumpy化して配列X, カテゴリをそのまま配列Yに格納してX,Yを返します。
    """
    X = []
    Y = []
    for category, file_name in input_list:
        img = Image.open(file_name)
        img = img.convert("RGB")
        img_data = np.asarray(img)
        X.append(img_data)
        Y.append(category)

    return np.array(X), np.array(Y)

def create_numpied_data(X_test, Y_test):
    xy = (X_test, Y_test)
    size = X_test[0].shape
    #画像サイズが256,256の場合は、testdata_numpied/256_256にファイルを出力する。
    output_dir = os.path.join("testdata_numpied", "{}_{}".format(size[0], size[1]))
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    now = datetime.datetime.now()
    numpied_file_name =\
     "testdata_{}_{}".format(size[0],size[1]) + "_{0:%Y%m%d%H%M}".format(now) +".npy"

    pickle_dump(xy, output_dir + "/" + numpied_file_name)

def testdata_converter(input_dirs):
    categorized_file_list = categorizer(input_dirs)
    X_test, Y_test = convert_to_numpy(categorized_file_list)
    create_numpied_data(X_test, Y_test)

# Macで4GB以上のファイルの読み書きを行うとエラーになるためこちらを使用する
# https://qiita.com/NomuraS/items/da3fd3a1ecd76175e5f8
class MacOSFile(object):

    def __init__(self, f):
        self.f = f

    def __getattr__(self, item):
        return getattr(self.f, item)

    def read(self, n):
        # print("reading total_bytes=%s" % n, flush=True)
        if n >= (1 << 31):
            buffer = bytearray(n)
            idx = 0
            while idx < n:
                batch_size = min(n - idx, 1 << 31 - 1)
                # print("reading bytes [%s,%s)..." % (idx, idx + batch_size), end="", flush=True)
                buffer[idx:idx + batch_size] = self.f.read(batch_size)
                # print("done.", flush=True)
                idx += batch_size
            return buffer
        return self.f.read(n)

    def write(self, buffer):
        n = len(buffer)
        print("writing total_bytes=%s..." % n, flush=True)
        idx = 0
        while idx < n:
            batch_size = min(n - idx, 1 << 31 - 1)
            print("writing bytes [%s, %s)... " % (idx, idx + batch_size), end="", flush=True)
            self.f.write(buffer[idx:idx + batch_size])
            print("done.", flush=True)
            idx += batch_size


def pickle_dump(obj, file_path):
    with open(file_path, "wb") as f:
        return pickle.dump(obj, MacOSFile(f), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(MacOSFile(f))
