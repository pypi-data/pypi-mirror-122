"""Parameter Store Loader
Use (setting_name, cast function) or setting_name as lookup value.
If no cast function is passed, the parameter will be stored as retrieved
from Parameter Store, typically string or stringList.

Usage:
from awstanding.parameter_store import load_parameters

LOOKUP_DICT = {
    '/my/parameter/path': 'NEW_VARIABLE'
}

load_parameters(LOOKUP_DICT)

# Now NEW_VARIABLE can be obtained from environment variables.

"""
import os
from collections.abc import Iterable
from typing import TypeVar, Union

import boto3

from .exceptions import ParameterNotFoundException

_ssm_client = boto3.client(service_name='ssm')


def load_parameters(lookup_dict: dict, allow_invalid=True) -> dict:
    """
    Loads each parameter defined in the lookup_dict as env. variables.
    The lookup_dict should look like this:
    {
        '/path/to/parameter1': 'PARAMETER_AS_ENV_VAR_1',
        '/path/to/parameter2': 'PARAMETER_AS_ENV_VAR_2',
        ...
        '/path/to/parameterN': 'PARAMETER_AS_ENV_VAR_N',
    }
    The values (Env. variables names) could be anything you want.
    It returns the loaded parameters for debugging purposes
    """
    paginated_keys = (list(lookup_dict.keys())[i:i+10] for i in range(0, len(lookup_dict), 10))

    parameters_ps = []
    invalid_parameters = []
    for keys in paginated_keys:
        parameters_page = _ssm_client.get_parameters(Names=keys, WithDecryption=True)
        parameters_ps += parameters_page['Parameters']
        invalid_parameters += parameters_page['InvalidParameters']

    if invalid_parameters and not allow_invalid:
        raise ParameterNotFoundException(invalid_parameters)

    parameters_ps = {param['Name']: param['Value'] for param in parameters_ps}

    # Override configuration for requested keys
    for key in parameters_ps:
        if isinstance(lookup_dict[key], (tuple, list)):
            setting_name, cast = lookup_dict[key]
            os.environ[setting_name] = cast(parameters_ps[key])
        elif isinstance(lookup_dict[key], str):
            os.environ[lookup_dict[key]] = parameters_ps[key]

    return parameters_ps


def load_path(*paths: Union[Iterable[str], str]) -> dict:
    """
    Loads each parameter behind `paths` recursively as env. variables.
    It returns the loaded parameters for debugging purposes
    """
    all_parameters = {}
    for path in paths:
        parameters_page = _ssm_client.get_parameters_by_path(Path=path, Recursive=True)
        parameters_ps = parameters_page['Parameters']

        while parameters_page.get('NextToken'):
            parameters_page = _ssm_client.get_parameters_by_path(Path=path, Recursive=True, NextToken=parameters_page.get('NextToken'))
            parameters_ps += parameters_page['Parameters']

        parameters_ps = {param['Name']: param['Value'] for param in parameters_ps}
        all_parameters.update(**parameters_ps)

        # Override configuration for requested keys
        for key in parameters_ps:
            os.environ[key.strip('/')
                .replace('/', '_')
                .replace('-', '_')
                .upper()
            ] = parameters_ps[key]

    return all_parameters
