import argparse
import time
import os
import importlib

def user_input():
    parser = argparse.ArgumentParser(description="JigglypuffOrKirbyの各種機能を実行するためのプログラムです。")

    parser.add_argument("func", help="crawler, trimming, augmentation, learn, or judge", type=str, choices=["crawler", "trimming", "augmentation", "learn", "judge"])
    parser.add_argument("-s", "--site", help="website to crawl", type=str, default = "flickr", choices=["flickr"])
    parser.add_argument("-ch", "--character", help="Search word", type=str)
    parser.add_argument("-im", "--images_folder_path", help="The path of image's folder", type=str)
    parser.add_argument("-in", "--input", help="input folder path", type=str)
    parser.add_argument("-out", "--output", help="output folder path", type=str, default = "augmented")
    # parser.add_argument("", help="", type=str)
    # parser.add_argument("", help="", type=str)
    # parser.add_argument("", help="", type=str)

    args_namespace = parser.parse_args()
    arguments = vars(args_namespace)
    return arguments

def run_crawler(site, character):
    import_file = "crawler.{}.crawler".format(site)
    crawler_module = importlib.import_module(import_file)
    crawler = crawler_module.ImageCrawler()
    crawler.get_images(character)

def run_trimmer(images_folder_path, character):
    assert os.path.isdir(images_folder_path), "-imに指定されたディレクトリが見つかりません。input:{}".format(images_folder_path)
    assert character, "-chが空白か無効な値になっています。input:{}".format(character)
    import_file = "trimming.trimmer"
    trimmer_module = importlib.import_module(import_file)
    trimmer_module.trimmer(images_folder_path, character)

def run_augmenter(input_dir, output_dir, character):
    assert os.path.isdir(input_dir), "-inに指定されたディレクトリが見つかりません。input:{}".format(input_dir)
    assert character, "-chが空白か無効な値になっています。input:{}".format(character)
    import_file = "augmentation.augmenter"
    augmenter_module = importlib.import_module(import_file)
    augmenter_module.augmenter(input_dir, output_dir, character)

def main():
    arguments = user_input()
    if arguments["func"] == "crawler":
        run_crawler(arguments["site"], arguments["character"])

    elif arguments["func"] == "trimming":
        run_trimmer(arguments["images_folder_path"], arguments["character"])

    elif arguments["func"] == "augmentation":
        run_augmenter(arguments["input"], arguments["output"], arguments["character"])
    # elif arguments["func"] == learn:
    # elif arguments["func"] == judge:

if __name__ == "__main__":
    main()
