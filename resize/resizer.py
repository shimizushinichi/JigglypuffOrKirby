import os
from PIL import Image

def resizer(input_dir, width, height):
    # 例えばinput_dir = augmented/jigglypuffなら、input_folder_name = jigglypuff
    input_folder_name = os.path.basename(input_dir)
    # 出力先はresized/{input_folder_name}/{width}_{height}/とする。
    output_dir = os.path.join("resized", input_folder_name, "{}_{}".format(width, height))
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
