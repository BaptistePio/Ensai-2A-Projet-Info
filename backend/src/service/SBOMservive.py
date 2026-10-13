
from dao.SBOMdao import SBOMDao
from utils.log_utils import log

from business_object.SBOM import SBOM


class SBOMService:
    """Orchestre la génération et la récupération des SBOM."""

    @log
    def generer_sbom(self, id_audit: int) -> SBOM | None:
        """Génère et enregistre un SBOM pour un audit."""

        # 1. Récupérer les informations de l'audit
        # 2. Récupérer les composants nécessaires
        # 3. Construire le document avec ExportateurSBOM
        # 4. Créer l'objet SBOM
        # 5. Enregistrer le SBOM avec SBOMDao

        pass

    @log
    def recuperer_par_audit(self, id_audit: int) -> list[SBOM]:
        """Récupère les SBOM associés à un audit."""

        return SBOMDao().recuperer_par_audit(id_audit)

    @log
    def recuperer_par_id(self, id_sbom: int) -> SBOM:
        """Recupère le SBOM à partir de son identifiant."""

        return SBOMDao().recuperer_par_id(id_SBOM)
