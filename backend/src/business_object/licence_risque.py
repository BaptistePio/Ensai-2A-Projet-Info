class LicenceRisque:
    """
    Classe permettant de réferencer les licences considérées comme à risque selon un seuil choisi.

    Les scores de ces licences à risque sont utilisés par la classe AuditSecurite pour évaluer
    les risques associées aux licences utilisées par le code soumis
    (la classe additionne les scores pour évaluer une partie global de sécurité)
    """

    MAPPING_LICENCE = {"AGPL-3.0": 4,
    "GPL-3.0": 3,
    "GPL-2.0": 3,
    "LGPL-3.0": 2,
    "Apache-2.0": 1,
    "MIT": 0,
    "BSD-3-Clause": 0
    }

    @classmethod
    def licence_risque_ref(cls, seuil):
        """
        Parameters
        ----------
        seuil: int|float:
            seuil à partir duquel on considère qu'une licence est à risque


        Return
        ------
        dict[str: int]
            renvoi un dictionnaire dont les clés sont les licences à risque et indique leur score en attribut.
        """

        licences_faibles = {}
        licences_moyennes = {}
        licences_critiques = {}
        for licence, score in cls.MAPPING_LICENCE.items():
            if score >= seuil:
                licences_critiques[licence] = score
            elif score < seuil:
                if score == 0 or score == 1:
                    licences_faibles[licence] = score
                else:
                    licences_moyennes[licence] = score
        return {"critiques": licences_critiques,
        "moyennes": licences_moyennes,
        "faibles": licences_faibles
        }


    @classmethod
    def obtenir_score(cls, licence):
        """ Méthode de classe permettant d'obtenir le score de la licence considérée

        Parameters
        ----------
        licence: Licence
            Correspond au package dont on veut étudier les vulnérabilités et les licences.

        Return
        ------
        int
            renvoie le score de la licence selon le mapping de référence

        """
        if licence.idspdx not in cls.MAPPING_LICENCE:
            cls.MAPPING_LICENCE[licence.idspdx] = 0
        return cls.MAPPING_LICENCE.get(licence.idspdx, 0)

# pas besoin de repr ici. 
# LicenceRisque est une classe utilitaire qui ne connait pas Licence

