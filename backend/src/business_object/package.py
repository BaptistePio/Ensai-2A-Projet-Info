from .licence import Licence


class Package:
    '''
    '''
    def __init__(self, nom: str, version: str, ecosysteme: str, licence: Licence):
        self.nom = nom
        self.version = version
        self.ecosysteme = ecosysteme
        self.licence = licence

    def __repr__(self):
        return (
            f"Package("
            f"nom='{self.nom}', "
            f"version='{self.version}', "
            f"ecosysteme='{self.ecosysteme}', "
            f"licence={self.licence})"
        )


p = Package(
    nom="django",
    version="4.2.0",
    ecosysteme="PyPI",
    licence=Licence("BSD-3-Clause", "BSD", True)
    )

print(p)