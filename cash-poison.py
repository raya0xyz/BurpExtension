# _POISON_IT_


from burp import IBurpExtender, IHttpRequestResponse, IContextMenuFactory
from java.io import PrintWriter
from javax.swing import JMenuItem
from java.util import List, ArrayList
from threading import Thread


def generate_cyclic_pattern(length):
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pattern = ""
        for a in charset:
            for b in charset.lower():
                for c in "0123456789":
                    if len(pattern) >= length:
                        return pattern[:length]
                    pattern += a + b + c
        return pattern[:length]
  

class BurpExtender(IBurpExtender, IContextMenuFactory):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)

        callbacks.setExtensionName("X")
        # Registerd Context Menu Factory
        callbacks.registerContextMenuFactory(self)

        self._stdout.println("[*] Extension Loaded")
        self._stdout.println("_______________________________________________")

    # This has not been used
    def long_header():
        # return headers= {
        #     "Random-Header": generate_cyclic_pattern(15000),
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Encoding": "gzip,deflate,br",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        #     }
        return header


    ## Right-Click gareako bela ma, it will display extenion `X`.
    def createMenuItems(self, invocation):
        menu = ArrayList()
        menu.add(JMenuItem("X", actionPerformed=lambda e: self.handle_action(invocation)))
        return menu

    def handle_action(self, invocation):

        def worker():
            try:
                # Selects the Request
                selected_messages = invocation.getSelectedMessages()
                if not selected_messages:
                    return # if none selected return nth.

                # From selected_message
                for message in selected_messages:
                    request = message.getRequest() # Pull request
                    # Get Helper for `message` from `selected_message`. 
                    request_info = self._helpers.analyzeRequest(message) 
                    headers = list(request_info.getHeaders())

                    # Generating Random Cyclic Pattern
                    headers.append("Random-Header: "+ generate_cyclic_pattern(50)) # <--------------- Update later
                    # Since I will be working with GET message this might not be needed.
                    body = request[request_info.getBodyOffset():]  # <------------------
                    new_request = self._helpers.buildHttpMessage(headers, body) # <------ Since working with GET request this body might just be empty
                    self._stdout.println(body)
                    self._stdout.println(new_request)
                    # Send modified request
                    http_service = message.getHttpService() # Just used to get HTTP service.
                    # Makes the request with appropriate Service.
                    response = self._callbacks.makeHttpRequest(http_service, new_request)
                    self._stdout.println(response)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    # Parse response
                    # resp_info = self._helpers.analyzeResponse(response.getResponse())
                    # status_code = resp_info.getStatusCode()
                    # self._stdout.println("[+] Got response: HTTP %d for %s" % (status_code, request_info.getUrl()))
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            except Exception as e:
                self._stderr.println("Error in thread: %s" % str(e))

        Thread(target=worker).start()

    # def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
    #     try:
    #         if messageIsRequest:
    #             requestInfo = self._helpers.analyzeRequest(messageInfo)
    #             self._stdout.println("[Resuest] Host: %s | Method: %s | URl: %s " %(host, method, URL)) 
    #     except Exception as e:
    #         self._stderr.println("Error: %s " % str(e))
