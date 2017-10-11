"""
argandenvparse
"""

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.0.1"


from argparse import *

def parse_args_and_env(self, env_prefix, args=None, namespace=None):
    from os import environ

    if namespace is None:
        namespace = Namespace()

    for x in environ:
        if x.startswith(env_prefix.upper()):
            setattr(namespace, x[len(env_prefix):].lower(), environ[x])

    args = self.parse_args(args=args, namespace=namespace)

    return args

ArgumentParser.parse_env_and_args = parse_env_and_args
