"""
argandenvparse
"""

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.0.1"


from os import environ
from argparse import *


def parse_args_and_env(self, env_prefix, args=None, namespace=None,
                       enable_positional=True):

    env_args = {}
    for x in environ:
        if x.startswith(env_prefix.upper()) and x.upper() == x:
            env_args[x[len(env_prefix):]] = environ[x]

    # Take a look at what the parser is looking for,
    # gathering up relevant information and dropping
    # it into a list of hook dictionaries
    parser_hooks = []
    for flag in self._actions:
        parser_hook_dict = {}
        # Valid bits after the env prefix include all
        # of the optstrs in all caps, or the dest in all caps
        parser_hook_dict['hooks'] = [x.lstrip("-").upper() for x in flag.option_strings]
        parser_hook_dict['hooks'].append(flag.dest.upper())
        if len(flag.option_strings) > 0:
            parser_hook_dict['optstr'] = flag.option_strings[0]
        else:
            parser_hook_dict['optstr'] = None
        parser_hooks.append(parser_hook_dict)

    # Build an extraplated argument list from our
    # environmental variables, leveraging the information
    # we gathered in the hooks
    env_arg_list = []
    for envarg in env_args:
        found_in_parser = False
        for hook in parser_hooks:
            if envarg in hook['hooks']:
                found_in_parser = True
                if hook['optstr']:
                    env_arg_list.append(hook['optstr'])
                else:
                    if not enable_positional:
                        self.error(
                            "Can't consume positional arguments from " +
                            "the enviromation: {}".format(envarg)
                        )
                env_arg_list.append(env_args[envarg])
        if not found_in_parser:
            self.error(
                "Unrecognized environmental argument: {}".format(
                    envarg
                )
            )

    if args:
        env_arg_list = env_arg_list + args

    parsed = self.parse_args(args=env_arg_list, namespace=namespace)

    return parsed


ArgumentParser.parse_args_and_env = parse_args_and_env
