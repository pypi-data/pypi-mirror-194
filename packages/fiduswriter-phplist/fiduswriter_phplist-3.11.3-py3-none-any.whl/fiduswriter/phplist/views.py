import json
from httpx import AsyncClient, HTTPError
from asgiref.sync import async_to_sync, sync_to_async
from urllib.parse import urljoin

from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.conf import settings

from allauth.account.models import EmailAddress


@sync_to_async
@require_POST
@async_to_sync
async def subscribe_email(request):
    if not hasattr(settings, "PHPLIST_BASE_URL"):
        return HttpResponse()
    url = urljoin(settings.PHPLIST_BASE_URL, "/admin/?page=call&pi=restapi")
    login_data = {
        "cmd": "login",
        "login": settings.PHPLIST_LOGIN,
        "password": settings.PHPLIST_PASSWORD,
    }
    if hasattr(settings, "PHPLIST_SECRET"):
        login_data["secret"] = settings.PHPLIST_SECRET
    try:
        async with AsyncClient() as client:
            response = await client.post(url, data=login_data)
            response.raise_for_status()
    except HTTPError:
        return HttpResponse(status=404)
    session_cookie = response.headers["Set-Cookie"]
    email = request.POST["email"]
    email_object = EmailAddress.objects.filter(email=email).first()
    if not email_object:
        return HttpResponse(status=500)
    data = {
        "cmd": "subscriberAdd",
        "email": email,
        "foreignkey": "",
        "confirmed": 1,
        "htmlemail": 1,
        "disabled": 0,
    }
    if hasattr(settings, "PHPLIST_SECRET"):
        data["secret"] = settings.PHPLIST_SECRET
    async with AsyncClient() as client:
        response = await client.post(
            url, headers={"Cookie": session_cookie}, data=data
        )
        response.raise_for_status()
    response_json = json.loads(response.content)
    if response_json["status"] == "error":
        # could not create user with this email
        return HttpResponse(status=500)
    subscriber_id = response_json["data"]["id"]
    subscriber_add_data = {
        "cmd": "listSubscriberAdd",
        "list_id": settings.PHPLIST_LIST_ID,
        "subscriber_id": subscriber_id,
    }
    if hasattr(settings, "PHPLIST_SECRET"):
        subscriber_add_data["secret"] = settings.PHPLIST_SECRET
    async with AsyncClient() as client:
        response = await client.post(
            url, headers={"Cookie": session_cookie}, data=subscriber_add_data
        )
        response.raise_for_status()
    return HttpResponse(status=201)
