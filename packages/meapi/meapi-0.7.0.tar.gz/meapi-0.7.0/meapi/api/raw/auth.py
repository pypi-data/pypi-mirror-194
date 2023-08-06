from typing import TYPE_CHECKING, Dict, Union
from meapi.models.others import RequestType
from meapi.utils.helpers import HEADERS

if TYPE_CHECKING:  # always False at runtime.
    from meapi import Me


def activate_account_raw(client: 'Me', phone_number: int, activation_code: str) -> Dict[str, str]:
    """
    Activate your account with the activation code.

    :param client: :py:obj:`~meapi.Me` client object.
    :type client: :py:obj:`~meapi.Me`
    :param phone_number: International phone number format.
    :type phone_number: ``int``
    :param activation_code: Activation code.
    :type activation_code: ``str``
    :rtype: ``dict``

    Example::

        {
            "access": "eyxxxxKV1xxxxxx1NiJ9.xxx.xxx",
            "pwd_token": "xxxx-xxxx-xxxxx-xxxx-xxxxxxxxxxd2",
            "refresh": "xxxx.xxxxxx.xxxx-xxxxx-xxxx"
        }
    """
    body = {"activation_code": activation_code, "activation_type": "sms", "phone_number": phone_number}
    return client.make_request(method=RequestType.POST, endpoint='/auth/authorization/activate/', body=body,
                               headers=HEADERS.copy())


def generate_new_access_token_raw(client: 'Me', phone_number: str, pwd_token: str) -> dict:
    """
    Get new ``access_token``.

    :param client: :py:obj:`~meapi.Me` client object.
    :type client: :py:obj:`~meapi.Me`
    :param phone_number: International phone number format.
    :type phone_number: ``int``
    :param pwd_token: The ``pwd_token`` from the first activation (``activate_account_raw``).
    :type pwd_token: ``str``
    :rtype: ``dict``

    Example::

        {
            "access": "eyxxxxKV1xxxxxx1NiJ9.xxx.xxx",
            "refresh": "xxxx.xxxxxx.xxxx-xxxxx-xxxx"
        }
    """
    body = {"phone_number": phone_number, "pwd_token": pwd_token}
    return client.make_request(method=RequestType.POST, endpoint='/auth/authorization/login/', body=body)


def ask_for_call_raw(client: 'Me', phone_number: str, session_token: str) -> dict:
    """
    Ask Me to call you with the activation code.

    :param client: :py:obj:`~meapi.Me` client object.
    :type client: :py:obj:`~meapi.Me`
    :param phone_number: International phone number format.
    :type phone_number: ``int``
    :param session_token: Session token.
    :type session_token: ``str``
    :rtype: ``dict``

    Example::

        {
            "activation_type": "failb",
            "error_message": "",
            "provider_name": "TwilioCall",
            "success": True
        }
    """
    body = {"activation_type": "failb", "device_type": "android", "phone_number": phone_number}
    headers = HEADERS.copy()
    headers['session-token'] = session_token
    return client.make_request(method=RequestType.POST, endpoint='/auth/authorization/verify/', body=body,
                               headers=headers)


def ask_for_sms_raw(client: 'Me', phone_number: str, session_token: str) -> Dict[str, Union[str, bool]]:
    """
    Ask me to send you the activation code in SMS.

    :param client: :py:obj:`~meapi.Me` client object.
    :type client: :py:obj:`~meapi.Me`
    :param phone_number: International phone number format.
    :type phone_number: ``int``
    :param session_token: Session token.
    :type session_token: ``str``
    :rtype: ``dict``

    Example::

        {
            "activation_type": "sms",
            "error_message": "",
            "provider_name": "IsraelSms",
            "success": True
        }
    """
    body = {"activation_type": "sms", "device_type": "android", "app_token": "", "phone_number": phone_number}
    headers = HEADERS.copy()
    headers['session-token'] = session_token
    return client.make_request(method=RequestType.POST, endpoint='/auth/authorization/verify/', body=body,
                               headers=headers)
