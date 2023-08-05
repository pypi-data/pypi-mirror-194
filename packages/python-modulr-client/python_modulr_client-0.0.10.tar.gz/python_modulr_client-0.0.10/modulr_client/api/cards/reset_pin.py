from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.card_reset_card_pin_request import CardResetCardPinRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: CardResetCardPinRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = f"{client.base_url}/cards/{id}/pin"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(x_mod_card_mgmt_token, Unset):
        headers["X-MOD-CARD-MGMT-TOKEN"] = x_mod_card_mgmt_token

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        return None
    if response.status_code == HTTPStatus.FORBIDDEN:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    json_body: CardResetCardPinRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Reset card PIN

     Reset the card's PIN for a specific card

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):
        json_body (CardResetCardPinRequest): Reset PIN

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        x_mod_card_mgmt_token=x_mod_card_mgmt_token,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: CardResetCardPinRequest,
    x_mod_card_mgmt_token: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Reset card PIN

     Reset the card's PIN for a specific card

    Args:
        id (str):
        x_mod_card_mgmt_token (Union[Unset, str]):
        json_body (CardResetCardPinRequest): Reset PIN

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        x_mod_card_mgmt_token=x_mod_card_mgmt_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
