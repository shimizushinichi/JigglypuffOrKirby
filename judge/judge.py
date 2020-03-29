from tensorflow.keras import models
from tensorflow.keras.preprocessing import image
import numpy as np
import os

def judge(input_img, input_model):
    model = models.load_model(input_model)

    img = image.load_img(input_img, target_size=(224,224,3))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)

    features = model.predict_proba(img_data)

    #category_list.txtからカテゴリの一覧を取得する
    category_list = get_category_list()

    #featuresの中で最も確率が高い番号を取得して、その番号に当てはまるカテゴリを出力する
    max_prob = np.where(features[0]==max(features[0]))[0][0]
    predicted_category = category_list[max_prob]
    print("この画像は" + "{}です".format(predicted_category))

    #全てのカテゴリの確率をそれぞれ出力する
    for i in range(len(category_list)):
        print("{}である確率：".format(category_list[i]), features[0][i])


def get_category_list():
    """同ディレクトリのcategory_listを参照してカテゴリ名のリストを作成する
        jigglypuff
        kirby
        と書かれていれば、["jigglypuff", "kirby"]を返す。
    """
    category_list = []
    file_dir = os.path.join(os.path.dirname(__file__), "category_list.txt")
    with open(file_dir) as f:
        category_list_file = f.readlines()
    for category_name in category_list_file:
        category_list.append(category_name.strip())

    assert category_list, "category_list.txtの内容が空です。ファイルを確認してください。"

    return category_list
