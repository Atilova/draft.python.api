from enum import StrEnum, auto


class UpperStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,  # noqa: ARG004
        count: int,  # noqa: ARG004
        last_values: list[str],  # noqa: ARG004
    ) -> str:
        return name.upper()


class JWKKeyType(UpperStrEnum):
    RSA = auto()


class JWKKeyUse(StrEnum):
    SIG = auto()


class RSAJWKKeyAlgorithm(UpperStrEnum):
    RS256 = auto()
    RS384 = auto()
    RS512 = auto()
    PS256 = auto()
    PS384 = auto()
    PS512 = auto()
