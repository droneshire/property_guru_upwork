from property_guru.headers import PROPERTY_GURU_API_HEADERS
from util.web2_client import Web2Client


class ApiCall:
    URL = ""
    DATA = ""
    HEADERS = None


class CreateSearch(ApiCall):
    URL = "https://www.propertyguru.com.sg/sf2-search/ajax/save-search/create"
    HEADERS = PROPERTY_GURU_API_HEADERS
    DATA = """------WebKitFormBoundaryjr3TeItenploVwLDContent-Disposition: form-data; name="additionalParams"

{{}}
------WebKitFormBoundaryjr3TeItenploVwLD
Content-Disposition: form-data; name="alert"

1
------WebKitFormBoundaryjr3TeItenploVwLD
Content-Disposition: form-data; name="application"

WEB
------WebKitFormBoundaryjr3TeItenploVwLD
Content-Disposition: form-data; name="email"

info.crabada.bot@gmail.com
------WebKitFormBoundaryjr3TeItenploVwLD
Content-Disposition: form-data; name="locale"

en
------WebKitFormBoundaryjr3TeItenploVwLD
Content-Disposition: form-data; name="searchCriteriaText"

Property for sale in Singapore, S$ 1,400,000 Max., at The Woodleigh Residences
------WebKitFormBoundaryjr3TeItenploVwLD
Content-Disposition: form-data; name="searchParams"

{}
------WebKitFormBoundaryjr3TeItenploVwLD
Content-Disposition: form-data; name="source"

www.propertyguru.com.sg
------WebKitFormBoundaryjr3TeItenploVwLD--

"""


class PropertyForSale(ApiCall):
    URL = "https://www.propertyguru.com.sg/property-for-sale"
    HEADERS = PROPERTY_GURU_API_HEADERS
