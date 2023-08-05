import logging
from typing import Optional
from psycopg2.extensions import cursor

from jax.geneweaver.db import sql
from jax.geneweaver.core.schema import PublicationUpload
from jax.geneweaver.core.exc import GeneweaverException


def get_id_from_pubmed_id(db: cursor, pubmed_id) -> Optional[int]:
    sql.publication.get_id_from_pubmed_id(db, pubmed_id)
    result = db.fetchone()

    if not result:
        logging.debug(f"Publication with PubMed ID {pubmed_id} not found")
        return None

    return result if result else result[0]


def create(db: cursor, publication: PublicationUpload):
    sql.publication.create(db, publication)
    result = db.fetchone()

    if not result:
        raise GeneweaverException(f"Failed to create publication record for {publication.dict()}")

    return result[0]


def get_or_create(db: cursor, publication: PublicationUpload):
    """Get the publication ID for a given PubMed ID, or create a new record."""
    pub_id = get_id_from_pubmed_id(db, publication.pubmed)

    if pub_id:
        return pub_id

    logging.info(f"Creating new publication record for {publication.dict()}")
    return create(db, publication)


