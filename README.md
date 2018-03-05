# argandenvparse

v0.0.1

[![Build Status](https://travis-ci.org/uchicago-library/argandenvparse.svg?branch=master)](https://travis-ci.org/uchicago-library/argandenvparse) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/argandenvparse/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/argandenvparse?branch=master)

A patch for argparse which gives the ArgumentParser class the ability to parse environmental variables as well

If an environmental variable in all caps beginning with a given prefix is found, the environmental variable name after the prefix (in all lowercase) is used as the key, and the value of the environmental variable as the value for the resulting args Namespace, assuming you have added an argument with either a ```dest``` or an option string that matches the content of the environmental variable after the prefix.

(For a demonstration of this functionality see the code snippet below.)

This is implemented in a new method: ```ArgumentParser.parse_args_and_env()```

This method works similarly to ```argparse.ArgumentParser.parse_args()``` with the following notable exceptions:

* One required position argument: a prefix to search for in environmental arguments, the value following the prefix in the environmental variable name will be used as the key in the resulting Namespace.
* Two new keyword arguments
    * ```enable_positional``` (True): Enable parsing positional arguments from the environment. 
        * *Note* that these are not clobbered by CLI input, but rather CLI input is appended as an additional positional argument
    * ```error_on_unrecognized_env_vars``` (True): Finding environmetal variables that contain the prefix but are not referenced in the parser will be silently ignored if this is set to false, otherwise behavior is exactly the same as passing unrecognized arguments on the CLI


```bash
$ EXAMPLE_FOO=bar python
>>> from argandenvparse import ArgumentParser
>>> parser = ArgumentParser()
>>> parser.add_argument('--foo')
>>> parser.parse_args_and_env('EXAMPLE_')
Namespace(foo='bar')
>>> parser.parse_args_and_env('EXAMPLE_', args=['--foo', 'baz'])
Namespace(foo='baz')
```

# Author
Brian Balsamo <brian@brianbalsamo.com>
