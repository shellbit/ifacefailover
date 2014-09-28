import binascii, unittest

from verifier.icmpRouteVerifier import IcmpRouteVerifier


class IcmpRouteVerifierTest(unittest.TestCase):
    def testCreateIcmpRequestPacket(self):
        self.assertEquals('08004bc1a52c0100202122232425262728292a2b2c2d2e2f3031323334353637', binascii.hexlify(IcmpRouteVerifier().createIcmpRequestPacket(11429)))