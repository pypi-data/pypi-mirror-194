from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.card_create_card_request import CardCreateCardRequest
from ...models.card_create_card_response import CardCreateCardResponse
from ...types import Response


def _get_kwargs(
    aid: str,
    *,
    client: Client,
    json_body: CardCreateCardRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/accounts/{aid}/cards"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[CardCreateCardResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CardCreateCardResponse.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CardCreateCardResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    aid: str,
    *,
    client: Client,
    json_body: CardCreateCardRequest,
) -> Response[CardCreateCardResponse]:
    """Create a new virtual card

    Args:
        aid (str):
        json_body (CardCreateCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCreateCardResponse]
    """

    kwargs = _get_kwargs(
        aid=aid,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aid: str,
    *,
    client: Client,
    json_body: CardCreateCardRequest,
) -> Optional[CardCreateCardResponse]:
    """Create a new virtual card

    Args:
        aid (str):
        json_body (CardCreateCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCreateCardResponse]
    """

    return sync_detailed(
        aid=aid,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    aid: str,
    *,
    client: Client,
    json_body: CardCreateCardRequest,
) -> Response[CardCreateCardResponse]:
    """Create a new virtual card

    Args:
        aid (str):
        json_body (CardCreateCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCreateCardResponse]
    """

    kwargs = _get_kwargs(
        aid=aid,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aid: str,
    *,
    client: Client,
    json_body: CardCreateCardRequest,
) -> Optional[CardCreateCardResponse]:
    """Create a new virtual card

    Args:
        aid (str):
        json_body (CardCreateCardRequest): Card

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardCreateCardResponse]
    """

    return (
        await asyncio_detailed(
            aid=aid,
            client=client,
            json_body=json_body,
        )
    ).parsed
