from burp import IBurpExtender

class BurpExtender(IBurpExtender):
    def registerExtenderCallbacks(self, callbacks):

        callbacks.setExtensionName("Minimal Ext")
        print("Hello Form BurpExtender !")

        callbacks.getStdout().write("Ext Load success")

        