from mock import call, MagicMock
import unittest

from handler.logHandler import LogHandler
from route import Route, createRoutesFromProperties
from verifier.icmpRouteVerifier import IcmpRouteVerifier


class RouteTest(unittest.TestCase):
    def setUp(self):
        self.verifier = IcmpRouteVerifier()
        self.handlers = [LogHandler()]
        self.route = Route('0.0.0.0', '192.168.1.1', '0.0.0.0', 'eth0', ['8.8.8.8', '8.8.4.4'], 10, self.verifier, {'timeout':2, 'maxRetry':3}, self.handlers, [{}])
        
    def testGetTargetRoutes(self):
        targetRoutes = self.route.getTargetRoutes()
        assert 2 == len(targetRoutes)
        assert Route('8.8.8.8', '192.168.1.1', '255.255.255.255', 'eth0') == targetRoutes[0]
        assert Route('8.8.4.4', '192.168.1.1', '255.255.255.255', 'eth0') == targetRoutes[1]
    
    def testIsRouteIsAvailable(self):
        mockIsRouteAvailable = MagicMock()
        mockIsRouteAvailable.return_value = True
        self.verifier.isRouteAvailable = mockIsRouteAvailable
        
        assert self.route.isAvailable()
        assert 2 == mockIsRouteAvailable.call_count
        expected = [call('8.8.8.8', timeout=2, maxRetry=3,), call('8.8.4.4', timeout=2, maxRetry=3,)]
        assert expected == mockIsRouteAvailable.call_args_list
    
    def testRouteIsNotAvailable(self):
        mockIsRouteAvailable = MagicMock()
        mockIsRouteAvailable.return_value = False
        self.verifier.isRouteAvailable = mockIsRouteAvailable
        
        assert not self.route.isAvailable()
        assert 2 == mockIsRouteAvailable.call_count
        expected = [call('8.8.8.8', timeout=2, maxRetry=3,), call('8.8.4.4', timeout=2, maxRetry=3,)]
        assert expected == mockIsRouteAvailable.call_args_list
    
    def testOnSetup(self):
        mockOnSetup = MagicMock()
        self.route.handlers[0].onSetup = mockOnSetup
        self.route.onSetup()
        mockOnSetup.assert_called_once_with(**{})
    
    def testTearDown(self):
        mockTearDown = MagicMock()
        self.route.handlers[0].onTearDown = mockTearDown
        self.route.onTearDown()
        mockTearDown.assert_called_once_with(**{})
    
    def testOnConnectionFailed(self):
        mockOnConnectionFailed = MagicMock()
        self.route.handlers[0].onConnectionFailed = mockOnConnectionFailed
        self.route.onConnectionFailed()
        mockOnConnectionFailed.assert_called_once_with(**{})
    
    def testOnConnectionRestored(self):
        mockOnConnectionRestored = MagicMock()
        self.route.handlers[0].onConnectionRestored = mockOnConnectionRestored
        self.route.onConnectionRestored()
        mockOnConnectionRestored.assert_called_once_with(**{})
    
    def testOnConnected(self):
        mockOnConnected = MagicMock()
        self.route.handlers[0].onConnected = mockOnConnected
        self.route.onConnected()
        mockOnConnected.assert_called_once_with(**{})
    
    def testValidationExceptionWhenHandlerKwargsDoNotMatchHandlers(self):
        try:
            properties = {'route.primary.gateway':'192.168.1.1'
                      , 'route.primary.iface':'eth0'
                      , 'route.primary.handlers':'["../resources/logHandler.pkl","../resources/logHandler.pkl"]'
                      , 'route.primary.handlerKwargs':"[{}]"
                      }
            createRoutesFromProperties(properties)
            self.assertFail()
        except Exception as e:
            assert 'Handler and HandlerKwargs mismatch for route 0.0.0.0' == e.message
        
    def testCreateRoutesFromProperties(self):
        properties = {'route.primary.gateway':'192.168.1.1'
                      , 'route.primary.iface':'eth0'
                      , 'route.primary.targets':'8.8.8.8,8.8.4.4'
                      , 'route.primary.verifierDelay':'10'
                      , 'route.primary.verifier':'../resources/icmpRouteVerifier.pkl'
                      , 'route.primary.verifierKwargs':"{'timeout':1, 'maxRetry':2}"
                      , 'route.primary.handlers':'["../resources/logHandler.pkl","../resources/logHandler.pkl"]'
                      , 'route.primary.handlerKwargs':"[{},{}]"
                      , 'route.fona.gateway':'0.0.0.0'
                      , 'route.fona.iface':'ppp0'}
        
        routes = createRoutesFromProperties(properties)
        assert 2 == len(routes)
        
        primary = routes[0]
        assert '0.0.0.0' == primary.destination
        assert '192.168.1.1' == primary.gateway
        assert '0.0.0.0' == primary.genmask
        assert 'eth0' == primary.iface
        assert ['8.8.8.8', '8.8.4.4'] == primary.targets
        assert 10 == primary.verifierDelay
        assert IcmpRouteVerifier() == primary.verifier
        assert {'timeout':1, 'maxRetry':2} == primary.verifierKwargs
        assert [LogHandler(), LogHandler()] == primary.handlers
        assert [{},{}] == primary.handlerKwargs
        
        primaryTargetRoutes = primary.getTargetRoutes()
        assert 2 == len(primaryTargetRoutes)
        
        primaryTargetRoute1 = primaryTargetRoutes[0]
        assert '8.8.8.8' == primaryTargetRoute1.destination
        assert '192.168.1.1' == primaryTargetRoute1.gateway
        assert '255.255.255.255' == primaryTargetRoute1.genmask
        assert 'eth0' == primaryTargetRoute1.iface
        assert 0 == len(primaryTargetRoute1.targets)
        assert 0 == primaryTargetRoute1.verifierDelay
        assert None == primaryTargetRoute1.verifier
        assert {} == primaryTargetRoute1.verifierKwargs
        assert [] == primaryTargetRoute1.handlers
        assert [] == primaryTargetRoute1.handlerKwargs
        
        primaryTargetRoute2 = primaryTargetRoutes[1]
        assert '8.8.4.4' == primaryTargetRoute2.destination
        assert '192.168.1.1' == primaryTargetRoute2.gateway
        assert '255.255.255.255' == primaryTargetRoute2.genmask
        assert 'eth0' == primaryTargetRoute2.iface
        assert 0 == len(primaryTargetRoute2.targets)
        assert 0 == primaryTargetRoute2.verifierDelay
        assert None == primaryTargetRoute2.verifier
        assert {} == primaryTargetRoute2.verifierKwargs
        assert [] == primaryTargetRoute2.handlers
        assert [] == primaryTargetRoute2.handlerKwargs
        
        fona = routes[1]
        assert '0.0.0.0' == fona.destination
        assert '0.0.0.0' == fona.gateway
        assert '0.0.0.0' == fona.genmask
        assert 'ppp0' == fona.iface
        assert 0 == len(fona.targets)
        assert 0 == fona.verifierDelay
        assert None == fona.verifier
        assert {} == fona.verifierKwargs
        assert [] == fona.handlers
        assert [] == fona.handlerKwargs
        
