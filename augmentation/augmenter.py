import os
from PIL import Image

def augmenter(input_dir, output_dir, character):
    output_dir = os.path.join(output_dir, character)
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    file_list = os.listdir(input_dir)
    for file_name in file_list:
        basename, ext = os.path.splitext(file_name)
        if ext == ".png" or ".jpg" or ".jpeg":
            img = Image.open(input_dir + "/" + file_name)

            # 90度ずつ回転させて画像を保存する。
            tmp_img = img
            tmp_img.save(output_dir + "/" + basename + "_0" + ext)
            for i in range(3):
                tmp_img = tmp_img.transpose(Image.ROTATE_90)
                rotate_num = "_" + str((i+1) * 90)
                tmp_img.save(output_dir + "/" + basename + rotate_num + ext)

            #画像の大きさを取得する
            width, height = img.size
            #画像を半分に縮小する
            img.thumbnail((width//2, height//2), Image.LANCZOS)
            #縮小した余白を埋めるための背景画像を作成。
            bg = Image.new("RGB", [width, height], (0,0,0,0))
            #縮小した画像を背景画像のセンターに配置
            bg.paste(img, (width//4, height//4))

            # 90度ずつ回転させて縮小した画像を保存する。
            shrinked_img = bg
            shrinked_img.save(output_dir + "/" + basename + "_shrinked" + "_0" + ext)
            for i in range(3):
                shrinked_img = shrinked_img.transpose(Image.ROTATE_90)
                rotate_num = "_" + str((i+1) * 90)
                shrinked_img.save(output_dir + "/" + basename + "_shrinked" + rotate_num + ext)
