import requests
from package import Package


class OSVClient:
    """
    Sert à communiquer avec l'API OSV.
        Cette API OSV interroge elle même les vulnérabilités d'un package via POST
    """

    URL_API_OSV = "https://api.osv.dev/v1/query"

    def interroger_api(self, package: Package):
        """ interroge l'API OSV grace à une requête HTML et retourne sa réponse au format json

        Parameters
        ----------
        package: Package
            Correspond au package dont on veut étudier les vulnérabilités et les licences.

        Return
        ------
        dict
            Renvoie la réponse de la l'API OSV au format JSON sous la forme d'un dictionnaire.

        """

        payload = {
            "version": package.version,
            "package": {
                "name": package.nom,
                "ecosystem": package.ecosysteme
            }
        }

        response = requests.post(
            self.URL_API_OSV,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

