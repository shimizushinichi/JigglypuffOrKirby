from .keras_yolo3.yolo import YOLO
from PIL import Image
import os, glob

def trimmer(input_dirs):
    for input_dir in input_dirs:
        if input_dir[-1] == "/":
            input_dir = input_dir[:-1]
        character = os.path.basename(input_dir)

        trimmed_savepath = "trimmer_checked/" + "trimmed/" + character
        untrimmed_savepath = "trimmer_checked/" + "untrimmed/" + character
        try:
            os.makedirs(trimmed_savepath)
            os.makedirs(untrimmed_savepath)
        except FileExistsError:
            pass

        model_path = get_modelpath(character)
        classes_path = get_classes_path(character)
        anchors_path = get_anchors_path()
        yolo = YOLO(model_path=model_path, classes_path=classes_path, anchors_path=anchors_path)

        filepaths = glob.glob(input_dir+"/*")

        for filepath in filepaths:
            basename, ext = os.path.splitext(filepath)
            if ext in {".png", ".jpg", ".jpeg"}:
                image = Image.open(filepath)
                detected_result_list = yolo.detect_image(image)
                filename = os.path.basename(filepath)

                if detected_result_list == []:
                    image.save(untrimmed_savepath+"/"+filename)
                else:
                    for idx, coordinate in enumerate(detected_result_list):
                        trimmed_image = image.crop((coordinate["left"], coordinate["top"], coordinate["right"], coordinate["bottom"]))
                        trimmed_image.save(trimmed_savepath+"/trimmed_"+str(idx)+"_"+filename)

def get_modelpath(character):
    model_name = "trained_weights_final_{}.h5".format(character)
    model_path = os.path.join(os.path.dirname(__file__), "keras_yolo3", "weights", model_name)

    assert os.path.isfile(model_path), "{}が見つかりませんでした。ファイル名が合っているかどうかご確認ください。".format(model_path)

    return model_path

def get_classes_path(character):
    classesfile_name = "my_classes_{}.txt".format(character)
    classesfile_path = os.path.join(os.path.dirname(__file__), "keras_yolo3", "model_data", classesfile_name)

    assert os.path.isfile(classesfile_path), "{}が見つかりませんでした。ファイル名が合っているかどうかご確認ください。".format(classesfile_path)

    return classesfile_path


def get_anchors_path():
    anchors_path = os.path.join(os.path.dirname(__file__), "keras_yolo3", "model_data", "yolo_anchors.txt")

    assert os.path.isfile(anchors_path), "{}が見つかりませんでした。ファイル名が合っているかどうかご確認ください。".format(anchors_path)

    return anchors_path
