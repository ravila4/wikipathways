import mygene


class QueryManager:
    def __init__(self, ids, id_type, species, cache_dict={}):
        self.ids = ids
        self.id_type = id_type
        self.species = species
        self.query_cache = cache_dict

    def query_mygene(self):
        """Query information from mygene.info about each gene in 'ids'."""
        mg = mygene.MyGeneInfo()
        # Fields to query
        fields = "entrezgene,ensembl.gene,uniprot,symbol,name,locus_tag"
        response = mg.querymany(self.ids,
                                scopes=self.id_type,
                                fields=fields,
                                species=self.species,
                                returnall=True)
        # Failed queries
        self.missing = response['missing']
        # Format successful queries
        for out in response['out']:
            query = out['query']
            if out.get('notfound'):
                continue
            gene = {'mygene_id': out['_id'],
                    'name': out['name'],
                    'symbol': out['symbol'],
                    }
            if out.get('entrezgene') is not None:
                gene['ncbigene'] = out['entrezgene']
            if out.get('ensembl') is not None:
                if len(out['ensembl']) > 1:
                    for i in out['ensembl']:
                        gene.setdefault('ensemblgene', []).append(i['gene'])
                else:
                    gene['ensemblgene'] = out['ensembl']['gene']
            if out.get('uniprot') is not None:
                gene['uniprot'] = out['uniprot']
            if out.get('locus_tag') is not None:
                gene['locus_tag'] = out['locus_tag']
            self.query_cache[query] = gene
