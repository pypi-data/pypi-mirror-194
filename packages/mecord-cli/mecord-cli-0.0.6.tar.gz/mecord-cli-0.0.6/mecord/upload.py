
from mecord import ftp_upload
from pathlib import Path

def upload(src):
    file_name = Path(src).name
    oss_path = f"ftp://192.168.3.220/1TB01/data/mecord/{file_name}"
    http_path = f"http://ftp.xinyu100.com/01/mecord/{file_name}"
    ftp_upload.upload(src)
    return http_path