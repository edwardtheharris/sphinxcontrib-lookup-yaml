import unittest
import warnings

from sphinx_testing import with_app

from sphinxcontrib.lookup_yaml import LookupYAMLError


def build(app, path):
    '''Build and return documents without known warnings.'''
    warnings.filterwarnings(
            'ignore',
            '\'U\' mode is deprecated',
            DeprecationWarning)
    app.build()
    return (app.outdir / path).read_text()


class TestLookupYAML(unittest.TestCase):

    @with_app(
            buildername='text',
            srcdir='tests/examples/good_lookup',
            copy_srcdir_to_tmpdir=True)
    def test_good_lookup(self, app, status, warning):
        '''Ensure, that good lookups don't throw exceptions.'''
        output = build(app, 'index.txt')
        with open('tests/examples/good_lookup/index.txt') as f:
            correct = f.read()
        self.assertEqual(correct, output)

    @with_app(
            buildername='text',
            srcdir='tests/examples/nonexisting',
            copy_srcdir_to_tmpdir=True)
    def test_nonexisting(self, app, status, warning):
        '''Ensure, that nonexistent value will throw exception.'''
        try:
            build(app, 'index.txt')
        except Exception as e:
            ret = e
        self.assertIsInstance(ret, LookupYAMLError)
        self.assertIn('Value "test_value20" not found', str(ret))

    @with_app(
            buildername='text',
            srcdir='tests/examples/nonnumeric',
            copy_srcdir_to_tmpdir=True)
    def test_nonnumeric_index(self, app, status, warning):
        '''Ensure, that non-numeric indexes won't be accepted for lists.'''
        try:
            build(app, 'index.txt')
        except Exception as e:
            ret = e
        self.assertIsInstance(ret, LookupYAMLError)
        self.assertIn('Can\'t convert index in "test_value2 / number_one"',
                str(ret))

    @with_app(
            buildername='text',
            srcdir='tests/examples/invalid_file',
            copy_srcdir_to_tmpdir=True)
    def test_invalid_file(self, app, status, warning):
        '''Ensure, that exceptions is thrown on non-existing file.'''
        try:
            build(app, 'index.txt')
        except Exception as e:
            ret = e
        self.assertIsInstance(ret, LookupYAMLError)
        self.assertIn('is not a file', str(ret))
