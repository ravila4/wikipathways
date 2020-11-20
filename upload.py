import biothings.hub.dataload.uploader as uploader
from .parser import load_data


class WikiPathwaysUploader(uploader.BaseSourceUploader):

    name = "wikipathways"
    __metadata__ = {
        "src_meta": {
            'license_url': 'https://www.wikipathways.org/index.php/WikiPathways:License_Terms',
            'licence': 'CC0 1.0 Universal',
            'url': 'https://www.wikipathways.org/'
            }
        }

    def load_data(self, data_folder):
        self.logger.info("Load data from folder '%s'" % data_folder)
        wikipathways_docs = load_data(data_folder)
        return wikipathways_docs
