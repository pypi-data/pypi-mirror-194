"""A Namespace to hold functions related to creating genesets in the database."""
import logging
from typing import Optional

import psycopg2
from psycopg2.extensions import cursor

from jax.geneweaver.core.schema import User, GenesetUpload, Publication
from jax.geneweaver.core.enum import GenesetAccess, CurationAssignment, AnnotationType
from jax.geneweaver.core.exc import GeneweaverException

from jax.geneweaver.db import sql
from jax.geneweaver import db as db_svc
from jax.geneweaver.db import user as user_svc
from jax.geneweaver.db import publication as publication_svc
from jax.geneweaver.db.gene import get_gene_id_int


def geneset_for_user(db: cursor, user: User,
                     geneset: GenesetUpload,
                     publication: Optional[Publication] = None,
                     file_url: Optional[str] = None):
    """"""
    # Create publication
    publication_id = publication_svc.get_or_create(db, publication) if publication else None

    # Create geneset
    if geneset.access == GenesetAccess.PRIVATE:
        curation_level = CurationAssignment.APPROVED
        gs_groups = '-1'
    else:
        curation_level = CurationAssignment.REVIEWED
        gs_groups = '0'

    if len(geneset.groups) > 0:
        gs_groups = ','.join(geneset.groups)

    # TODO:
    gene_data = None
    gene_count = None

    gene_identifier = get_gene_id_int(geneset.gene_identifier)

    create_geneset_args = sql.geneset.CreateGeneset2Args(
        user_id=user.id,
        curation_id=curation_level.value,
        species_id=geneset.species,
        threshold_type=None,
        threshold_value=None,
        groups=gs_groups,
        status='normal',
        count=gene_count,
        uri='',
        gene_id_type=gene_identifier,
        name=geneset.name,
        abbreviation=geneset.abbreviation,
        description=geneset.description,
        attribution=None,
        file_contents=gene_data
    )
    try:
        sql.geneset.call_create_geneset2(db, create_geneset_args)

        result = db.fetchone()
        if not result:
            raise GeneweaverException(f'Failed to create geneset: {create_geneset_args.dict()}')

        geneset_id = result[0]
        db.connection.commit()
        logging.info(f'Created geneset "{geneset.name}" with ID {geneset_id}')

        if publication_id is not None:
            sql.geneset.add_geneset_publication(db, geneset_id, publication_id)
            db.connection.commit()

    except psycopg2.Error as e:
        db.connection.rollback()
        raise GeneweaverException(f'Failed to create geneset: {create_geneset_args.dict()}') from e

    # Some genesets contain no genes. We need to remove those genesets
    gene_count = get_geneset_gene_count(db, geneset_id)
    if gene_count < 1:
        sql.geneset.set_geneset_as_deleted(db, geneset_id)
        db.connection.commit()

    # get the user's annotator preference.  if there isn't one in their user
    # preferences, default to the monarch annotator
    annotator = AnnotationType(user_svc.get_user_preferences(db, user.id).get('annotator', 'monarch'))
    db_svc.annotator.insert_annotations(db, geneset_id, geneset.description, publication.abstract, annotator)


def get_geneset_gene_count(db: cursor, geneset_id: int):
    """"""
    sql.geneset.count_geneset_genes(db, geneset_id)
    result = db.fetchone()
    if not result:
        raise GeneweaverException(f'Failed to get gene count for geneset {geneset_id}')

    return result[0]














