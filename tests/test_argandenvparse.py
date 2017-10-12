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
        try:
            del environ['TEST_FOO']
        except:
            pass
        try:
            del environ['TEST_THIS']
        except:
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
        with self.assertRaises(TestError) as cm:
            parser.parse_args_and_env('TEST_')
            self.assertTrue(
                cm.exception.message.startswith("Unrecognized")
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
        with self.assertRaises(TestError) as cm:
            parser.parse_args_and_env('TEST_', enable_positional=False)
            self.assertTrue(
                cm.exception.message.startswith("Can't consume positional")
            )

    def testNoErrorOnUnrecognizedEnvVar(self):
        environ['TEST_FOO'] = 'bar'
        environ['TEST_THIS'] = 'that'
        parser = argandenvparse.ArgumentParser()
        parser.add_argument("--foo")
        args = parser.parse_args_and_env('TEST_', error_on_unrecognized_env_vars=False)
        self.assertEqual(args.foo, 'bar')
        with self.assertRaises(AttributeError):
            args.this


if __name__ == "__main__":
    unittest.main()
