import logging

log = logging.getLogger("holiday_notify.helpers.http_helpers")

import typing as t
import httpx
from httpx import URL
from httpx._types import (
    QueryParamTypes,
    HeaderTypes,
    CookieTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    SyncByteStream,
    AsyncByteStream,
)


def build_request(
    method: str = "GET",
    url: t.Union[URL, str] = None,
    params: QueryParamTypes | None = None,
    headers: HeaderTypes | None = None,
    cookies: CookieTypes | None = None,
    content: RequestContent | None = None,
    data: RequestData | None = None,
    files: RequestFiles | None = None,
    json: t.Any | None = None,
    stream: t.Union[SyncByteStream, AsyncByteStream] | None = None,
    extensions: RequestExtensions | None = None,
):
    method = method.upper()

    try:
        req: httpx.Request = httpx.Request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            stream=stream,
            extensions=extensions,
        )
    except Exception as exc:
        msg = Exception(f"Unhandled exception building Request object. Details: {exc}")
        log.error(msg)

        raise exc

    return req
