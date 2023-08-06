import json
import logging

from utils import get_url, decode_json

class reposFetcher():

    def __init__(self):
        self.tools = []

    def fetch_tools(self):
        '''
        Fetches all the tools (las revision of each repository) from the Galaxy 
        Toolshed and stores them in self.tools.
        Metadata is extracted from the toolshed API.
        '''
        # fetch repos ids
        repositories_list = self._get_repositories_dict()
        
        # fetch metadata of each repository using id
        logging.debug('Fetching metadata of each repository from the Galaxy Toolshed API')

        for repository_dict in repositories_list:
            # Only unrestricted repositories are accessible
            if repository_dict['type']=='unrestricted':
                self.tools.append(galaxyTool(repository_dict))
        
        logging.debug(f"{len(self.tools)} repositories processed.")

        self.all_metadatas = [tool.metadata for tool in self.tools if tool.metadata]

    def _get_repositories_dict(self):
        '''
        Fetches metadata of all the repositories from the Galaxy Toolshed and returns a list of dictionaries. 
        Among the metadata, the id of each repository is of interest. 
        This id is used to fetch the metadata of each repository from the Toolshed API. 
        '''
        REPS_URL = "https://toolshed.g2.bx.psu.edu/api/repositories?" 
        logging.debug(f"Fetching metadata of all the repositories from the Galaxy Toolshed at {REPS_URL} to get their ids.")

        repositories_list = get_url(REPS_URL)
        if repositories_list:
            return(repositories_list)

        else:
            logging.error('error - crucial_object_empty')
            logging.error(f"no repositories metadata at {REPS_URL}. JSON is empty. Exiting ...")
            logging.info("end_importation")
            exit(1)

        
    
    def export_metadatas(self, output_file_name):
        all_metadatas = [tool.metadata for tool in self.tools if tool.metadata]
        with open(output_file_name, 'w') as outputfile:
            json.dump(all_metadatas, outputfile)

class galaxyTool():
    '''
    A galaxyTool is an individual tool repository from the Galaxy Toolshed.
    '''
    def __init__(self, repository_dict):
        self.metadata =  self._get_metadata(repository_dict)
        if self.metadata:
            self.revisions = self.metadata.keys()

    def _get_metadata(self, repository_dict):
        '''
        Fetches metadata of a repository from the Galaxy Toolshed API
        using its id.
        '''
        id_ = repository_dict['id']
        url = f"https://toolshed.g2.bx.psu.edu/api/repositories/{id_}/metadata?"
        
        meta = get_url(url)
        if meta:
            return(meta)
        else:
            logging.warning(f"error with {url} - empty")
            logging.warning(f"Metadata for repository {url} not found.")
            return(meta)


if __name__ == '__main__':
    RF = reposFetcher()
    RF.fetch_tools()
    RF.export_metadatas('galaxy_metadatas.json')