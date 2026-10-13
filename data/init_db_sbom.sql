-- Création de la table SBOM
DROP TABLE IF EXISTS sbom CASCADE;

CREATE TABLE sbom (
    id_sbom         SERIAL PRIMARY KEY,
    id_audit        INTEGER NOT NULL,
    contenu         TEXT NOT NULL,
    date_generation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    format          VARCHAR(50) NOT NULL
);