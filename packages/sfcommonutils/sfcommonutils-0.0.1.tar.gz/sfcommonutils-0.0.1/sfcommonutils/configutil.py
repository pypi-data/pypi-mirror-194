import rdsutils.vendor.dynamic_yaml as dynamic_yaml
from mergedict import ConfigDict


def load_app_config(config_file_path: str, environment: str = '', include_defaults=True):
    print("hello")
    """
    Loads a yaml-based application configuration.
    The structure is expected to be one section for each environment for your app, with an optional 'defaults' section:

    defaults:
        thing1:
            property1: one
            property2: two
        thing2:
            property1: one

    dev:
        thing1:
            property2: something_else

    beta:
        thing1:
            property2: something_else_also


    If you supply an environment name, it will grab the sub-config for that environment.
    If include_defaults is True (the default) it will merge the environment specific config over top of the defaults (if they exist).

    The returned config object is a dynamic_yaml object, which includes support for string interpolation as described here:
    https://github.com/childsish/dynamic-yaml

    :param config_file_path: The path to a yaml file
    :param environment: An optional environment name to only return config for a specific environment
    :param include_defaults: Whether or not to layer the environment specific section on top of the defaults section
    :return: A dynamic_yaml dict containing the configuration
    """
    with open(config_file_path) as f:
        full_config = dynamic_yaml.load(stream=f)
        if not environment:
            return full_config

        defaults = full_config['defaults'] if include_defaults and 'defaults' in full_config else {}
        env = full_config[environment]
        app_config = ConfigDict(defaults)
        app_config.merge(env)
        return app_config
