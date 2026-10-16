
from .ParsingDependances import ParsingDependances


class OSVService:
    """
    Transforme la réponse de l'API en OSV en objet métiers de notre API.
    """

    def __init__(self, osv_client):
        self.osv_client = osv_client

    def scanner(self, package):
        """ Va traiter la réponse retournée au format json dans OSVclient
            Elle transforme la réponse en business objects de notre API

        Parameters
        ----------
        package: Package
            Correspond au package dont on veut étudier les vulnérabilités et les licences.

        Return
        ------
        list[Vulnerabilite]
        Renvoie la liste des vulnérabilités du package et leurs caractéristiques.
        """

        reponse_json = self.osv_client.interroger_API(
            package
        )

        return ParsingDependances.parser(
            reponse_json
        )

