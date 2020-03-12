class flickr_api_cralwer():
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
        画像の保存先は./savedir/characterとなります。

        Args:
            character(int):検索キーワード。jigglypuffかkirby
            savedir(str):保存先フォルダ名。デフォルトはdownloads
        """
        from flickrapi import FlickrAPI
        from urllib.request import urlretrieve
        import os, time, sys

        wait_time = 1
        savepath = savedir+"/"+character
        try:
            os.makedirs(savepath)
        except FileExistsError:
            pass

        flickr = FlickrAPI(self.key, self.secret, format="parsed-json")
        result = flickr.photos.search(
            text = character,
            per_page = 10,
            media = "photos",
            sort = "relevance",
            safe_search = 1,
            extras = "url_c"
            #url_cが存在しない画像が複数ある。サイズ指定せず取得する方法があるか調べる必要がある。
        )
        for item in result["photos"]["photo"]:
            url = item["url_c"]
            filepath = savepath + "/" + item["id"] + ".jpg"
            if os.path.exists(filepath):
                continue
            urlretrieve(url, filepath)
            time.sleep(wait_time)

test = flickr_api_cralwer()
test.get_images("jigglypuff")
