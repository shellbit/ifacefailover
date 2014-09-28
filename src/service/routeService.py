import logging, netinfo
from time import sleep

from route import Route


DESTINATION = 'dest'
GATEWAY = 'gateway'
GENMASK = 'netmask'
IFACE = 'dev'

def getRoutes():
    routes = []
    for route in netinfo.get_routes():
        routes.append(Route(route[DESTINATION], route[GATEWAY], route[GENMASK], route[IFACE]))
    return routes

def getRoute(destination):
    for route in getRoutes():
        if route.destination == destination:
            return route
    return None

def addRoute(route):
    # TODO: Move to external properties
    retryDelay = 0.5
    maxRetry = 120
    attempts = 0
    while attempts < maxRetry:
        try:
            attempts += 1
            logging.info('Adding route {}; attempt {} of {}'.format(route.iface, attempts, maxRetry))
            validateResponse(netinfo.add_route(route.iface, route.destination, route.gateway, route.genmask))
            attempts = maxRetry
        except Exception as e:
            logging.error(e)
            sleep(retryDelay)

def deleteRoute(route):
    validateResponse(netinfo.del_route(route.iface, route.destination, route.gateway, route.genmask))

def validateResponse(response):
    if response is not None:
        logging.error(response)
