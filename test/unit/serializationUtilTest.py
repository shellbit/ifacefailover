import filecmp, unittest, os

from serializationUtil import serialize, deserialize
from verifier.icmpRouteVerifier import IcmpRouteVerifier


class SerializationUtilTest(unittest.TestCase):
    def setUp(self):
        self.expectedFile = os.path.join(os.path.dirname(__file__), '../resources/icmpRouteVerifier.pkl')
        self.actualFile = os.path.join(os.path.dirname(__file__), '../resources/icmpRouteVerifierTest.pkl')
        
    def testSerialize(self):
        assert os.path.isfile(self.expectedFile)
        assert not os.path.isfile(self.actualFile)
        
        serialize(IcmpRouteVerifier(), self.actualFile)
        assert os.path.isfile(self.actualFile)
        assert filecmp.cmp(self.expectedFile, self.actualFile)
        
        os.remove(self.actualFile)
        assert not os.path.isfile(self.actualFile)
    
    def testDeserialize(self):
        assert os.path.isfile(self.expectedFile)
        assert IcmpRouteVerifier() == deserialize(self.expectedFile)
