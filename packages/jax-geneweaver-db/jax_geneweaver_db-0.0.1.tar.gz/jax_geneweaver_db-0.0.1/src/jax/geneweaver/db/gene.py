
def get_gene_id_int(gene_id_str: str) -> int:
    """
    This function returns a negative int for a gene db and a positive int for a microarray-based string
    :param gene_id_str: gene_*** or ma_***
    :return: either positive or negative int
    """
    prefix, identifier_int = gene_id_str.split('_')
    if prefix == 'ma':
        return int(identifier_int)
    else:
        return int(identifier_int) * -1
