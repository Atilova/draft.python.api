from typing import NamedTuple

from jwcrypto import jwk

from src.identity.domain import JWKS, RSAJWKPrivateKey, RSAJWKPublicKey
from src.identity.enum import (
    JWKKeyType,
    JWKKeyUse,
    RSAJWKKeyAlgorithm,
)


class JWKSServiceConfig(NamedTuple):
    rsa_key_algorithm: RSAJWKKeyAlgorithm


class JWKSService:
    __slots__ = ("_config",)

    def __init__(self, *, config: JWKSServiceConfig):
        self._config = config

    def generate_rsa_jwks(self, kid: str) -> JWKS[RSAJWKPublicKey, RSAJWKPrivateKey]:
        key = jwk.JWK.generate(
            kid=kid,
            kty=JWKKeyType.RSA,
            alg=self._config.rsa_key_algorithm,
            use=JWKKeyUse.SIG,
        )
        public_key = key.export_public(as_dict=True)
        private_key = key.export_private(as_dict=True)

        return JWKS(
            public_key=RSAJWKPublicKey.from_dict(public_key),
            private_key=RSAJWKPrivateKey.from_dict(private_key),
        )

    def validate_jwt[PublicKey: RSAJWKPublicKey](self, *, token: str, public_key: PublicKey):
        ...
        # try:
        #     jwt_token = jwt.JWT(
        #         jwt=token,
        #         key=jwk.JWK(**public_key._asdict()),
        #     )
        # except jwt.JWException:
        #     ...


