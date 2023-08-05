from psycopg2.extensions import cursor
from jax.geneweaver.core.enum import AnnotationType


def insert_annotations(db: cursor, genest_id: int, description: str, abstract: str, annotation_type: AnnotationType):
    ...