import json
from importlib import import_module
from typing import Any, Dict, Optional
import glob
import graphql
from turms.errors import GenerationError

from graphql import (
    build_ast_schema,
    build_client_schema,
    get_introspection_query,
    parse,
)


def import_class(module_path, class_name):
    """Import a module from a module_path and return the class"""
    module = import_module(module_path)
    return getattr(module, class_name)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed. Simliar to
    djangos import_string, but without the cache.
    """

    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    try:
        return import_class(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            f"{module_path} does not define a {class_name} attribute/class"
        ) from err


def introspect_url(
    schema_url: str, bearer_token: Optional[str] = None
) -> Dict[str, Any]:
    """Introspect a GraphQL schema using introspection query

    Args:
        schema_url (str): The Schema url
        bearer_token (str, optional): A Bearer token. Defaults to None.

    Raises:
        GenerationError: An error occurred while generating the schema.

    Returns:
        dict: The introspection query response.
    """
    try:  # pragma: no cover
        import requests  # pragma: no cover
    except ImportError:  # pragma: no cover
        raise GenerationError(
            "The requests library is required to introspect a schema from a url"
        )  # pragma: no cover

    jdata = json.dumps({"query": get_introspection_query()}).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    try:
        req = requests.post(schema_url, data=jdata, headers=headers)
        x = req.json()
    except Exception as e:
        raise GenerationError(f"Failed to fetch schema from {schema_url}")
    if "errors" in x:  # pragma: no cover
        raise GenerationError(
            f"Failed to fetch schema from {schema_url} Graphql error: {x['errors']}"
        )
    return x["data"]


def build_schema_from_introspect_url(
    schema_url: str, bearer_token: Optional[str] = None
) -> graphql.GraphQLSchema:
    """Introspect a GraphQL schema using introspection query

    Args:
        schema_url (str): The Schema url
        bearer_token (str, optional): A Bearer token. Defaults to None.

    Raises:
        GenerationError: An error occurred while generating the schema.

    Returns:
        graphql.GraphQLSchema: The parsed GraphQL schema.
    """
    x = introspect_url(schema_url, bearer_token)

    return build_client_schema(x)


def build_schema_from_glob(glob_string: str):
    """Build a GraphQL schema from a glob string"""
    schema_glob = glob.glob(glob_string, recursive=True)
    dsl_string = ""
    introspection_string = ""
    for file in schema_glob:
        with open(file, "rb") as f:
            decoded_file = f.read().decode("utf-8-sig")
            if file.endswith(".graphql"):
                dsl_string += decoded_file
            elif file.endswith(".json"):
                # not really necessary as json files are generally not splitable
                introspection_string += decoded_file

    if not dsl_string and not introspection_string:
        raise GenerationError(f"No schema files found in {glob_string}")

    if dsl_string != "" and introspection_string != "":  # pragma: no cover
        raise GenerationError("We cannot have both dsl and introspection files")
    if dsl_string != "":
        return build_ast_schema(parse(dsl_string))
    else:
        return build_client_schema(json.loads(introspection_string))
