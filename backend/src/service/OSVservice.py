from osv_client import OSVClient
from package import Package
from risque import Risque
from severite import Severite
from vulnerabilite import Vulnerabilite


class OSVService:
    """
    Transforme la réponse de l'API en OSV en objet métiers de notre API.
    """

    def __init__(self):
        self.osv_client = OSVClient()

    def scanner(self, package: Package):

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

        donnees = self.osv_client.interroger_api(package)

        vulnerabilites = []
        #va contenir les objets métier [Vinerabilite(...), Vunerabilite(...)]

        for v in donnees.get("vulns", []):
        #permet de parcourir les vulnerabilités, .get assure que cela ne plante pas
        #second argument indique quoi retourner si la clé n'existe pas 

            id_cve = v.get("id")

            description = v.get("summary", "")

            severite = self._extraire_severite(v)

            risque = self._construire_risque(severite)

            version_corrigee = self._version_corrigee(v)

            vulnerabilites.append(
                Vulnerabilite(
                    id_cve,
                    [package],
                    description,
                    risque,
                    severite,
                    version_corrigee
                )
            )

        return vulnerabilites

#méthodes construire_risque, version_corrigée et extraire_vulnerabilite seraient des méthodes privées de OSVService.
#Elles servent uniquement à transformer les données brutes renvoyées par l'API OSV en objets de ton modèle métier.