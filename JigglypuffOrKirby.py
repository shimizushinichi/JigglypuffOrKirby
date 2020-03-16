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
    # parser.add_argument("", help="")
    # parser.add_argument("", help="")
    args_namespace = parser.parse_args()
    arguments = vars(args_namespace)
    return arguments

def run_crawler(site, character):
    import_file = "crawler.{}.crawler".format(site)
    crawler_module = importlib.import_module(import_file)
    crawler = crawler_module.ImageCrawler()
    crawler.get_images(character)

def run_trimmer(images_folder_path, character):
    assert os.path.isdir, "-imに指定されたディレクトリが見つかりません。input:{}".format(images_folder_path)
    assert character, "-chが空白か無効な値になっています。input:{}".format(character)
    import_file = "trimming.trimmer"
    trimmer_module = importlib.import_module(import_file)
    trimmer_module.trimmer(images_folder_path, character)

def main():
    arguments = user_input()
    if arguments["func"] == "crawler":
        run_crawler(arguments["site"], arguments["character"])

    elif arguments["func"] == "trimming":
        run_trimmer(arguments["images_folder_path"], arguments["character"])

    # elif arguments["func"] == augmentation:
    # elif arguments["func"] == learn:
    # elif arguments["func"] == judge:

if __name__ == "__main__":
    main()
