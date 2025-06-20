# _POISON_IT_


from burp import IBurpExtender, IHttpRequestResponse, IContextMenuFactory
from java.io import PrintWriter
from javax.swing import JMenuItem
from java.util import List, ArrayList
from threading import Thread
from java.net import URL



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

    # TO DISPLAY THE NAME OF EXTENISON
    def createMenuItems(self, invocation):
        menu = ArrayList()
        menu.add(JMenuItem("X", actionPerformed=lambda e: self.handle_action(invocation)))
        return menu

    # TAKES IHttpRequestRequest AND OUTPUT HUMAN READABLE OUTPUT
    def logRequest(self, messageInfo):
        request_info = self._helpers.analyzeRequest(messageInfo)
        headers = request_info.getHeaders()
        body = messageInfo.getRequest()[request_info.getBodyOffset():].tostring()
        return '\n'.join(headers) + '\n\n' + body
    
    # TAKES byte array AND RETURN HUMAN READABLE OUTPUT
    def logRequestFromBytes(self, byte_array):
        request_info = self._helpers.analyzeRequest(byte_array)
        headers = request_info.getHeaders()
        body = byte_array[request_info.getBodyOffset():].tostring()
        return '\n'.join(headers) + '\n\n' + body
    
    # TAKES IHttpRequestResponse AND OUTPUT HUMAN READABLE RESPONSE 
    def logResponse(self, messageInfo):
        response_info = self._helpers.analyzeResponse(messageInfo.getResponse())
        headers = response_info.getHeaders()
        body = messageInfo.getResponse()[response_info.getBodyOffset():].tostring()
        return '\n'.join(headers) + '\n\n' + body

    # HANDLE_ACTION CHECK IF IT HAS INVOKED
    def handle_action(self, invocation):
        def worker():
            try:
                # ONCE INVOKED GET MESSAGE FROM INVOCATION AND SAVE IT TO SELECTED_MESSAGE
                selected_messages = invocation.getSelectedMessages()
                if not selected_messages:
                    return # IF NO MESSAGE IS SELECTED THEN REURN NTH
                # From selected_message
                for message in selected_messages:
                    request = message.getRequest() # Pull request
                    request_info = self._helpers.analyzeRequest(message) 

                    urlCheck = request_info.getUrl()
                    hostCheck = urlCheck.getHost()
                    protocolCheck = urlCheck.getProtocol()
                    protCheck = urlCheck.getPort()
                    # Building URL
                    checkURL = "%s://%s:%d/un1gg4.js" % (protocolCheck, hostCheck, protCheck)
                    self._stdout.println("[-] Checking response of | %s" %checkURL)

                    # Build GET request 
                    newCheckReq = self._helpers.buildHttpRequest(URL(checkURL))
                    httpService = self._helpers.buildHttpService(hostCheck, protCheck, protocolCheck=="htttps")
                    
                    # Resposne Check
                    respCheck = self._callbacks.makeHttpRequest(httpService, newCheckReq)
                    respInfoCheck = self._helpers.analyzeResponse(respCheck.getResponse())
                    statusCheck = respInfoCheck.getStatusCode()


                    if statusCheck == 404:
                        self._stdout.println("[+]True (Got 404)")
                        headers = list(request_info.getHeaders())
                        headers.append("Random-Header: "+ generate_cyclic_pattern(50)) 
                        body = request[request_info.getBodyOffset():]  
                        new_request = self._helpers.buildHttpMessage(headers, body)
                        log_req = self.logRequestFromBytes(new_request)
                        self._stdout.println(log_req)
                        """
                        1. GET MESSAGE REQUEST                             (request)
                        2. GET HELPER TO WORK WITH REQUEST                 (request_info)
                        3. EXTRACT HEADERS
                        4. APPEND THE LONG HEADER
                        5. FORM REQUEST GET CONTENT OF REQUEST BODY 
                        6. CRAFT REQUEST                                   (request.appen + body)
                        7. LOG
                        """
                        http_service = message.getHttpService()
                        response = self._callbacks.makeHttpRequest(http_service, new_request)
                        log_resp = self.logResponse(response)
                        self._stdout.println(log_resp)
                        """
                        1.0 GET's HTTP SERVICE TYPE                 (http_service)
                        2.1 FIRST CRAFT REQUEST WITH SERVICE AND MODIFIED REQUEST && MAKES REQUEST
                        2.2 RESPOSNE IS THEN STORED                 (response)
                        3.0 LOG
                        """
                    else:
                        self._stdout.println("False (Got %d)" % statusCheck)
                        break

            except Exception as e:
                self._stderr.println("Error in thread: %s" % str(e))

        Thread(target=worker).start()
