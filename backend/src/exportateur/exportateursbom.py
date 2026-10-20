
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

        ref_racine = f"root:{nom_projet}"
        if version_projet:
            ref_racine += f"@{version_projet}"

        references = {
            self.CLE_RACINE: ref_racine
        }

        # Créer une référence unique pour chaque composant.
        for composante in composantes:
            cle = f"{composante.nom}@{composante.version}"

            if cle in references:
                raise ValueError(
                    f"Clé de composant absente ou en double : {cle}"
                )

            references[cle] = f"component:{cle}"

        # Décrire le projet racine.
        composant_racine = {
            "type": "application",
            "bom-ref": ref_racine,
            "name": nom_projet,
        }

        if version_projet:
            composant_racine["version"] = version_projet

        # Convertir les composants du projet.
        composants_json = [
            self._convertir_composante(
                composante,
                references[
                    f"{composante.nom}@{composante.version}"
                ],
            )
            for composante in composantes
        ]

        document = {
            "bomFormat": "CycloneDX",
            "specVersion": self.VERSION_SPEC,
            "serialNumber": f"urn:uuid:{uuid.uuid4()}",
            "version": 1,
            "metadata": {
                "component": composant_racine
            },
            "components": composants_json,
            "dependencies": self._construire_dependances(
                dependances,
                references,
            ),
        }

        return document

    def _convertir_composante(
        self,
        composante: ComposanteSBOM,
        reference: str,
    ) -> dict[str, Any]:
        """Convertit un objet métier en composant CycloneDX."""

        resultat = {
            "type": "library",
            "bom-ref": reference,
            "name": composante.nom,
            "version": composante.version,
        }

        # Ajouter la licence si elle est renseignée.
        if composante.licence and composante.licence.strip():
            resultat["licenses"] = [
                {
                    "license": {
                        "name": composante.licence
                    }
                }
            ]

        # Ajouter le hash si sa valeur est disponible.
        if composante.hash_integrite:
            resultat["hashes"] = [
                {
                    "alg": "SHA-256",
                    "content": composante.hash_integrite,
                }
            ]

        return resultat

    def _construire_dependances(
        self,
        dependances: dict[str, list[str]],
        references: dict[str, str],
    ) -> list[dict[str, Any]]:
        """Convertit les relations en références CycloneDX."""

        # Vérifier que chaque élément possède une entrée.
        for source in references:
            if source not in dependances:
                raise ValueError(
                    f"Relations non renseignées pour : {source}"
                )

        resultat = []

        for source, cibles in dependances.items():
            if source not in references:
                raise ValueError(
                    f"Composant source inconnu : {source}"
                )

            for cible in cibles:
                if cible not in references:
                    raise ValueError(
                        f"Composant dépendant inconnu : {cible}"
                    )

            resultat.append(
                {
                    "ref": references[source],
                    "dependsOn": [
                        references[cible] for cible in cibles
                    ],
                }
            )

        return resultat

    def _serialiser_json(
        self,
        document: dict[str, Any],
    ) -> str:
        """Convertit le document Python en texte JSON."""

        return json.dumps(
            document,
            ensure_ascii=False,
            indent=2,
        )
