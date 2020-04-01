import datetime
import chrome_bookmarks

from hostingInfo import HostInfo
from hostStorage import HostStorage

def retriveInfo(domain, hostStorage, useCache):
    hostInfo = hostStorage.getHostInfo(domain)
    
    if hostInfo == None and useCache:
        start = datetime.datetime.now()
        hostInfo = HostInfo.hostingInfo(domain)
        end = datetime.datetime.now()

        delta = end - start
        time = str(delta.total_seconds())

        hostStorage.cache([hostInfo])
    else:
        time = "Loaded from cache"

    print("{:20} {:30} {}".format(hostInfo.domain, str(hostInfo.datacenter), time))



if __name__ == "__main__":
    urls = set()
    hostStorage = HostStorage("host_info.sqlite3")

    for url in chrome_bookmarks.urls:
        domain = HostInfo.getDomain(url.url)
        urls.add(domain)
    
    print("Found " + str(len(urls)) + " favorites")

    for u in urls:
        retriveInfo(u, hostStorage, True)