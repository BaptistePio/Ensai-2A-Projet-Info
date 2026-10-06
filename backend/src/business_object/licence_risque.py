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
        for key in cls.MAPPING_LICENCE:
            if cls.MAPPING_LICENCE[key] >= seuil:
                cls.licence_risque[key] = cls.MAPPING_LICENCE[key]

    @classmethod
    def obtenir_score(cls, licence):
        return cls.MAPPING_LICENCE.get(licence.id_spdx, 0)
