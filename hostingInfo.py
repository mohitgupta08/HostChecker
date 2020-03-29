from pyquery import PyQuery
from urllib.parse import urlparse
import requests

class HostInfo:
    """
    Info about the host
    """

    def __init__(self, datacenter="", domain=""):
        self.datacenter = datacenter
        self.domain = domain
    
    @property
    def datacenter(self):
        return self._datacenter

    @datacenter.setter
    def datacenter(self, value):
        self._datacenter = HostInfo.correctDatacenter(value)
        self._completeDatacenter = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def completeDatacenter(self):
        return self._completeDatacenter

    @staticmethod
    def hostingInfo(url):
        """
        Get the host info about an URL

        :param url: String of the url of whitch retrive the info
        :return: Info about the hosting
        """
        if not url:
            raise ValueError("url is not present")
        
        domain = HostInfo.getDomain(url)

        r = requests.post("https://hostingchecker.com/wp-admin/admin-ajax.php", { 
                "action": "wx__domain_hostcheker",
                "domain": domain,
            })

        hostInfo = HostInfo()

        if r.status_code == requests.codes.ok:
            pq = PyQuery(r.text)
            hostInfo.datacenter = pq("li span").html() # Get the Datacenter info
            hostInfo.domain = domain

        return hostInfo

    @staticmethod
    def getDomain(url):
        """
        Get the Domain of an URL

        :param url: URL from whitch get the domain
        :return: Domain name
        """
        urlInfo = urlparse(url)

        # Method 'urlparse' populete field 'netloc' or 'path' depending if the url is only the domain or a complete url
        if urlInfo.netloc:
            return urlInfo.netloc
        else:
            return urlInfo.path

    @staticmethod
    def correctDatacenter(name):
        """
        For statistic purpose is usless if different company 
        """
        name = name.upper()
        if name.startswith("AWS") or name.startswith("AMAZON"):
            return "AWS"
        elif name.startswith("MICROSOFT"):
            return "Microsoft Azure Cloud"
        elif name.startswith("DIGITALOCEAN") or name.startswith("DIGITAL OCEAN"):
            return "Digital Ocean"
        else:
            return name
        