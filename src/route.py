import ast, copy

from serializationUtil import deserialize


class Route:
    def __init__(self, destination, gateway, genmask, iface, targets=[], verifierDelay=0, verifier=None, verifierKwargs={}, handlers=[], handlerKwargs=[]):
        self.destination = destination
        self.gateway = gateway
        self.genmask = genmask
        self.iface = iface
        self.targets = copy.deepcopy(targets)
        self.verifierDelay = verifierDelay
        self.verifier = verifier
        self.verifierKwargs = copy.deepcopy(verifierKwargs)
        self.handlers = copy.deepcopy(handlers)
        self.handlerKwargs = copy.deepcopy(handlerKwargs)
        self.validate()
    
    def __str__(self):
        return str(self.__dict__)
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
    
    def validate(self):
        if len(self.handlers) != len(self.handlerKwargs):
            raise Exception('Handler and HandlerKwargs mismatch for route %s' % self.destination)
    
    def getTargetRoutes(self):
        routes = []
        for target in self.targets:
            routes.append(Route(target, self.gateway, '255.255.255.255', self.iface))
        return routes
    
    def isAvailable(self):
        upRoutes = []
        downRoutes = []
        for target in self.targets:
            if(self.verifier.isRouteAvailable(target, **self.verifierKwargs)):
                upRoutes.append(target)
            else:
                downRoutes.append(target)
        self.onAvailable(upRoutes, downRoutes)
        return len(upRoutes) > 0
    
    def onSetup(self):
        if self.handlers is not None:
            for index, handler in enumerate(self.handlers):
                handler.onSetup(**self.handlerKwargs[index])
    
    def onTearDown(self):
        if self.handlers is not None:
            for index, handler in enumerate(self.handlers):
                handler.onTearDown(**self.handlerKwargs[index])
    
    def onConnectionFailed(self):
        if self.handlers is not None:
            for index, handler in enumerate(self.handlers):
                handler.onConnectionFailed(**self.handlerKwargs[index])
    
    def onConnectionRestored(self):
        if self.handlers is not None:
            for index, handler in enumerate(self.handlers):
                handler.onConnectionRestored(**self.handlerKwargs[index])
    
    def onConnected(self):
        if self.handlers is not None:
            for index, handler in enumerate(self.handlers):
                handler.onConnected(**self.handlerKwargs[index])
    
    def onAvailable(self, upRoutes, downRoutes):
        if self.handlers is not None:
            for index, handler in enumerate(self.handlers):
                kwargs = self.handlerKwargs[index]
                kwargs['ifacefailover_uproutes'] = upRoutes
                kwargs['ifacefailover_downroutes'] = downRoutes
                handler.onAvailable(**kwargs)

def createRoutesFromProperties(properties):
    routeMap = {}
    for key, value in properties.iteritems():
        if key.startswith('route'):
            lineTokens = key.split('.')
            lineTokens.pop(0)
            name = lineTokens[0]
            routeProperty = lineTokens[1]
            route = routeMap.get(name, None)
            if route is None:
                route = Route('0.0.0.0', None, '0.0.0.0', None)
                routeMap[name] = route
            if 'gateway' == routeProperty:
                route.gateway = value
            elif 'iface' == routeProperty:
                route.iface = value
            elif 'targets' == routeProperty:
                route.targets = value.split(',')
            elif 'verifierDelay' == routeProperty:
                route.verifierDelay = float(value)
            elif 'verifier' == routeProperty:
                route.verifier = deserialize(value)
            elif 'verifierKwargs' == routeProperty:
                route.verifierKwargs = ast.literal_eval(value)
            elif 'handlers' == routeProperty:
                for handlerFile in ast.literal_eval(value):
                    route.handlers.append(deserialize(handlerFile))
            elif 'handlerKwargs' == routeProperty:
                for handlerKwargs in ast.literal_eval(value):
                    route.handlerKwargs.append(handlerKwargs)
    
    routes = []
    for route in routeMap.itervalues():
        route.validate()
        routes.append(route)
    return routes
