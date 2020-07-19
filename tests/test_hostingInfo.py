from src.hostchecker.hostingInfo import HostInfo
import pytest
import requests

def test_HostInfo_datacenter_isSet():
    h = HostInfo(datacenter="Google LLC", domain="google.com")
    assert h.datacenter == "Google LLC"

def test_HostInfo_domain_isSet():
    h = HostInfo(datacenter="Google LLC", domain="google.com")
    assert h.domain == "google.com"

@pytest.mark.parametrize("url,expected", [
    ("https://google.com", "google.com"),
    ("http://google.com", "google.com"),
    ("google.com", "google.com"),
    ])
def test_getDomain_returnsDomain(url, expected):
    assert HostInfo.getDomain(url) == expected

class MockRequest:
    def __init__(self, status_code):
        self.status_code = status_code

def test_hostingInfo_defaultValues_ifPostWentBad(mocker):
    mockRequest = MockRequest(400)

    mocker.patch("requests.post", mocker.MagicMock(return_value=mockRequest))
    r = HostInfo.hostingInfo("https://google.com")
    assert r != None
    assert r.domain == ""
    assert r.datacenter == ""