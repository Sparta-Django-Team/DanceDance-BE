import json
from typing import Any, Dict

import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

from dance_dance.common.exception.exceptions import AuthenticationFailedException


@define
class KakaoLoginCredentials:
    client_id: str
    client_secret: str


@define
class KakaoAccessToken:
    access_token: str


class KakaoLoginFlowService:
    API_URI = reverse_lazy("api-users:kakao-login-callback")

    KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_ACCESS_TOKEN_OBTAIN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def __init__(self):
        self._credentials = kakao_login_get_credentials()

    def _get_redirect_uri(self) -> str:
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self) -> Dict[str, Any]:
        redirect_uri = self._get_redirect_uri()
        client_id = self._credentials.client_id
        return {"redirect_uri": redirect_uri, "client_id": client_id, "response_type": "code"}

    def get_authorization_url(self) -> str:
        client_config = self._generate_client_config()
        response = requests.get(self.KAKAO_AUTH_URL, params=client_config)

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get authorization url from Kakao.")
        return response.url

    def get_token(self, code: str) -> KakaoAccessToken:
        redirect_uri = self._get_redirect_uri()
        data = {
            "grant_type": "authorization_code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "client_secret": self._credentials.client_secret,
            "code": code,
        }
        response = requests.post(self.KAKAO_ACCESS_TOKEN_OBTAIN_URL, data=data)
        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get access token from Kakao.")

        kakao_token = KakaoAccessToken(access_token=response.json()["access_token"])
        return kakao_token

    def get_user_info(self, kakao_token: KakaoAccessToken) -> Dict[str, Any]:
        access_token = kakao_token.access_token
        response = requests.get(self.KAKAO_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})

        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get user info from Kakao.")
        return json.loads(response.text)


def kakao_login_get_credentials() -> KakaoLoginCredentials:
    client_id = settings.KAKAO_API_KEY
    client_secret = settings.KAKAO_SECRET_KEY

    if not client_id:
        raise ImproperlyConfigured("KAKAO_API_KEY missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("KAKAO_SECRET_KEY missing in env.")

    credentials = KakaoLoginCredentials(client_id=client_id, client_secret=client_secret)

    return credentials
