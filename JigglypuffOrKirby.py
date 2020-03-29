import argparse
import time
import os
import importlib

def user_input():
    list_type = lambda x:list(x.split(" "))

    parser = argparse.ArgumentParser(description="JigglypuffOrKirbyの各種機能を実行するためのプログラムです。")

    parser.add_argument("func", help="crawler, trimming, resize, augmentation, numpy_convert, testdata_convert or judge", type=str,
        choices=["crawler", "trimming", "augmentation", "resize", "numpy_convert", "testdata_convert", "judge"])
    parser.add_argument("-s", "--site", help="website to crawl", type=str, default = "flickr", choices=["flickr"])
    parser.add_argument("-ch", "--character", help="Search word", type=str)
    parser.add_argument("-wid", "--width",help="width for output image", type=int)
    parser.add_argument("-hei", "--height",help="height for output image", type=int)
    parser.add_argument("-in", "--inputdirs", help="Image folders. should be space separated. e.g '/aaa/bbb ccc/ddd'", type=list_type)
    parser.add_argument("-img", "--imagepath", help="An image path to be used by judge func.", type=str)
    parser.add_argument("-model", "--model", help="A model path to be used by judge func", type=str, default = "judge/model_jigglypufforkirby_forJudge.h5")

    args_namespace = parser.parse_args()
    arguments = vars(args_namespace)
    return arguments

def run_crawler(site, character):
    import_file = "crawler.{}.crawler".format(site)
    crawler_module = importlib.import_module(import_file)
    crawler = crawler_module.ImageCrawler()
    crawler.get_images(character)

def run_trimmer(input_dirs):
    for input_dir in input_dirs:
        assert os.path.isdir(input_dir), "-indirsに指定されたディレクトリが見つかりません。input:{}".format(input_dir)
    import_file = "trimming.trimmer"
    trimmer_module = importlib.import_module(import_file)
    trimmer_module.trimmer(input_dirs)

def run_resizer(input_dirs, width, height):
    for input_dir in input_dirs:
        assert os.path.isdir(input_dir), "-indirsに指定されたディレクトリが見つかりません。input:{}".format(input_dir)
    assert width, "-widが空白か無効な値になっています。input:{}".format(width)
    assert height, "-heiが空白か無効な値になっています。input:{}".format(height)
    import_file = "resize.resizer"
    resizer_module = importlib.import_module(import_file)
    resizer_module.resizer(input_dirs, width, height)

def run_augmenter(input_dirs):
    for input_dir in input_dirs:
        assert os.path.isdir(input_dir), "-indirsに指定されたディレクトリが見つかりません。input:{}".format(input_dir)
    import_file = "augmentation.augmenter"
    augmenter_module = importlib.import_module(import_file)
    augmenter_module.augmenter(input_dirs)

def run_numpy_converter(input_dirs):
    for input_dir in input_dirs:
        assert os.path.isdir(input_dir), "-indirsに指定されたディレクトリが見つかりません。input:{}".format(input_dir)
    import_file = "numpy_convert.numpy_converter"
    numpy_converter_module = importlib.import_module(import_file)
    numpy_converter_module.numpy_converter(input_dirs)

def run_testdata_converter(input_dirs):
    for input_dir in input_dirs:
        assert os.path.isdir(input_dir), "-indirsに指定されたディレクトリが見つかりません。input:{}".format(input_dir)
    import_file = "testdata_convert.testdata_converter"
    testdata_converter_module = importlib.import_module(import_file)
    testdata_converter_module.testdata_converter(input_dirs)

def run_judge(image_path, model_path):
    assert os.path.isfile(image_path), "-imgに指定されたファイルが見つかりません。input:{}".format(image_path)
    assert os.path.isfile(model_path), "-modelに指定されたファイルが見つかりません。input:{}".format(model_path)
    import_file = "judge.judge"
    judge_module = importlib.import_module(import_file)
    judge_module.judge(image_path, model_path)

def main():
    arguments = user_input()
    t0 = time.time() # start the timer
    if arguments["func"] == "crawler":
        run_crawler(arguments["site"], arguments["character"])

    elif arguments["func"] == "trimming":
        run_trimmer(arguments["inputdirs"])

    elif arguments["func"] == "resize":
        run_resizer(arguments["inputdirs"], arguments["width"], arguments["height"])

    elif arguments["func"] == "augmentation":
        run_augmenter(arguments["inputdirs"])

    elif arguments["func"] == "numpy_convert":
        run_numpy_converter(arguments["inputdirs"])

    elif arguments["func"] == "testdata_convert":
        run_testdata_converter(arguments["inputdirs"])

    elif arguments["func"] == "judge":
        run_judge(arguments["imagepath"], arguments["model"])

    t1 = time.time() # stop the timer
    total_time = t1 - t0
    print("Total time:" + str(total_time) + " Seconds")

if __name__ == "__main__":
    main()
