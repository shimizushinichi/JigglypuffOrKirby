import argparse
import time

def user_input():
    parser = argparse.ArgumentParser(description="JigglypuffOrKirbyの各種機能を実行するためのプログラムです。")

    parser.add_argument("func", help="crawler, trimming, augmentation, learn, or judge", type=str, choices=["crawler, trimming, augmentation, learn, judge"])
    parser.add_argument("-s", "--site", help="website to crawl", type=str, default = "flickr", choices=["flickr"])
    parser.add_argument("-ch", "--character", help="Search word", type=str)
    # parser.add_argument("", help="")
    # parser.add_argument("", help="")
    # parser.add_argument("", help="")
    args_namespace = parser.parse_args()
    arguments = vars(args_namespace)
    return arguments

def main():


if __name__ == "__main__":
    main()
