from business_object.SBOM import SBOM

class SBOMDao:
    """Stocke et sauvegarde le SBOM dans la base de données.
    """
    def __init__(self) -> None:
        pass

    def sauvegarder(sbom: SBOM) -> None:
        """Sauvegarde le SBOM dans la base de données.
        Attributes:
        sbom: SBOM
        C'est le SBOM qu'on veut sauvegarder.
        """
        pass

    def recuperer_par_audit(id_audit) -> list:
        """Recupère l'id_audit pour la fbricationn du SBOM correspondant à l'audit.
        """
        pass