
import json
import uuid
from typing import Any

from business_object.ComposanteSBOM import ComposanteSBOM


class ExportateurSBOM:
    """Construit un document SBOM au format CycloneDX JSON."""

    VERSION_SPEC = "1.7"
    CLE_RACINE = "__racine__"

    def exporter_cyclonedx(
        self,
        nom_projet: str,
        composantes: list[ComposanteSBOM],
        dependances: dict[str, list[str]],
        version_projet: str | None = None,
    ) -> str:
        """Construit et sérialise un SBOM au format CycloneDX."""

        document = self._construire_document(
            nom_projet,
            version_projet,
            composantes,
            dependances,
        )

        return self._serialiser_json(document)

    def _construire_document(
        self,
        nom_projet: str,
        version_projet: str | None,
        composantes: list[ComposanteSBOM],
        dependances: dict[str, list[str]],
    ) -> dict[str, Any]:
        """Construit la structure Python du document CycloneDX."""

        pass
    def _convertir_composante(
        self,
        composante: ComposanteSBOM,
        reference: str,
    ) -> dict[str, Any]:
        """Convertit un objet métier en composant CycloneDX."""

        pass

    def _construire_dependances(
        self,
        dependances: dict[str, list[str]],
        references: dict[str, str],
    ) -> list[dict[str, Any]]:
        """Convertit les relations en références CycloneDX."""

        pass

    def _serialiser_json(
        self,
        document: dict[str, Any],
    ) -> str:
        """Convertit le document Python en texte JSON."""

        pass