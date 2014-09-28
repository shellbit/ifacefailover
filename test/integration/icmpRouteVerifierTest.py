import unittest

from verifier.icmpRouteVerifier import IcmpRouteVerifier


class IcmpRouteVerifierTest(unittest.TestCase):
    def testIsRouteAvailable(self):
        self.assertTrue(IcmpRouteVerifier().isRouteAvailable('8.8.8.8'))