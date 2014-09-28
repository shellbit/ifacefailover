import property, os, unittest


class PropertyTest(unittest.TestCase):
    def testLoadPropertiesWithInvalidFile(self):
        self.assertRaises(Exception, property.loadProperties, 'doesnotexist.properties')
    
    def testLoadProperties(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../resources/ifacefailover-test.properties')
        properties = property.loadProperties(filename)
        self.assertEqual(properties['route.primary.gateway'], '192.168.1.1')
