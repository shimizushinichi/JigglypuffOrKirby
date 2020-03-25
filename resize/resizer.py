import os
from PIL import Image

def resizer(input_dirs, width, height):
    for input_dir in input_dirs:
        # カテゴリ名はフォルダ名から抽出する。もし末尾が/で終わる形で入力されたら取り除く。
        if input_dir[-1] == "/":
            input_dir = input_dir[:-1]
        # 例えばinput_dir = augmented/jigglypuffなら、input_folder_name = jigglypuff
        input_folder_name = os.path.basename(input_dir)
        # 出力先はresized/{width}_{height}/{input_folder_name}/とする。
        output_dir = os.path.join("resized", "{}_{}".format(width, height), input_folder_name)
        size = (width, height)
        try:
            os.makedirs(output_dir)
        except FileExistsError:
            pass

        file_list = os.listdir(input_dir)
        for file_name in file_list:
            basename, ext = os.path.splitext(file_name)
            if ext in {".png", ".jpg", ".jpeg"}:
                img = Image.open(input_dir + "/" + file_name)
                #画像を指定されたサイズに変更する。
                img = img.resize(size, Image.LANCZOS)
                img.save(output_dir + "/" + basename + "_{}_{}".format(width, height) + ext)
