from psycopg2.extensions import cursor
from pydantic import BaseModel


class CreateGeneset2Args(BaseModel):
    user_id: int
    curation_id: int
    species_id: int
    threshold_type: int
    threshold_value: float
    groups: str
    status: str
    count: int
    uri: str
    gene_id_type: int
    name: str
    abbreviation: str
    description: str
    attribution: int
    file_contents: str


def call_create_geneset2(db: cursor, create_geneset2_args: CreateGeneset2Args):
    return db.execute('''
        SELECT create_geneset2(
            %(user_id)s, 
            %(curation_id)s,
            %(species_id)s,
            %(threshold_type)s,
            %(threshold_value)s,
            %(groups)s,
            %(count)s,
            %(status)s,
            %(uri)s,
            %(gene_id_type)s,
            %(name)s,
            %(abbreviation)s,
            %(description)s,
            %(attribution)s,
            %(file_contents)s
        );
    ''', create_geneset2_args.dict())


def add_geneset_publication(db: cursor, geneset_id: int, publication_id: int):
    return db.execute('''
        UPDATE geneset SET pub_id=%(publication_id)s WHERE gs_id=%(geneset_id)s
    ''', {'geneset_id': geneset_id, 'publication_id': publication_id})


def count_geneset_genes(db: cursor, geneset_id: int):
    return db.execute('''
        SELECT count(*) FROM extsrc.geneset_value WHERE gs_id=%(geneset_id)s
    ''', {'geneset_id': geneset_id})


def set_geneset_as_deleted(db: cursor, geneset_id: int):
    return db.execute('''
        UPDATE geneset SET gs_status='deleted' WHERE gs_id=%(geneset_id)s
    ''', {'geneset_id': geneset_id})

