# argandenvparse

v0.0.1

[![Build Status](https://travis-ci.org/bnbalsamo/argandenvparse.svg?branch=master)](https://travis-ci.org/bnbalsamo/argandenvparse) [![Coverage Status](https://coveralls.io/repos/github/bnbalsamo/argandenvparse/badge.svg?branch=master)](https://coveralls.io/github/bnbalsamo/argandenvparse?branch=master)

A patch for argparse which gives the ArgumentParser class the ability to parse environmental variables as well

Adds the ```.parse_args_and_env()``` which operates exactly the same as ```argparse.ArgumentParser.parse_args()``` except for the inclusion of one positional argument, a prefix to look for in the environmental variables.

If an environmental variable in all caps beginning with that prefix is found, the environmental variable name after the prefix (in all lowercase) is used as the key, and the value of the environmental variable as the value for the resulting args Namespace.

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
