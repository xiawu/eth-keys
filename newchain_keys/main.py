from typing import (Any, Union, Type)  # noqa: F401

from newchain_keys.datatypes import (
    LazyBackend,
    PublicKey,
    PrivateKey,
    Signature,
)
from newchain_keys.exceptions import (
    ValidationError,
)
from newchain_keys.validation import (
    validate_message_hash,
)


# These must be aliased due to a scoping issue in mypy
# https://github.com/python/mypy/issues/1775
_PublicKey = PublicKey
_PrivateKey = PrivateKey
_Signature = Signature


class KeyAPI(LazyBackend):
    #
    # datatype shortcuts
    #
    PublicKey = PublicKey  # type: Type[_PublicKey]
    PrivateKey = PrivateKey  # type: Type[_PrivateKey]
    Signature = Signature  # type: Type[_Signature]

    #
    # Proxy method calls to the backends
    #
    def ecdsa_sign(self,
                   message_hash: bytes,
                   private_key: _PrivateKey) -> _Signature:
        validate_message_hash(message_hash)
        if not isinstance(private_key, PrivateKey):
            raise ValidationError(
                "The `private_key` must be an instance of `newchain_keys.datatypes.PrivateKey`"
            )
        signature = self.backend.ecdsa_sign(message_hash, private_key)
        if not isinstance(signature, Signature):
            raise ValidationError(
                "Backend returned an invalid signature.  Return value must be "
                "an instance of `newchain_keys.datatypes.Signature`"
            )
        return signature

    def ecdsa_verify(self,
                     message_hash: bytes,
                     signature: _Signature,
                     public_key: _PublicKey) -> bool:
        if not isinstance(public_key, PublicKey):
            raise ValidationError(
                "The `public_key` must be an instance of `newchain_keys.datatypes.PublicKey`"
            )
        return self.ecdsa_recover(message_hash, signature) == public_key

    def ecdsa_recover(self,
                      message_hash: bytes,
                      signature: _Signature) -> _PublicKey:
        validate_message_hash(message_hash)
        if not isinstance(signature, Signature):
            raise ValidationError(
                "The `signature` must be an instance of `newchain_keys.datatypes.Signature`"
            )
        public_key = self.backend.ecdsa_recover(message_hash, signature)
        if not isinstance(public_key, _PublicKey):
            raise ValidationError(
                "Backend returned an invalid public_key.  Return value must be "
                "an instance of `newchain_keys.datatypes.PublicKey`"
            )
        return public_key

    def private_key_to_public_key(self, private_key: _PrivateKey) -> _PublicKey:
        if not isinstance(private_key, PrivateKey):
            raise ValidationError(
                "The `private_key` must be an instance of `newchain_keys.datatypes.PrivateKey`"
            )
        public_key = self.backend.private_key_to_public_key(private_key)
        if not isinstance(public_key, PublicKey):
            raise ValidationError(
                "Backend returned an invalid public_key.  Return value must be "
                "an instance of `newchain_keys.datatypes.PublicKey`"
            )
        return public_key


# This creates an easy to import backend which will lazily fetch whatever
# backend has been configured at runtime (as opposed to import or instantiation time).
lazy_key_api = KeyAPI(backend=None)
