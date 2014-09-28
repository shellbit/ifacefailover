import logging, requests
from time import sleep


class HttpHandler:
    def __str__(self):
        return str(self.__dict__)
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
        
    def onSetup(self, **kwargs):
        self.httpPost(kwargs.get('onSetupUrlSuffix', None), **kwargs)
    
    def onTearDown(self, **kwargs):
        self.httpPost(kwargs.get('onTearDownUrlSuffix', None), **kwargs)
        
    def onConnectionFailed(self, **kwargs):
        self.httpPost(kwargs.get('onConnectionFailedUrlSuffix', None), **kwargs)
    
    def onConnectionRestored(self, **kwargs):
        self.httpPost(kwargs.get('onConnectionRestoredUrlSuffix', None), **kwargs)
    
    def onConnected(self, **kwargs):
        self.httpPost(kwargs.get('onConnectedUrlSuffix', None), **kwargs)
    
    def onAvailable(self, **kwargs):
        pass

    def httpPost(self, urlSuffix, **kwargs):
        if urlSuffix is not None:
            maxRetry = kwargs.get('maxRetry', 120)
            retryDelay = kwargs.get('retryDelay', 0.5)
            attempts = 0
            while attempts < maxRetry:
                try:
                    attempts += 1
                    logging.info('Attempting POST request {} of {}'.format(attempts, maxRetry))
                    #TODO: This requests sometimes hangs and never timeouts
                    r = requests.post(kwargs.get('url') + urlSuffix, auth=kwargs.get('auth', None), headers=kwargs.get('headers', {}))
                    if r.status_code == 200:
                        attempts = maxRetry
                except Exception as e:
                    logging.error(e)
                    sleep(retryDelay)
