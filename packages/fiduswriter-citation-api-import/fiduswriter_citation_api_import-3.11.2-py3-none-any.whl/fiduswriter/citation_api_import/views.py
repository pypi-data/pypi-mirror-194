from httpx import AsyncClient
from urllib.parse import urljoin
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpResponseForbidden
from django.http import HttpResponse

ALLOWED_DOMAINS = {
    "search.gesis.org": True,
    "api.datacite.org": True,
    "www.bioinformatics.org": True,
}


@sync_to_async
@login_required
@require_GET
@async_to_sync
async def proxy(request, url):
    domain = url.split("/")[2]
    if domain not in ALLOWED_DOMAINS:
        return HttpResponseForbidden()
    query_string = request.META["QUERY_STRING"]
    if len(query_string):
        url = f"{url}?{query_string}"
    async with AsyncClient() as client:
        response = await client.get(
            url,
            timeout=88,  # Firefox times out after 90 seconds, so we need to return before that.
        )
    return HttpResponse(response.text, status=response.status_code)
