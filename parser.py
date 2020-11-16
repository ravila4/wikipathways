import glob
import os
import requests
import urllib.parse
import logging

from biothings.utils.dataload import tabfile_feeder
import mygene


def load_data(data_folder):
    # Load .gmt (Gene Matrix Transposed) files
    for f in glob.glob(os.path.join(data_folder, "*.gmt")):
        # Get species name from the filename and convert to taxid
        species = f.replace(".gmt", "").split("-")[-1].replace("_", " ")
        taxid = get_taxid(species)
        data = tabfile_feeder(f, header=0)
        for rec in data:
            header = rec[0].split("%")
            # Get fields from header
            pathway_name = header[0]
            wikipathways_id = header[2]
            assert species == header[3], "Species does not match."
            # Get URL and gene list
            url = rec[1]
            ncbigenes = rec[2:]
            genes = fetch_gene_ids(ncbigenes, taxid)
            # Format schema
            doc = {'_id': wikipathways_id,
                   'is_public': True,
                   'taxid': taxid,
                   'genes': genes,
                   'wikipathways': {
                       'id': wikipathways_id,
                       'pathway_name': pathway_name,
                       'url': url
                       }
                   }
            yield doc


def get_taxid(species):
    """Fetch taxonomic ID given a scientific name."""
    s = urllib.parse.quote(species)
    url = 'http://t.biothings.io/v1/query?q={}&fields=taxid&limit=1'.format(s)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        taxid = data['hits'][0]['taxid']
        return taxid


def fetch_gene_ids(ncbi_ids, taxid):
    """Given entrez (ncbi) ids, fetch ensembl, gene symbol, name and _id."""
    mg = mygene.MyGeneInfo()
    fields = "ensembl.gene,symbol,name"
    response = mg.querymany(ncbi_ids, scopes='entrezgene',
                            species=taxid, fields=fields, returnall=True)
    genes = []
    for out in response['out']:
        query = out['query']
        if out.get('notfound'):
            logging.warn("NCBI ids with no hits may be deprecated, skipping."
                         .format(query))
            continue
        gene = {'mygene_id': out['_id'],
                'ncbigene': query,
                'symbol': out['symbol'],
                'name': out['name']
                }
        if out.get('ensembl') is not None:
            if len(out['ensembl']) > 1:
                for i in out['ensembl']:
                    gene.setdefault('ensemblgene', []).append(i['gene'])
            else:
                gene['ensemblgene'] = out['ensembl']['gene']
        genes.append(gene)
    return genes


if __name__ == "__main__":
    import json

    annotations = load_data("./test_data")
    for a in annotations:
        print(json.dumps(a, indent=2))
