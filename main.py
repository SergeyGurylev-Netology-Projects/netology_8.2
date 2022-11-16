import sys
import requests
from config import TOKEN


class YaUploader:
    def __init__(self, token: str):
        self.base_host = 'https://cloud-api.yandex.net:443/'
        self.base_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token}'}

    def _get_upload_url(self, yandex_path: str):
        url = self.base_host + 'v1/disk/resources/upload'
        params = {"path": yandex_path, "overwrite": True}
        response = requests.get(url, params=params, headers=self.base_headers)
        return response

    def upload(self, file_path: str, yandex_path: str):
        response = self._get_upload_url(yandex_path)
        if response.status_code != 200:
            return dict(status_code=response.status_code, reason=response.reason)

        upload_url = response.json()['href']
        try:
            with open(file_path, 'rb') as data_file:
                response = requests.put(upload_url, data=data_file, headers=self.base_headers)
        except FileNotFoundError:
            return dict(status_code='FileNotFoundError', reason='File not found')

        return dict(status_code=response.status_code, reason=response.reason)


if __name__ == '__main__':
    # file_list = ['test_upload_1.txt', 'test_upload_2.txt', 'test_upload_3.txt']
    # список выгружаемых файлов передается в параметрах запуска
    file_list = sys.argv[1:]
    if len(file_list)==0:
        print('Files to upload are not specified')
        sys.exit()
    else:
        print(f'Number of files to upload {len(file_list)}...')

    uploader = YaUploader(TOKEN)

    for path_to_file in file_list:
        yandex_path = path_to_file
        result = uploader.upload(path_to_file, yandex_path)
        if result['status_code'] != 201:
            print(f'File "{path_to_file}" upload error. Code {result["status_code"]}: {result["reason"]}')
        else:
            print(f'File "{path_to_file}" uploaded successfully')
