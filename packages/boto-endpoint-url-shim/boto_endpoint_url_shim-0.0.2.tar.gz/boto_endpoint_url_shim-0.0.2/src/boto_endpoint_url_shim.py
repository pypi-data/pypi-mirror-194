# Copyright 2023 Louis Cochen <louis.cochen@protonmail.ch>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import os
import typing
import warnings

import boto3
import botocore

if typing.TYPE_CHECKING:
    from typing import Callable, TypeVar

    S = TypeVar("S", bound=botocore.session.Session)

BOTOCORE_PATCHED = {}  # type: ignore

SERVICE_ENV_VAR = "AWS_{}_ENDPOINT_URL"
GLOBAL_ENV_VAR = "AWS_ENDPOINT_URL"

_SERVICE_ENDPOINT_URL_MAP: dict[str, str] = None  # type: ignore


def read_service_env_var(session: S, service_id: str) -> str | None:
    """Read from service-specific environment variable.

    Example:
    ```sh
    AWS_DYNAMODB_ENDPOINT_URL=http://localhost:8024
    AWS_ELASTIC_BEANSTALK_ENDPOINT_URL=http://localhost:8053
    ```
    """
    return os.environ.get(SERVICE_ENV_VAR.format(service_id.upper()))


def read_global_env_var(session: S, service_id: str) -> str | None:
    """Read from global environment variable.

    Example:
    ```sh
    AWS_ENDPOINT_URL=http://localhost:8099
    ```
    """
    return os.environ.get(GLOBAL_ENV_VAR)


def read_service_config_file(session: S, service_id: str) -> str | None:
    """Read from service-specific parameter from the shared configuration file.

    Example:
    ```ini
    [services local-db-eb]
    dynamodb =
        endpoint_url = http://localhost:8024
    elastic_beanstalk =
        endpoint_url = http://localhost:8053
    [profile testing]
    services = local-db-eb
    ```
    """
    services_config = _get_services_config(session)
    service_config = services_config.get(service_id, {})
    return service_config.get("endpoint_url")


def read_global_config_file(session: S, service_id: str) -> str | None:
    """Read from global parameter from the shared configuration file.

    Example:
    ```ini
    [services local-services]
    endpoint_url = http://localhost:8099
    [profile testing]
    services = local-services
    ```
    """
    services_config = _get_services_config(session)
    return services_config.get("endpoint_url")


def _get_services_config(session: S) -> dict:
    profile_config = session.get_scoped_config()
    try:
        services_key = profile_config["services"]
        services_config = session.full_config["services"][services_key]
    except KeyError:
        services_config = {}
    return services_config


def read_mapping_env_var(session: S, service_id: str) -> str | None:
    """Read mapping from global environment variable.

    Example:
    ```sh
    AWS_ENDPOINT_URL="dynamodb=http://localhost:8024,elastic_beanstalk=http://localhost:8053"
    ```
    """
    if _SERVICE_ENDPOINT_URL_MAP is None:
        _parse_mapping(os.environ.get(GLOBAL_ENV_VAR))

    return _SERVICE_ENDPOINT_URL_MAP.get(service_id)


def _parse_mapping(raw_mapping: str | None) -> None:
    global _SERVICE_ENDPOINT_URL_MAP

    if raw_mapping:
        _SERVICE_ENDPOINT_URL_MAP = dict(
            pair.split("=", maxsplit=1) for pair in raw_mapping.split(",")
        )
    else:
        _SERVICE_ENDPOINT_URL_MAP = {}
        warnings.warn(f"{GLOBAL_ENV_VAR} is unset or empty", RuntimeWarning)


def read_named_top_level_config_file(
    session: S, service_id: str
) -> str | None:
    """Read from named top level parameter from the shared configuration file.

    Example:
    ```ini
    [profile local-services]
    dynamodb_endpoint_url = http://localhost:8024
    elastic_beanstalk_endpoint_url = http://localhost:8053
    ```
    """
    profile_config = session.get_scoped_config()
    return profile_config.get(f"{service_id}_endpoint_url")


def _custom_build_profile_map(
    parsed_ini_config: dict,
) -> dict:  # pragma: no cover
    """Convert parsed INI config into services map.

    Modified from `botocore.botocore.configloader.build_profile_map`.

    The modifications fall under the licence and copyright listed in the notice
    at the top of this file.

    The following notice affects only the source material on upon which this
    function is built.

    === botocore configloader.py notice begin  # noqa: E501

    Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
    Copyright 2012-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You
    may not use this file except in compliance with the License. A copy of
    the License is located at

    http://aws.amazon.com/apache2.0/

    or in the "license" file accompanying this file. This file is
    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
    ANY KIND, either express or implied. See the License for the specific
    language governing permissions and limitations under the License.

    === botocore configloader notice end
    """
    import copy
    import shlex

    parsed_config = copy.deepcopy(parsed_ini_config)
    profiles = {}
    services = {}
    sso_sessions = {}
    final_config = {}
    for key, values in parsed_config.items():
        if key.startswith("profile"):
            try:
                parts = shlex.split(key)
            except ValueError:
                continue
            if len(parts) == 2:
                profiles[parts[1]] = values
        if key.startswith("services"):
            try:
                parts = shlex.split(key)
            except ValueError:
                continue
            if len(parts) == 2:
                services[parts[1]] = values
        elif key.startswith("sso-session"):
            try:
                parts = shlex.split(key)
            except ValueError:
                continue
            if len(parts) == 2:
                sso_sessions[parts[1]] = values
        elif key == "default":
            # default section is special and is considered a profile
            # name but we don't require you use 'profile "default"'
            # as a section.
            profiles[key] = values
        else:
            final_config[key] = values
    final_config["profiles"] = profiles
    final_config["services"] = services
    final_config["sso_sessions"] = sso_sessions
    return final_config


def proposed_endpoint_url_resolution() -> None:  # pragma: no cover
    """Set endpoint URL resolution order for botocore.session.Session to.

    1. the `endpoint_url` parameter provided to the client or resource
    2. service-specific environment variable
    3. global environment variable
    4. service-specific parameter from the shared configuration file
    5. global parameter from the shared configuration file
    6. fallback to methods provided by the botocore
    """
    custom_endpoint_url_resolution(
        read_service_env_var,
        read_global_env_var,
        read_service_config_file,
        read_global_config_file,
    )


def custom_endpoint_url_resolution(
    *ero: Callable[[S, str], str | None]
) -> None:
    """Set endpoint resolution order for botocore.session.Session.

    :ero: iterable of resolution methods
    """

    class Session(botocore.session.Session):
        def _resolve_endpoint_url(self, service_name):
            service_id = (
                self.get_service_model(service_name)
                .service_id.hyphenize()
                .replace("-", "_")
            )
            for resolution_method in iter(ero):
                endpoint_url = resolution_method(self, service_id)
                if endpoint_url:
                    return endpoint_url
            else:
                return None

        def create_client(
            self,
            service_name,
            region_name=None,
            api_version=None,
            use_ssl=True,
            verify=None,
            endpoint_url=None,
            aws_access_key_id=None,
            aws_secret_access_key=None,
            aws_session_token=None,
            config=None,
        ):
            if endpoint_url is None:
                endpoint_url = self._resolve_endpoint_url(service_name)
            return super().create_client(
                service_name,
                region_name,
                api_version,
                use_ssl,
                verify,
                endpoint_url,
                aws_access_key_id,
                aws_secret_access_key,
                aws_session_token,
                config,
            )

    _patch_botocore(session_cls=Session)
    _refresh_boto3_default_session()


def _patch_botocore(session_cls):
    global BOTOCORE_PATCHED

    if BOTOCORE_PATCHED != {}:
        raise RuntimeError(
            f"BOTOCORE_PATCHED already populated by: {BOTOCORE_PATCHED}"
        )

    BOTOCORE_PATCHED["Session"] = botocore.session.Session
    BOTOCORE_PATCHED[
        "build_profile_map"
    ] = botocore.configloader.build_profile_map

    botocore.session.Session = session_cls
    botocore.configloader.build_profile_map = _custom_build_profile_map


def _unpatch_botocore():  # pragma: no cover
    global BOTOCORE_PATCHED

    try:
        botocore.session.Session = BOTOCORE_PATCHED["Session"]
        botocore.configloader.build_profile_map = BOTOCORE_PATCHED[
            "build_profile_map"
        ]
    except KeyError:
        raise RuntimeError(
            f"BOTOCORE_PATCHED is not populated: {BOTOCORE_PATCHED}"
        )

    BOTOCORE_PATCHED = {}


def _refresh_boto3_default_session():
    if boto3.DEFAULT_SESSION is not None:
        boto3.setup_default_session()
