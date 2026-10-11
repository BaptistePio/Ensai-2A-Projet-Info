from licence import Licence


class LicenceRisque:
    """
    Classe permet de réferencer les licences considérées comme à risque selon un seuil choisi.

    Les scores de ces licences à risque sont utilisés par la classe AuditSecurite pour évaluer l
    les risques juridiques
    (la classe additionne les score pour évaluer une partie global de sécurité)
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
        for licence, score in cls.MAPPING_LICENCE.items()
            if score >= seuil:
                licences_critiques[licence] = score
            elif score < seuil:
                if score == 0 or score == 1:
                    licences_faible[licence] = score
                else:
                    licences_moyennes[licence] = score
        return list[licences_critiques, licences_moyennes, licences_faible]

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
        return cls.MAPPING_LICENCE.get(licence.id_spdx, 0)
