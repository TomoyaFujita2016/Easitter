import pickle as pkl
import os

def confirmPklFile(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pkl.load(f)
    else:
        return []

def searchUrl(url, savedUrls):
    for sUrl in savedUrls:
        if url in sUrl:
            return sUrl
    return "NOT_FOUND!"
    
def main(urls):
    try:
        IMAGE_URL_PATH = "./PklData/IMAGE_URLS_PATH.pkl"
        urlList = confirmPklFile(IMAGE_URL_PATH)
        if len(urlList) == 0:
            return 0
    
        for url in urls:
            result = searchUrl(url, urlList)
            print(url + " -> " + result)
    
        return 0
    except Exception as e:
        print(e)

