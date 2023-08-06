from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.oauth2.credentials import Credentials

import backoff
from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY

from .exceptions import GoogleAdsAccountLostAccessException

_GOOGLE_ADS_VERSION = "v7"


def get_exception_message(account_id: str, access_token: Optional[str] = None) -> str:
    if access_token:
        return F"We cannot access your account with the id: {account_id}. Are you sure you have access and entered correct ID?"
    else:
        return F"We cannot access your account with the id: {account_id} from the Arcane Manager Account. Are you sure you granted access and gave the correct ID?"


def get_google_ads_client(
    credentials_path: Optional[str] = None,
    access_token: Optional[str] = None,
    login_customer_id: Optional[str] = None,
    developer_token: Optional[str] = None

) -> GoogleAdsClient:
    """ credentials_path or access_token must be specified """

    if access_token:
        credentials = Credentials(token=access_token, scopes='https://www.googleapis.com/auth/adwords')
        return GoogleAdsClient(
            credentials,
            developer_token,
            login_customer_id=login_customer_id
        )
    elif credentials_path:
        return GoogleAdsClient.load_from_storage(credentials_path)
    else:
        raise ValueError('one of the following arguments must be specified: adscale_key or access_token')


def get_google_ads_service(service_name: str, google_ads_client: GoogleAdsClient, version: str = _GOOGLE_ADS_VERSION):
    return google_ads_client.get_service(service_name, version=version)

@backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
def check_access_account(
    account_id: str,
    adscale_key: Optional[str] = None,
    access_token: Optional[str] = None,
    login_customer_id: Optional[str] = None,
    developer_token: Optional[str] = None
):
    """From an account id check if Arcane has access to it"""

    google_ads_client = get_google_ads_client(adscale_key, access_token, login_customer_id, developer_token)
    google_ads_service = get_google_ads_service('GoogleAdsService', google_ads_client)

    query = f"""
        SELECT
          customer_client.manager
        FROM customer_client
        WHERE customer_client.id = '{account_id}'"""
    search_query = google_ads_client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_query.customer_id = account_id
    search_query.query = query
    try:
        response = list(google_ads_service.search(search_query))
        if len(response) == 0:
            raise GoogleAdsAccountLostAccessException(get_exception_message(account_id, access_token))
        response = response[0]
    except GoogleAdsException as err:
        if "USER_PERMISSION_DENIED" in str(err):
                raise GoogleAdsAccountLostAccessException(get_exception_message(account_id, access_token))
        elif "CUSTOMER_NOT_FOUND" in str(err):
            raise GoogleAdsAccountLostAccessException(f"We cannot find this account ({account_id}). Are you sure you entered the correct id?")
        else:
            raise GoogleAdsAccountLostAccessException(f"We cannot access this account ({account_id}). Are you sure you entered the correct id?")

    if response.customer_client.manager:
        raise GoogleAdsAccountLostAccessException('This account ID is a MCC. Please enter a Google Ads Account.')
