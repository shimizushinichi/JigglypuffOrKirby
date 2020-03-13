class ImageCrawler():
    def __init__(self):
        """flickrで使用するAPIKeyを同ディレクトリのファイルから読み込みます。
        同ディレクトリにflickrAPIkey.jsonというファイルを用意してください。
        APIKeyはhttps://www.flickr.com/services/api/のAPI Keysから取得してください。

        """
        import json
        with open("flickrAPIkey.json") as f:
            df = json.load(f)
        self.key = df["key"]
        self.secret = df["secret"]

    def get_images(self, character,savedir="downloads"):
        """flickrからAPIで画像を取得して保存します。
        画像の保存先は./savedir/flickr/characterとなります。

        Args:
            character(int):検索キーワード。jigglypuffかkirby
            savedir(str):保存先フォルダ名。デフォルトはdownloads
        """
        from flickrapi import FlickrAPI
        from urllib.request import urlretrieve
        import os, time, sys

        wait_time = 1
        savepath = savedir+"/flickr/"+character
        try:
            os.makedirs(savepath)
        except FileExistsError:
            pass

        flickr = FlickrAPI(self.key, self.secret, format="parsed-json")
        result = flickr.photos.search(
            text = character,
            per_page = 500,
            media = "photos",
            sort = "relevance",
            safe_search = 1
        )

        for item in result["photos"]["photo"]:
            url = "https://live.staticflickr.com/{0}/{1}_{2}.jpg".format(item["server"],item["id"],item["secret"])
            filepath = savepath + "/" + item["id"] + ".jpg"
            if os.path.exists(filepath):
                continue
            urlretrieve(url, filepath)
            time.sleep(wait_time)
