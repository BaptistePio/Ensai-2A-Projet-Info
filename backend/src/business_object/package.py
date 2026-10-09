from licence import Licence


class Package:
    '''
    '''
    def __init__(self, nom: str, version: str, ecosysteme: str, licence: Licence):
        self.nom = nom
        self.version = version
        self.ecosysteme = ecosysteme
        self.licence = licence