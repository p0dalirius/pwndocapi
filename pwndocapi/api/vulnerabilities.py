class vulnerabilities(object):
    """
    Documentation for class vulnerabilities
    """

    def __init__(self, api):
        super(vulnerabilities, self).__init__()
        self.api = api
    
    def list(self, lang):
        if self.api.isLoggedIn():
            return self.api.vulnerabilities_list(lang)
        else:
            return None