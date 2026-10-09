from licence import Licence


class LicenceRisque:

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
        Attributes
        ----------
        seuil: int|float:
            seuil à partir duquel on considère qu'une licence est à risque


        Return
        ------
        dict{Licence: score: int }
            renvoi un dictionnaire prenant comme clé les licences à risque et indique son score en attribut.
        """
        return {
            licence: score
            for licence, score in cls.MAPPING_LICENCE.items()
            if score >= seuil
            }

    @classmethod
    def obtenir_score(cls, licence):
        """ Méthode de classe permettant d'obtenir le score de la licence considérée

        Attributes
        ----------
        licence: Licence
            Correspond au package dont on veut étudier les vulnérabilités et les licences.

        Return
        ------
        int
            renvoie le score de la licence selon le mapping de référence

        """
        return cls.MAPPING_LICENCE.get(licence.id_spdx, 0)
