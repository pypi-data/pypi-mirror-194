#!/usr/bin/env python3

from subprocess import Popen, PIPE
from typing import Optional, List, Dict
from tempfile import NamedTemporaryFile
import enum
import json


class CreateSealedSecretError(Exception):
    pass


class UpdateSealedSecretError(Exception):
    pass


class GetSealedSecretError(Exception):
    pass


class ListSealedSecretError(Exception):
    pass


class OutputFormat(str, enum.Enum):
    json = "json"
    yaml = "yaml"


def create(
    name: str,
    key: str,
    value: str,
    namespace: str = "default",
    merge_into: Optional[str] = None,
    output_format: OutputFormat = OutputFormat.json,
) -> str:
    """
    Returns an unapplied SealedSecret as a JSON or YAML string. If `merge_into` is provided,
    returns a path to a SealedSecret file in JSON or YAML format.
    """
    proc = Popen(
        [
            "kubectl",
            "-n",
            namespace,
            "create",
            "secret",
            "generic",
            name,
            "--dry-run=client",
            f"--from-file={key}=/dev/stdin",
            "-o",
            output_format,
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = proc.communicate(input=value.encode())
    if proc.returncode != 0:
        raise CreateSealedSecretError(stderr.decode())

    kubeseal = ["kubeseal", "-o", output_format]
    if merge_into:
        kubeseal.append("--merge-into")
        kubeseal.append(merge_into)

    proc2 = Popen(kubeseal, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout2, stderr2 = proc2.communicate(input=stdout)
    if proc2.returncode != 0:
        raise CreateSealedSecretError(stderr2.decode())

    # NB: this only generates the JSON, it still has to be commited to the repo and applied
    return stdout2.decode()


def update(
    name: str,
    key: str,
    value: str,
    namespace: str = "default",
    output_format: OutputFormat = OutputFormat.yaml,
):
    """
    Returns an unapplied SealedSecret matching name, as a JSON string. The updated
    secret is first retrieved from the k8s cluster by name. A SealedSecret matching
    key and value is then updated or added to the existing SealedSecret.
    """
    sealed_secret_str = get(name, namespace=namespace, output_format=output_format)
    with NamedTemporaryFile("w+") as tmpfile:
        tmpfile.write(sealed_secret_str)
        tmpfile.flush()
        create(
            name,
            key,
            value,
            namespace=namespace,
            merge_into=tmpfile.name,
            output_format=output_format,
        )
        tmpfile.seek(0)
        return tmpfile.read()


def _list(
    namespace: str = "default", output_format: OutputFormat = OutputFormat.json
) -> str:
    """
    Returns a JSON string of all SealedSecrets in namespace
    """
    proc = Popen(
        ["kubectl", "-n", namespace, "get", "sealedsecret", "-o", output_format],
        stdout=PIPE,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise ListSealedSecretError(stderr.decode())

    return stdout.decode()


def list_names(namespace: str = "default") -> Dict[str, List[str]]:
    """
    Returns a dictionary of SealedSecrets in namepsace, keyed by name, associated
    with a list of sub-key names
    """
    secrets = json.loads(_list(namespace, OutputFormat.json))
    return {
        s["metadata"]["name"]: list(s["spec"]["encryptedData"].keys())
        for s in secrets["items"]
    }


def get(
    name: str,
    namespace: str = "default",
    output_format: OutputFormat = OutputFormat.yaml,
) -> str:
    """
    Returns a SealedSecret matching name, as a JSON string
    """
    proc = Popen(
        ["kubectl", "-n", namespace, "get", "sealedsecret", name, "-o", output_format],
        stdout=PIPE,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise GetSealedSecretError(stderr.decode())

    return stdout.decode()
