import os
import glob
from datetime import date

from biothings.utils.dataload import tabfile_feeder, dict_sweep, unlist
import mygene


def load_data(data_folder):
    # Load .gmt (Gene Matrix Transposed) files
    for f in glob.glob(os.path.join(data_folder, "*.gmt")):
        data = tabfile_feeder(f, header=0)
        for rec in data:
            header = rec[0].split("%")
            # Get fields from header
            name = header[0]
            version = header[1]
            _id = header[2]
            species = header[3]
            # Get URL and gene list
            url = rec[1]
            ncbigenes = rec[2:]
            genes = [{"ncbigene": gene} for gene in ncbigenes]
            # Format schema
            doc = {'_id': _id,
                   'is_public': True,
                   'species': species,
                   'genes': genes,
                   'wikipathways': {
                       'pathway_name': name,
                       'version': version,
                       'url': url
                       }
                   }
            yield doc



if __name__ == "__main__":
    import json

    annotations = load_data("./test_data")
    for a in annotations:
        print(json.dumps(a, indent=2))
