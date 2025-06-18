# LOGGER #
# https://portswigger.net/burp/extender/api/

from burp import IBurpExtender, IHttpListener
from java.io import PrintWriter

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        # Creates helper to work with HTTP Message
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Simple Logger")

        # stdout/stderr for logging
        # Remeber this as syntax for logging in Jython.
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)

        # When instance of this method is called
        # Sign-me up or Notify me whenever HTTP messages is happning
        callbacks.registerHttpListener(self)
        self._stdout.println("[-] A02xt Loaded Successfully ")
        self._stdout.println("[-] IBurpExtender Load Success ")
        self._stdout.println("[-] Moving on to IHttpListener ")
        self._stdout.println(".. ... ")

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        try:
            # messageIsRequest throws bool if method is invoked for request or response
            if messageIsRequest:
                #// since we called .analyzeRequest(messgaeInfo) we are logging only request
                #// I guess to log respone ther must be method sth similar like .analyzeResponse(messageInfo)
                requestInfo = self._helpers.analyzeRequest(messageInfo)
                method = requestInfo.getMethod()
                URL = requestInfo.getUrl()
                host = URL.getHost()

                self._stdout.println("[Resuest] Host: %s | Method: %s | URl: %s " %(host, method, URL)) 

        except Exception as e:
            #// IDK what kind of error it will log, what is `e` ?
            self._stderr.println("Error: %s " % str(e))           


#________________________________________________________________________________________________
"""
basicall what have we done,
    1. IBurpExtender must be improted and defined with class name `BurpExtender`
    2. The Class takes to arg `IBurpExtender` for fundamental extension support 
    and `IHttpListener` for listeneing with HTTP messages
    
    3. Once class is defined,
        3.1  registerExtenderCallbacks() was so that we receive callback for burp.
        3.2  First I set self._callback then self._helper for creating helper to work with Req/Res.
        3.3  Then I registerd current instance of extension for any HTTP req/res with `callback.registerHttpListener(self)`
    
    4. Method `processHttpMessage()` from IHttpListener
        4.1  define the method
        4.2  When Method `processHttpMessage()` is invoke it returns *true*
        4.3  If will execute and with the helper I prepare to alayze request
        4.4  From that HTTP Request analyze I extracted Method, URL and Host. 

    5. Then everything is logged accordingly.
"""  
#________________________________________________________________________________________________
