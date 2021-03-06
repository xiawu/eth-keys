from typing import Any


from eth_utils import (
    is_bytes,
    is_integer,
)
from eth_utils.toolz import curry

from newchain_keys.constants import (
    SECPR1_N,
)
from newchain_keys.exceptions import (
    ValidationError,
)


def validate_integer(value: Any) -> None:
    if not is_integer(value) or isinstance(value, bool):
        raise ValidationError("Value must be a an integer.  Got: {0}".format(type(value)))


def validate_bytes(value: Any) -> None:
    if not is_bytes(value):
        raise ValidationError("Value must be a byte string.  Got: {0}".format(type(value)))


@curry
def validate_gte(value: Any, minimum: int) -> None:
    validate_integer(value)
    if value < minimum:
        raise ValidationError(
            "Value {0} is not greater than or equal to {1}".format(
                value, minimum,
            )
        )


@curry
def validate_lte(value: Any, maximum: int) -> None:
    validate_integer(value)
    if value > maximum:
        raise ValidationError(
            "Value {0} is not less than or equal to {1}".format(
                value, maximum,
            )
        )


validate_lt_secpk1n = validate_lte(maximum=SECPR1_N - 1)


def validate_message_hash(value: Any) -> None:
    validate_bytes(value)
    if len(value) != 32:
        raise ValidationError("Unexpected signature format.  Must be length 65 byte string")


def validate_public_key_bytes(value: Any) -> None:
    validate_bytes(value)
    if len(value) != 64:
        raise ValidationError("Unexpected public key format.  Must be length 64 byte string")


def validate_private_key_bytes(value: Any) -> None:
    validate_bytes(value)
    if len(value) != 32:
        raise ValidationError("Unexpected private key format.  Must be length 32 byte string")


def validate_signature_bytes(value: Any) -> None:
    validate_bytes(value)
    if len(value) != 65:
        raise ValidationError("Unexpected signature format.  Must be length 65 byte string")
