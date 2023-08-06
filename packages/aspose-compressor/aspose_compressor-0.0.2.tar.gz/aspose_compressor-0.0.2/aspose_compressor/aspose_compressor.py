import requests,urllib3,time
urllib3.disable_warnings()

class DownloadedFile:
    def __init__(self, link: str):
        self.link = link

    def save(self, path: str):
        """Downloads compressed video
        `path`: Path to save your video.
        ```py
        file = ac.compress_video("./video.mp4")
        file.save("./output.mp4")
        ```
        """
        binaries = requests.get(self.link).content
        open(path, "wb").write(binaries)

class AsposeCompressor:
    def __init__(self):
        """
        ```py
        ac = AsposeCompressor()
        ```
        """

    def compress_video(self, path_to_file: str) -> str:
        """Returns the download link for the compressed file
        ```py
        ac = AsposeCompressor()
        file = ac.compress_video("./video.mp4")
        ```
        """
        self.files = {
            '1': open(path_to_file, 'rb'),
            'VideoFormat': (None, 'mp4'),
        }

        print("[!] Compressing video")
        response = requests.post('https://api.products.aspose.app/video/compress/api/compress', files=self.files, verify=False)
        file_request_id = response.json()["Data"]["FileRequestId"]
        params = {
            'fileRequestId': file_request_id,
        }
        response = None

        print("[!] Fetching download link")
        response = requests.get(
            'https://api.products.aspose.app/video/compress/api/compress/HandleStatus',
            params=params,
            verify=False,
        )

        while response.json()["Data"]["DownloadLink"] == None:
            response = requests.get(
                'https://api.products.aspose.app/video/compress/api/compress/HandleStatus',
                params=params,
                verify=False,
            )
            time.sleep(5)
        print("[!] Compression finished")
        return DownloadedFile(response.json()["Data"]["DownloadLink"])