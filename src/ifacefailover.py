import logging.config, sys
from time import sleep

from property import loadProperties
from route import createRoutesFromProperties
from service.routeService import addRoute, deleteRoute, getRoute


def main(argv):
    properties = loadProperties(argv[0])
    logging.config.fileConfig(properties.get('log.properties'))
    routes = createRoutesFromProperties(properties)
    initializeRoutes(routes)
    
    routeIndex = 0
    while 1:
        routeRecovered, routeIndex = recoverRoutes(routes, routeIndex)
        if routeRecovered:
            restoreRoute(routes, routeIndex)
        else:
            routeIndex = verifyRoute(routes, routeIndex)

def initializeRoutes(routes):
    for index, route in enumerate(routes):
        if index == 0:
            createRoute(route)
        for targetRoute in route.getTargetRoutes():
            createRoute(targetRoute)
    
def createRoute(route):
    existingRoute = getRoute(route.destination)
    if existingRoute is not None:
        deleteRoute(existingRoute)
    addRoute(route)

def recoverRoutes(routes, routeIndex):
    for i in range(0, routeIndex):
        downRoute = routes[i]
        if downRoute.isAvailable():
            return True, i
    return False, routeIndex

def verifyRoute(routes, routeIndex):
    route = routes[routeIndex]
    if len(route.targets) > 0:
        if route.isAvailable():
            sleep(route.verifierDelay)
        else:
            routeIndex = failoverToNextRoute(routes, routeIndex)
    return routeIndex

def restoreRoute(routes, routeIndex):
    currentRouteIndex = routeIndex - 1
    if(currentRouteIndex < 0):
        currentRouteIndex = len(routes) - 1
    currentRoute = routes[currentRouteIndex]
    currentRoute.onTearDown()
    restoreRoute = routes[routeIndex]
    restoreRoute.onSetup()
    createRoute(restoreRoute)
    restoreRoute.onConnectionRestored()
    sleep(restoreRoute.verifierDelay)

def failoverToNextRoute(routes, routeIndex):
    currentRoute = routes[routeIndex]
    currentRoute.onTearDown()
    routeIndex = routeIndex + 1
    if routeIndex >= len(routes):
        routeIndex = 0
    failoverRoute = routes[routeIndex]
    failoverRoute.onSetup()
    createRoute(failoverRoute)
    currentRoute.onConnectionFailed()
    failoverRoute.onConnected()
    return routeIndex
                
if __name__ == "__main__":
    main(sys.argv[1:])
