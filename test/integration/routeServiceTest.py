from route import Route
import service.routeService, unittest


class RouteServiceTest(unittest.TestCase):
    def testGetRoutes(self):
        assert len(service.routeService.getRoutes()) > 0

    def testGetRoute(self):
        route = service.routeService.getRoute('0.0.0.0')
        assert '0.0.0.0' == route.destination
    
    def testAddRoute(self):
        assert None == service.routeService.getRoute('8.8.8.8')
        service.routeService.addRoute(Route('8.8.8.8', '192.168.1.1', '255.255.255.255', 'wlan0'))
        assert None != service.routeService.getRoute('8.8.8.8')
    
    def testDeleteRoute(self):
        assert None != service.routeService.getRoute('8.8.8.8')
        service.routeService.deleteRoute(Route('8.8.8.8', '192.168.1.1', '255.255.255.255', 'wlan0'))
        assert None == service.routeService.getRoute('8.8.8.8')