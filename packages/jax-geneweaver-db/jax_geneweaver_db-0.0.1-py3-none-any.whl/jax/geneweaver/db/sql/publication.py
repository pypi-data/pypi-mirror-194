from typing import Optional
from psycopg2.extensions import cursor
from jax.geneweaver.core.schema import PublicationUpload


def by_id(db: cursor, pub_id):
    return db.execute("SELECT * from publication WHERE pub_id=%s", (pub_id,))


def get_id_from_pubmed_id(db: cursor, pubmed_id) -> Optional[int]:
    """Get the publication ID for a given PubMed ID."""
    return db.execute('''SELECT pub_id FROM publication WHERE pub_pubmed=%s''', (pubmed_id,))


def create(db: cursor, publication: PublicationUpload):
    """Create a new publication record in the database."""
    return db.execute('''
            INSERT INTO publication

                (pub_authors, pub_title, pub_abstract, pub_journal,
                pub_volume, pub_pages, pub_month, pub_year, pub_pubmed)

            VALUES

                (%(authors)s, %(title)s, %(abstract)s,
                %(journal)s, %(volume)s, %(pages)s, %(month)s,
                %(year)s, %(pubmed)s)

            RETURNING pub_id;    
    ''', publication.dict())

