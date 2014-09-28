from mock import call, patch, MagicMock

from route import Route
import service.routeService, unittest


class RouteServiceTest(unittest.TestCase):
    def setUp(self):
        self.actualRoutes = ({'dest': '0.0.0.0', 'netmask': '0.0.0.0', 'gateway': '192.168.1.1', 'dev': 'wlan0'}
                       , {'dest': '192.168.1.0', 'netmask': '255.255.255.0', 'gateway': '0.0.0.0', 'dev': 'wlan0'})
        self.defaultRoute = Route('0.0.0.0', '192.168.1.1', '0.0.0.0', 'wlan0')
        self.staticRoute = Route('192.168.1.0', '0.0.0.0', '255.255.255.0', 'wlan0')
        self.expectedRoutes = [self.defaultRoute, self.staticRoute]
        
    @patch('service.routeService.netinfo.get_routes')
    def testGetRoutes(self, mockGetRoutes):
        mockGetRoutes.return_value = self.actualRoutes
        assert self.expectedRoutes == service.routeService.getRoutes()
    
    def testGetRoute(self):
        service.routeService.getRoutes = MagicMock(return_value=self.expectedRoutes)
        assert self.defaultRoute == service.routeService.getRoute('0.0.0.0')
    
    def testGetRouteWhenRouteDoesNotExist(self):
        service.routeService.getRoutes = MagicMock(return_value=self.expectedRoutes)
        assert None == service.routeService.getRoute('1.1.1.1')
    
    @patch('service.routeService.logging.error')
    @patch('service.routeService.netinfo.add_route')
    def testAddRouteWasSuccessful(self, mockAddRoute, mockErrorLogger):
        mockAddRoute.return_value = None
        service.routeService.addRoute(self.staticRoute)
        assert 1 == mockAddRoute.call_count
        assert 0 == mockErrorLogger.call_count
    
    @patch('service.routeService.logging.error')
    @patch('service.routeService.netinfo.add_route')
    def testAddRouteWasNotSuccessful(self, mockAddRoute, mockErrorLogger):
        mockAddRoute.return_value = 'Route already exists'
        service.routeService.addRoute(self.defaultRoute)
        assert 1 == mockAddRoute.call_count
        mockErrorLogger.assert_called_once_with('Route already exists')
    
    @patch('service.routeService.logging.error')
    @patch('service.routeService.netinfo.del_route')
    def testDeleteRouteWasSuccessful(self, mockDeleteRoute, mockErrorLogger):
        mockDeleteRoute.return_value = None
        service.routeService.deleteRoute(self.staticRoute)
        assert 1 == mockDeleteRoute.call_count
        assert 0 == mockErrorLogger.call_count
    
    @patch('service.routeService.logging.error')
    @patch('service.routeService.netinfo.del_route')
    def testDeleteRouteWasNotSuccessful(self, mockDeleteRoute, mockErrorLogger):
        mockDeleteRoute.return_value = 'Route does not exist'
        service.routeService.deleteRoute(self.staticRoute)
        assert 1 == mockDeleteRoute.call_count
        mockErrorLogger.assert_called_once_with('Route does not exist')
    
    @patch('service.routeService.logging.error')
    def testValidateResponseWithSuccess(self, mockErrorLogger):
        service.routeService.validateResponse(None)
        assert 0 == mockErrorLogger.call_count
    
    @patch('service.routeService.logging.error')
    def testValidateResponseWithError(self, mockErrorLogger):
        service.routeService.validateResponse('ERROR')
        mockErrorLogger.assert_called_once_with('ERROR')