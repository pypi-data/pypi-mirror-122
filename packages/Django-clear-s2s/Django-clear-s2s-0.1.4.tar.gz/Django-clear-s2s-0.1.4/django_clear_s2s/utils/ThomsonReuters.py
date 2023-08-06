import requests
import requests_pkcs12
import pprint
import xmltodict
import datetime
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from django_soap.utils.SOAPHandlerBase import SOAPHandlerBase
from django.conf import settings
from django.utils import timezone
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from django_clear_s2s.utils.exceptions import ThomsonReutersException
from django_soap.models import SOAPRequestLogger, SOAPResponseLogger



class ThomsonReuters(SOAPHandlerBase):
    TOKEN_URL = "https://api.thomsonreuters.com/tr-oauth/v1/token"
    TEMPLATES = {
        'PersonSearch': 'django_clear_s2s/PersonSearchRequest.xml',
        'BusinessSearch': 'django_clear_s2s/BusinessSearchRequest.xml',
        'EIDVPersonSearch': 'django_clear_s2s/EIDVPersonSearch.xml',
        'PersonQuickAnalysisFlagRequest': 'django_clear_s2s/PersonQuickAnalysisFlagRequest.xml',
        'CompanyQuickAnalysisFlagRequest': 'django_clear_s2s/CompanyQuickAnalysisFlagRequest.xml',
        'WebAndSocialMediaSearchRequest': 'django_clear_s2s/WebAndSocialMediaSearchRequest.xml'
    }


    def __init__(self):
        retry_strategy = Retry(
            total=5,
            backoff_factor=10,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"]
        )
        if not getattr(settings, 'TR_CLEAR_S2S_USER', None):
            self.adapter = HTTPAdapter(max_retries=retry_strategy)
            self.http = requests.Session()
            self.base_url = settings.TR_CLEAR_S2S_HOST
            self.auth = None
            self.auth = HTTPBasicAuth(settings.TR_CLEAR_S2S_USER, settings.TR_CLEAR_S2S_PASS)

        self.authenticate()
    
    def authenticate(self):
        if not settings.TR_CLEAR_S2S_USER:
            _headers = {
                "Content-Type": "application/x-www-form-urlencoded", 
                "Accept": "application/json"
            }
            data = {
                'client_id': settings.TR_CLEAR_S2S_CLIENT_ID,
                'client_secret': settings.TR_CLEAR_S2S_CLIENT_SECRET,
                'scopes': settings.TR_CLEAR_S2S_SCOPES, 
                'grant_type': 'client_credentials'
            }
            res = requests.post(self.TOKEN_URL, data=data, headers=_headers)
            token = res.json()['access_token']
            self.headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/xml'}
            self.cert = None
        else:
            self.headers = {'Content-Type': 'application/xml'}
            self.cert = (settings.TR_CLEAR_S2S_CERT_PATH, settings.TR_CLEAR_S2S_CERT_KEY_PATH)
    
    def get_results(self, url, body=None, log=None, *args, **kwargs):
        params = {'data': body, 'headers': self.headers}
        req_log = SOAPRequestLogger.objects.create(
            method='GET',
            url=url,
            headers=str(self.headers),
            body=None,            
        )
        
        response2 = self.http.get(
            url,
            params={'startGroup': 0, 'direction': 'dsc', 'sortBy': 'relevance', 'maxGroups': 1},  # ensure we only ever get the most relevant result
            headers=self.headers
        )

        req_log.request_time_ms = (
            datetime.datetime.now(timezone.utc) - req_log.date_sent
        ).microseconds
        req_log.save()

        SOAPResponseLogger.objects.create(
            request_id=req_log,
            status=response2.status_code,
            headers=str(response2.headers),
            body=str(response2.content),
        )

        return xmltodict.parse(response2.content)

    # TODO a lot of duplication blocks w/ only 3 line changes, maybe open one method with selections by param
    def person_search(self, **kwargs):
        response1 = self.post(
            self.TEMPLATES['PersonSearch'], 
            {**kwargs, 'url': self.base_url + '/v2/person/searchResults'}
        )
        print(response1)
        
        response2 = None
        url = response1.find('ns2:PersonResults').get('Uri')
        if url != None:
            response2 = self.get_results(url)
            
        return (response1, response2)

    def eidv_person_search(self, **kwargs):
        response1 = self.post(
            self.TEMPLATES['EIDVPersonSearch'], 
            {**kwargs, 'url': self.base_url + '/v2/eidvperson/searchResults'}
        )
        response2 = None
        url = response1.find('ns2:EIDVPersonResults').get('Uri')
        if url != None:
            response2 = self.get_results(url)

        return (response1, response2)

    def business_search(self, **kwargs):
        response1 = self.post(
            self.TEMPLATES['BusinessSearch'], 
            {**kwargs, 'url': self.base_url + '/v2/business/searchResults'}
        )
        response2 = None
        url = response1.find('ns2:BusinessResults').get('Uri')
        if url != None:
            response2 = self.get_results(url)
        return (response1, response2)

    def person_quick_analysis_search(self, **kwargs):
        response1 = self.post(
            self.TEMPLATES['PersonQuickAnalysisFlagRequest'],
            {**kwargs, 'url': self.base_url + '/v2/person/quickanalysis/searchResults'}
        )
        response2 = None
        url = response1.find('ns2:PersonQuickAnalysisFlagResults').get('Uri')
        if url != None:
            response2 = self.get_results(url)
        return (response1, response2)

    def business_quick_analysis_search(self, **kwargs):
        response1 = self.post(
            self.TEMPLATES['CompanyQuickAnalysisFlagRequest'],
            {**kwargs, 'url': self.base_url + '/v2/business/quickanalysis/searchResults'}
        )
        response2 = None
        url = response1.find('ns2:CompanyQuickAnalysisFlagResults').get('Uri')
        if url != None:
            response2 = self.get_results(url)
        return (response1, response2)
    
    def social_media_search(self, **kwargs):
        response1 = self.post(
            self.TEMPLATES['WebAndSocialMediaSearchRequest'],
            {**kwargs, 'url': self.base_url + '/v2/webandsocialmedia/searchResults'}
        )
        response2 = None
        url = response1.find('ns2:WebAndSocialMediaSearchResults').get('Uri')
        if url != None:
            response2 = self.get_results(url)
        return (response1, response2)
