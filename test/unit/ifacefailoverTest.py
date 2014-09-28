from mock import call, patch, MagicMock

import ifacefailover, unittest
from route import Route


class IFaceFailoverTest(unittest.TestCase):
    def setUp(self):
        self.defaultRoute = Route('0.0.0.0', '192.168.1.1', '0.0.0.0', 'eth0', ['8.8.8.8', '8.8.4.4'], 10)
        self.failoverRoute = Route('0.0.0.0', '0.0.0.0', '0.0.0.0', 'ppp0')
        self.routes = [self.defaultRoute, self.failoverRoute]
        
    @patch('ifacefailover.createRoute')
    def testInitializeRoutes(self, mockCreateRoute):
        ifacefailover.initializeRoutes(self.routes)
        
        assert 3 == mockCreateRoute.call_count
        expected = [call(self.defaultRoute,), call(Route('8.8.8.8', '192.168.1.1', '255.255.255.255', 'eth0'),), call(Route('8.8.4.4', '192.168.1.1', '255.255.255.255', 'eth0'),)]
        assert expected == mockCreateRoute.call_args_list
    
    @patch('ifacefailover.addRoute')
    @patch('ifacefailover.deleteRoute')
    @patch('ifacefailover.getRoute')
    def testCreateRouteWithNonExistingRoute(self, mockGetRoute, mockDeleteRoute, mockAddRoute):
        mockGetRoute.return_value = None
        
        route = Route('0.0.0.0', '192.168.1.1', '0.0.0.0', 'eth0')
        ifacefailover.createRoute(route)
        
        mockGetRoute.assert_called_once_with('0.0.0.0')
        assert not mockDeleteRoute.called
        mockAddRoute.assert_called_once_with(route)

    @patch('ifacefailover.addRoute')
    @patch('ifacefailover.deleteRoute')
    @patch('ifacefailover.getRoute')
    def testCreateRouteWithExistingRoute(self, mockGetRoute, mockDeleteRoute, mockAddRoute):
        existingRoute = Route('0.0.0.0', '192.168.1.1', '0.0.0.0', 'eth0')
        mockGetRoute.return_value = existingRoute
        
        route = Route('0.0.0.0', '192.168.1.1', '0.0.0.0', 'eth0')
        ifacefailover.createRoute(route)
        
        mockGetRoute.assert_called_once_with('0.0.0.0')
        mockDeleteRoute.assert_called_once_with(existingRoute)
        mockAddRoute.assert_called_once_with(route)
    
    def testRecoverRoutesWithDefaultRouteIndex(self):
        assert (False, 0) == ifacefailover.recoverRoutes(self.routes, 0)
    
    def testRecoverRoutesWhenDownRouteIsAvailable(self):
        self.defaultRoute.isAvailable = MagicMock(return_value=True)
        assert (True, 0) == ifacefailover.recoverRoutes(self.routes, 1)
        
    def testRecoverRoutesWhenDownRouteIsNotAvailable(self):
        self.defaultRoute.isAvailable = MagicMock(return_value=False)
        assert (False, 1) == ifacefailover.recoverRoutes(self.routes, 1)
    
    def testVerifyRouteWithRouteContainingNoTargets(self):
        assert 1 == ifacefailover.verifyRoute(self.routes, 1)
    
    @patch('ifacefailover.sleep')
    def testVerifyRouteSleepsWhenRouteIsAvailable(self, mockSleep):
        self.defaultRoute.isAvailable = MagicMock(return_value=True)
        assert 0 == ifacefailover.verifyRoute(self.routes, 0)
        mockSleep.assert_called_once_with(10)
    
    @patch('ifacefailover.failoverToNextRoute')
    def testVerifyRouteFailoverWhenRouteIsUnavailable(self, mockFailoverToNextRoute):
        self.defaultRoute.isAvailable = MagicMock(return_value=False)
        mockFailoverToNextRoute.return_value = 1
        assert 1 == ifacefailover.verifyRoute(self.routes, 0)
        mockFailoverToNextRoute.assert_called_once_with(self.routes, 0)
    
    @patch('ifacefailover.sleep')
    @patch('ifacefailover.createRoute')
    def testRestoreFirstRoute(self, mockCreateRoute, mockSleep):
        mockOnTearDown = MagicMock()
        mockOnSetup = MagicMock()
        mockOnConnectionRestored = MagicMock()
        self.failoverRoute.onTearDown = mockOnTearDown
        self.defaultRoute.onSetup = mockOnSetup
        self.defaultRoute.onConnectionRestored = mockOnConnectionRestored
        
        ifacefailover.restoreRoute(self.routes, 0)
        mockOnTearDown.assert_any_call()
        mockOnSetup.assert_any_call()
        mockOnConnectionRestored.assert_any_call()
        mockCreateRoute.assert_called_once_with(self.defaultRoute)
        mockSleep.assert_called_once_with(10)
    
    @patch('ifacefailover.sleep')
    @patch('ifacefailover.createRoute')
    def testRestoreSecondRoute(self, mockCreateRoute, mockSleep):
        mockOnTearDown = MagicMock()
        mockOnSetup = MagicMock()
        mockOnConnectionRestored = MagicMock()
        self.defaultRoute.onTearDown = mockOnTearDown
        self.failoverRoute.onSetup = mockOnSetup
        self.failoverRoute.onConnectionRestored = mockOnConnectionRestored
        
        ifacefailover.restoreRoute(self.routes, 1)
        mockOnTearDown.assert_any_call()
        mockOnSetup.assert_any_call()
        mockOnConnectionRestored.assert_any_call()
        mockCreateRoute.assert_called_once_with(self.failoverRoute)
        mockSleep.assert_called_once_with(0)
    
    @patch('ifacefailover.createRoute')
    def testFailoverToNextRoute(self, mockCreateRoute):
        mockOnTearDown = MagicMock()
        mockOnSetup = MagicMock()
        mockOnConnectionFailed = MagicMock()
        mockOnConnected = MagicMock()
        self.defaultRoute.onTearDown = mockOnTearDown
        self.failoverRoute.onSetup = mockOnSetup
        self.defaultRoute.onConnectionFailed = mockOnConnectionFailed
        self.failoverRoute.onConnected = mockOnConnected
        
        assert 1 == ifacefailover.failoverToNextRoute(self.routes, 0)
        mockCreateRoute.assert_called_once_with(self.failoverRoute)
        mockOnTearDown.assert_any_call()
        mockOnSetup.assert_any_call()
        mockOnConnectionFailed.assert_any_call()
        mockOnConnected.assert_any_call()
    
    @patch('ifacefailover.createRoute')
    def testFailoverToFirstRouteWhenIndexIsLastRoute(self, mockCreateRoute):
        mockOnTearDown = MagicMock()
        mockOnSetup = MagicMock()
        mockOnConnectionFailed = MagicMock()
        mockOnConnected = MagicMock()
        self.failoverRoute.onTearDown = mockOnTearDown
        self.defaultRoute.onSetup = mockOnSetup
        self.failoverRoute.onConnectionFailed = mockOnConnectionFailed
        self.defaultRoute.onConnected = mockOnConnected
        
        assert 0 == ifacefailover.failoverToNextRoute(self.routes, 1)
        mockCreateRoute.assert_called_once_with(self.defaultRoute)
        mockOnTearDown.assert_any_call()
        mockOnSetup.assert_any_call()
        mockOnConnectionFailed.assert_any_call()
        mockOnConnected.assert_any_call()
