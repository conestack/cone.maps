from cone.app import testing
from cone.tile.tests import TileTestCase
import sys
import unittest


class MapsLayer(testing.Security):

    def make_app(self, **kw):
        super(MapsLayer, self).make_app(**{
            'cone.plugins': 'cone.maps'
        })


class TestMapsTile(TileTestCase):
    layer = MapsLayer()

    def test_stub(self):
        self.assertTrue(True)


def run_tests():
    from cone.maps import tests
    from zope.testrunner.runner import Runner

    suite = unittest.TestSuite()
    suite.addTest(unittest.findTestCases(tests))

    runner = Runner(found_suites=[suite])
    runner.run()
    sys.exit(int(runner.failed))


if __name__ == '__main__':
    run_tests()
