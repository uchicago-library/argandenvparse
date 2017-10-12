import unittest
from os import environ
import argandenvparse


class Tests(unittest.TestCase):
    def setUp(self):
        # Perform any setup that should occur
        # before every test
        pass

    def tearDown(self):
        # Perform any tear down that should
        # occur after every test
        pass

    def testPass(self):
        self.assertEqual(True, True)

    def testVersionAvailable(self):
        x = getattr(argandenvparse, "__version__", None)
        self.assertTrue(x is not None)

    def testGetArg(self):
        environ['TEST_FOO'] = 'bar'
        parser = argandenvparse.ArgumentParser()
        parser.add_argument("--foo")
        args = parser.parse_args_and_env('TEST_')
        self.assertEqual(args.foo, 'bar')

    def testClobber(self):
        environ['TEST_FOO'] = 'bar'
        parser = argandenvparse.ArgumentParser()
        parser.add_argument("--foo")
        args = parser.parse_args_and_env('TEST_', args=['--foo', 'baz'])
        self.assertEqual(args.foo, 'baz')

    def testTypeCasting(self):
        environ['TEST_FOO'] = '1'
        parser = argandenvparse.ArgumentParser()
        parser.add_argument("--foo", type=int)
        args = parser.parse_args_and_env('TEST_')
        self.assertEqual(args.foo, 1)

    def testPositional(self):
        environ['TEST_FOO'] = 'bar'
        parser = argandenvparse.ArgumentParser()
        parser.add_argument("foo")
        args = parser.parse_args_and_env('TEST_')
        self.assertEqual(args.foo, 'bar')

    def testMixture(self):
        environ['TEST_FOO'] = 'bar'
        parser = argandenvparse.ArgumentParser()
        parser.add_argument("--foo")
        parser.add_argument("--monty")
        args = parser.parse_args_and_env('TEST_', args=['--monty', 'python'])
        self.assertEqual(args.foo, 'bar')
        self.assertEqual(args.monty, 'python')

    def testUnrecognized(self):
        class TestError(Exception):
            def __init__(self, message):
                self.message = message

        def error(message):
            raise TestError(message)

        environ['TEST_FOO'] = 'bar'
        parser = argandenvparse.ArgumentParser()
        parser.error = error
        # We have to catch the exception here and use
        # isinstance because of some weirdness with
        # hot-patching the parser object, I think
        try:
            parser.parse_args_and_env('TEST_')
        except Exception as e:
            self.assertTrue(
                isinstance(e, TestError)
            )
            self.assertTrue(
                e.message.startswith("Unrecognized")
            )

    def testNoPositional(self):
        class TestError(Exception):
            def __init__(self, message):
                self.message = message

        def error(message):
            raise TestError(message)

        environ['TEST_FOO'] = 'bar'
        parser = argandenvparse.ArgumentParser()
        parser.error = error
        parser.add_argument('foo')
        try:
            parser.parse_args_and_env('TEST_', enable_positional=False)
        except Exception as e:
            self.assertTrue(
                isinstance(e, TestError)
            )
            print(e.message)
            self.assertTrue(
                e.message.startswith("Can't consume positional")
            )


if __name__ == "__main__":
    unittest.main()
