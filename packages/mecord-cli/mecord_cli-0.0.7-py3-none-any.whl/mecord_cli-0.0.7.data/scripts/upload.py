import requests

from mecord import ftp_upload
from mecord import xy_pb
from pathlib import Path

def upload(src):
    file_name = Path(src).name
    oss_path = f"ftp://192.168.3.220/1TB01/data/mecord/{file_name}"
    http_path = f"http://ftp.xinyu100.com/01/mecord/{file_name}"
    ftp_upload.upload(src)
    return http_path

def uploadUseOss(src, widgetid):
    ossurl = xy_pb.GetOssUrl(widgetid)
    headers = dict()
    headers['Accept-Encoding'] = 'gzip'
    # headers['Content-Type'] = 'application/zip'
    # headers["x-oss-storage-class"] = "Standard"
    res = requests.put(ossurl, data=open(src, 'rb').read(), headers=headers)
    checkid = xy_pb.OssUploadEnd(widgetid)
    return ossurl, checkid


# import oss2
# import os

# from mecord import ftp_upload
# from pathlib import Path

# def upload(src):
#     file_name = Path(src).name
#     # oss_path = f"ftp://192.168.3.220/1TB01/data/mecord/{file_name}"
#     # http_path = f"http://ftp.xinyu100.com/01/mecord/{file_name}"
#     # ftp_upload.upload(src)

#     http_path = f"http://yesdesktop-web-beta.oss-cn-shenzhen.aliyuncs.com/local/mecord/widget/html/test.zip?Expires=1677650192&OSSAccessKeyId=STS.NSzzjmdm7LVJiERFfnJHBmSZp&Signature=zWhjKiMD/1VGenGe+ErYqXSlF8o=&security-token=CAIS7gF1q6Ft5B2yfSjIr5DPMdDZibIW+5Sha2PjomY7Rsdugpbxkjz2IHlLfHFpCekWs/s2mm9T6/oTlqN2RpRCX0DzdtdrtgKtDt4gO9ivgde8yJBZor/HcDHhJnyW9cvWZPqDP7G5U/yxalfCuzZuyL/hD1uLVECkNpv74vwOLK5gPG+CYCFBGc1dKyZ7tcYeLgGxD/u2NQPwiWeiZygB+Cgc0zsjsvXvmZOmh0CA3AGg+Ig8vJ/sJ5WoVc5oMapkXs29tO4MLfOeiHYJu0Eaqfgv0vMfpGuWpKiaGEJN5BaLNfDT9tB/JgJlb7jOtRklGoABWP9X3HARnZiJQJCFfqeO4NFBY0yq5gON1WBHSxbrZ0xDplR2/7a/ycgOeWaZiGu+KLfJ+ip0X+ZORjuOe6BkCKagWgp1i0CjgKwBi30u47sflL+Ykvq4Mk0Ze3LyQhIjyFW/LRCpUXKJjcAzmjlccfblF3FjMmyWNS2zhZuzNSc="
#     headers = dict()
#     headers['Accept-Encoding'] = 'gzip'
#     # headers['Content-Type'] = 'application/zip'
#     # headers["x-oss-storage-class"] = "Standard"
#     res = requests.put(http_path, data=open(src, 'rb').read(), headers=headers)
#     return http_path

# # upload(f"E:\\mecord_sd\\3333333333333333333333\\h5\\icon.zip")
# auth = oss2.Auth('LTAI5tEjgqmErzxZeuJb3YBq', 'vTDdiCuoDrV3sjNgnnrkeugAoAHVFk')
# bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'yesdesktop-web-beta')
# bucket.put_object_from_file('test.zip', 'E:\\mecord_sd\\3333333333333333333333\\h5\\icon.zip')
