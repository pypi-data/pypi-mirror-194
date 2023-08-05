from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.rule_create_rule_request import RuleCreateRuleRequest
from ...models.rule_rule_response import RuleRuleResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Dict[str, Any]:
    url = f"{client.base_url}/rules"

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[RuleRuleResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = RuleRuleResponse.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[RuleRuleResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Response[RuleRuleResponse]:
    """Create a Rule

     When you want a new rule on an account you can create one with this endpoint. Note that Rules are
    linked to an Account and each Account can only have one instance of a Rule type

    Args:
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Optional[RuleRuleResponse]:
    """Create a Rule

     When you want a new rule on an account you can create one with this endpoint. Note that Rules are
    linked to an Account and each Account can only have one instance of a Rule type

    Args:
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Response[RuleRuleResponse]:
    """Create a Rule

     When you want a new rule on an account you can create one with this endpoint. Note that Rules are
    linked to an Account and each Account can only have one instance of a Rule type

    Args:
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: RuleCreateRuleRequest,
) -> Optional[RuleRuleResponse]:
    """Create a Rule

     When you want a new rule on an account you can create one with this endpoint. Note that Rules are
    linked to an Account and each Account can only have one instance of a Rule type

    Args:
        json_body (RuleCreateRuleRequest): create rule request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleRuleResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
