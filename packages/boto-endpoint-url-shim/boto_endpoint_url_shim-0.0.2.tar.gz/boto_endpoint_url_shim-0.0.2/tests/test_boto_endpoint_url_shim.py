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

import importlib
import tempfile

import boto3
import botocore
import pytest

import boto_endpoint_url_shim

SERVICE = "elasticbeanstalk"
SERVICE_ID = "elastic_beanstalk"
ENDPOINT_URL = "http://localhost:8123"


@pytest.fixture(autouse=True)
def aws_region(monkeypatch):
    region = "eu-west-1"
    monkeypatch.setenv("AWS_DEFAULT_REGION", region)
    return region


@pytest.fixture(autouse=True)
def reset_shim():
    importlib.reload(boto_endpoint_url_shim)
    importlib.reload(botocore)
    importlib.reload(boto3)


@pytest.fixture
def make_config_file(monkeypatch):
    def _make_config_file(content):
        with tempfile.NamedTemporaryFile(mode="wt", delete=False) as f_config:
            f_config.write(content)
            f_config.seek(0)
            monkeypatch.setenv("AWS_CONFIG_FILE", f_config.name)

    return _make_config_file


def test_endpoint_kwarg():
    boto_endpoint_url_shim.custom_endpoint_url_resolution()

    session = botocore.session.Session()
    client = session.create_client(
        SERVICE,
        endpoint_url=ENDPOINT_URL,
    )
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_endpoint_fallback(aws_region):
    boto_endpoint_url_shim.custom_endpoint_url_resolution()

    session = botocore.session.Session()
    client = session.create_client(SERVICE)
    assert (
        client.meta.endpoint_url
        == f"https://{SERVICE}.{aws_region}.amazonaws.com"
    )


def test_read_service_env_var(monkeypatch):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_service_env_var
    )

    monkeypatch.setenv(
        boto_endpoint_url_shim.SERVICE_ENV_VAR.format(SERVICE_ID.upper()),
        ENDPOINT_URL,
    )

    session = botocore.session.Session()
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_read_global_env_var(monkeypatch):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_global_env_var
    )

    monkeypatch.setenv(boto_endpoint_url_shim.GLOBAL_ENV_VAR, ENDPOINT_URL)

    session = botocore.session.Session()
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_read_service_config_file_profile(make_config_file):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_service_config_file
    )

    make_config_file(
        "\n".join(
            [
                "[services local-srv]",
                f"{SERVICE_ID} =",
                f"    endpoint_url = {ENDPOINT_URL}",
                "[profile local]",
                "services = local-srv",
            ]
        )
    )

    session = botocore.session.Session(profile="local")
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_read_service_config_file_profile_KeyError(
    make_config_file,
    aws_region,
):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_service_config_file
    )

    make_config_file(
        "\n".join(
            [
                "[services local-srv]",
                f"{SERVICE_ID} =",
                f"    endpoint_url = {ENDPOINT_URL}",
                "[profile local]",
            ]
        )
    )

    session = botocore.session.Session(profile="local")
    client = session.create_client(SERVICE)
    assert (
        client.meta.endpoint_url
        == f"https://{SERVICE}.{aws_region}.amazonaws.com"
    )


def test_read_global_config_file_profile(make_config_file):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_global_config_file
    )

    make_config_file(
        "\n".join(
            [
                "[services local-srv]",
                f"endpoint_url = {ENDPOINT_URL}",
                "[profile local]",
                "services = local-srv",
            ]
        )
    )

    session = botocore.session.Session(profile="local")
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_read_mapping_env_var(monkeypatch, mocker):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_mapping_env_var
    )

    mapping = f"{SERVICE_ID}={ENDPOINT_URL}"

    monkeypatch.setenv(boto_endpoint_url_shim.GLOBAL_ENV_VAR, mapping)

    spy = mocker.spy(boto_endpoint_url_shim, "_parse_mapping")

    session = botocore.session.Session()
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL
    spy.assert_called_once_with(mapping)
    spy.spy_exception = None


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_read_mapping_env_var_unset_raises_RuntimeWarning(mocker, aws_region):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_mapping_env_var
    )

    spy = mocker.spy(boto_endpoint_url_shim, "_parse_mapping")

    session = botocore.session.Session()
    with pytest.warns(RuntimeWarning):
        client = session.create_client(SERVICE)
    assert (
        client.meta.endpoint_url
        == f"https://{SERVICE}.{aws_region}.amazonaws.com"
    )
    spy.assert_called_once_with(None)
    spy.spy_exception = None


def test_read_named_top_level_config_file_default(make_config_file):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_named_top_level_config_file
    )

    make_config_file(
        f"[default]\n{SERVICE_ID}_endpoint_url = {ENDPOINT_URL}\n"
    )

    session = botocore.session.Session()
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_read_named_top_level_config_file_profile(make_config_file):
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        boto_endpoint_url_shim.read_named_top_level_config_file
    )

    make_config_file(
        f"[profile local]\n{SERVICE_ID}_endpoint_url = {ENDPOINT_URL}\n"
    )

    session = botocore.session.Session(profile="local")
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_read_custom_resolution_method():
    boto_endpoint_url_shim.custom_endpoint_url_resolution(
        lambda *_: ENDPOINT_URL
    )

    session = botocore.session.Session()
    client = session.create_client(SERVICE)
    assert client.meta.endpoint_url == ENDPOINT_URL


def test_patch_already_patched_raises_RuntimeError():
    boto_endpoint_url_shim.custom_endpoint_url_resolution()

    with pytest.raises(RuntimeError):
        boto_endpoint_url_shim.custom_endpoint_url_resolution()


def test_patch_resets_boto3_default_session():
    boto3.setup_default_session()
    session_unpatched = boto3.DEFAULT_SESSION

    boto_endpoint_url_shim.custom_endpoint_url_resolution()
    session_patched = boto3.DEFAULT_SESSION

    assert session_patched is not session_unpatched
