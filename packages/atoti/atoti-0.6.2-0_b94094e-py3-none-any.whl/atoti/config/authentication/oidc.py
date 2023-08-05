import warnings
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence, Union

from .._utils import Config


@dataclass(frozen=True)
class OidcConfig(Config):
    """The configuration to connect to an `OpenID Connect <https://openid.net/connect/>`__ authentication provider (Auth0, Google, Keycloak, etc.).

    Example:

        >>> config = {
        ...     "authentication": {
        ...         "oidc": {
        ...             "provider_id": "auth0",
        ...             "issuer_url": "https://example.auth0.com",
        ...             "client_id": "some client ID",
        ...             "client_secret": "some client secret",
        ...             "name_claim": "email",
        ...             "scopes": ["email", "profile"],
        ...             "roles_claims": [
        ...                 "https://example:com/roles",
        ...                 ["other", "path", "to", "roles"],
        ...             ],
        ...             "role_mapping": {
        ...                 "dev_team": {"ROLE_USER", "ROLE_DEV"},
        ...                 "admin": {"ROLE_ADMIN"},
        ...             },
        ...         }
        ...     }
        ... }

        .. doctest::
            :hide:

            >>> validate_config(config)

    """

    provider_id: str
    """The name of the provider.

    It is used to build the redirect URL: ``f"{session_url}/login/oauth2/code/{provider_id}"``.
    """

    issuer_url: str
    """The issuer URL parameter from the provider's OpenID Connect configuration endpoint."""

    client_id: str
    """The app's client ID, obtained from the authentication provider."""

    client_secret: str
    """The app's client secret, obtained from the authentication provider."""

    name_claim: Optional[str] = None
    """The name of the claim in the ID token to use as the name of the user."""

    paths_to_authorities: Optional[Sequence[str]] = None
    """The path to the authorities to use in atoti in the returned access token or ID token.

    This configuration option is deprecated, :attr:`roles_claims` should be used instead.
    """

    roles_claims: Optional[Sequence[Union[str, Sequence[str]]]] = None
    """The claims of the ID token from which to extract roles to use as keys in the :attr:`role_mapping`.

    When the elements of the sequence are also sequences, the inner elements will be used as a path pointing to a nested value in the token.
    """

    scopes: Optional[Sequence[str]] = None
    """The scopes to request from the authentication provider."""

    role_mapping: Optional[Mapping[str, Sequence[str]]] = None
    """The mapping between the roles returned by the authentication provider and the roles to grant in atoti.

    Users without the role :guilabel:`ROLE_USER` will not have access to the application.
    """

    def __post_init__(self):
        if self.__dict__["paths_to_authorities"] is not None:
            if self.__dict__["roles_claims"] is not None:
                raise ValueError(
                    "paths_to_authorities and roles_claims should not be used at the same time."
                )
            warnings.warn(
                "paths_to_authorities is deprecated, use roles_claims instead."
            )
            self.__dict__["roles_claims"] = [
                path.split("/") for path in self.__dict__["paths_to_authorities"]
            ]
            del self.__dict__["paths_to_authorities"]
        self.__dict__["roles_claims"] = (
            [
                [role_claim] if isinstance(role_claim, str) else role_claim
                for role_claim in self.roles_claims
            ]
            if self.roles_claims is not None
            else None
        )
