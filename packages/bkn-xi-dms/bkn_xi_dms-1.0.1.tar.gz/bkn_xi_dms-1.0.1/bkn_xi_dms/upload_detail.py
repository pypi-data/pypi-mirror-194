import requests
from requests.packages import urllib3


def set_upload_document(id, path, link_upload_document, headers_upload):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    post_url = link_upload_document
    files = {'RemoteFile': open(path, 'rb')}

    payload = {
        "id": id
    }

    resp = requests.post(post_url, headers=headers_upload, files=files,
                         data=payload, verify=False)
    # print("====================================")
    # print("respon uploaded adalah", resp.content)
