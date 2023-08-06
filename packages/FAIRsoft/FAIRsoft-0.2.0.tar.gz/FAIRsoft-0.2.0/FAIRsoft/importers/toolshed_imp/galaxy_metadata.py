import os
import logging
from utils import connect_db, push_entry, save_entry


class dMetadataFetcher():
    def __init__(self, tools_galaxy_metadata):
        self.repositories = tools_galaxy_metadata
        self.seen_tools = set()
        
    def get_dependencies(self, latest_revision):
        if latest_revision['tool_dependencies']:
            return(list(latest_revision['tool_dependencies'].keys()))
        else:
            return([])
    
    def retrieve_metadata(self, tool):
        if tool:
            latest_revision_id = max(iter(tool.keys()))
            latest_revision = tool[latest_revision_id]
            if 'tools' in latest_revision.keys():
                dependencies = self.get_dependencies(latest_revision)
                for t in latest_revision['tools']:
                    if latest_revision['tools'][0]['id']+latest_revision['tools'][0]['version'] not in self.seen_tools:
                        entry = {}
                        entry['id'] = latest_revision['tools'][0]['id']
                        entry['name'] = latest_revision['tools'][0]['name']
                        entry['version'] = latest_revision['tools'][0]['version']
                        entry['dependencies'] = dependencies
                        entry['@data_source'] = "galaxy_metadata"
                        self.seen_tools.add(latest_revision['tools'][0]['id']+latest_revision['tools'][0]['version'])
                        entry['@id'] = 'https://openebench.bsc.es/monitor/tool/galaxy_metadata:{name}:{version}/cmd'.format(name=entry['id'], version=entry['version'])
                        return(entry)
        return({})

    def process_metadata(self):
        STORAGE_MODE = os.getenv('STORAGE_MODE', 'db')

        if STORAGE_MODE =='db':
            alambique = connect_db()
        else:
            OUTPUT_PATH = os.getenv('OUTPUT_PATH', './data/toolshed.json')

        for tool in self.repositories:

            entry = self.retrieve_metadata(tool)
            if entry:
                if STORAGE_MODE=='db':
                    push_entry(entry, alambique)
                else:
                    save_entry(entry, OUTPUT_PATH)
            else:
                continue
        
