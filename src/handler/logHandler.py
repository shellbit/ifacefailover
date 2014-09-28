import logging


class LogHandler:
    def __str__(self):
        return str(self.__dict__)
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
        
    def onSetup(self, **kwargs):
        logging.info('Setting up connection to %s' % kwargs.get('name'))
    
    def onTearDown(self, **kwargs):
        logging.info('Tearing down connection to %s' % kwargs.get('name'))
        
    def onConnectionFailed(self, **kwargs):
        logging.info('Connection failed on %s' % kwargs.get('name'))
    
    def onConnectionRestored(self, **kwargs):
        logging.info('Connection restored to %s' % kwargs.get('name'))
    
    def onConnected(self, **kwargs):
        logging.info('Failing over to %s' % kwargs.get('name'))
    
    def onAvailable(self, **kwargs):
        upRoutes = kwargs.get('ifacefailover_uproutes', [])
        downRoutes = kwargs.get('ifacefailover_downroutes', [])
        logging.info('upRoutes=%s; downRoutes=%s' % (', '.join(upRoutes), ', '.join(downRoutes)))
