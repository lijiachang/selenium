import sys

sys.path.append('.')
sys.path.append('..')

from core.spider import Spider91
from core.urlManger import UrlManger
from core.videosDownload import VideosDownload
from utils.identityCode import IdentityCode
from utils.logHandler import LogHandler
from core.config import CODE_INFO as info


def main():
    urlManger = UrlManger()
    videosDownload = VideosDownload()
    logHandler = LogHandler(__name__, level=40)
    identityCode = IdentityCode(info)
    spider = Spider91(urlManger, videosDownload, identityCode, logHandler)
    spider.start()


if __name__ == '__main__':
    main()
