import biothings.hub.dataload.uploader as uploader
from .parser import load_data


class WikiPathwaysUploader(uploader.BaseSourceUploader):

    name = "wikipathways"

    def load_data(self, data_folder):
        self.logger.info("Load data from folder '%s'" % data_folder)
        wikipathways_docs = load_data(data_folder)
        return wikipathways_docs
