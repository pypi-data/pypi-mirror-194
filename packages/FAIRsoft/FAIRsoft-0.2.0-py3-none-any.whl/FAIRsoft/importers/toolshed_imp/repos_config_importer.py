
import requests
import json
import zipfile
import io
from bs4 import BeautifulSoup
import logging
import os

from utils import connect_db, push_entry, save_entry


class toolShedMetadataFetcher():

    def __init__(self, tools_galaxy_metadata, only_new):
        self.only_new = only_new
        logging.debug(f"Only new:{self.only_new}")
        if self.only_new:
            # only unseen: only repos not already in DB are processed
            self.seen_repos = self.compute_initial_seen_repos()
        else:
            self.seen_repos = set()
        

        self.repositories = self._build_repositories(tools_galaxy_metadata)
        self.all_metadata = []

    def compute_initial_seen_repos(self):
        seen = set()
        for entry in self.alambique.find({'@data_source':'toolshed'}):
            seen.add(entry['@source_url'])
        return(seen)

    def _build_repositories(self, tools_galaxy_metadata):
        repositories = []
        repos_n = 0
        repos_unseen = 0
        logging.debug('Fetching repo information from tools_galaxy_metadata')
        for tool in tools_galaxy_metadata: 
            if tool: # we ignore empty metadata
                repos_n += 1
                #print("Reading repo %d"%(repos_n))
                latest_revision_id = max(iter(tool.keys()))
                latest_revision = tool[latest_revision_id]
                keys = repositoryKeys(latest_revision['repository_id'], latest_revision['changeset_revision'])
                if self.only_new:
                    if self.seen_repository(keys) == False:
                        repositories.append(shed_repository(keys))
                        #print(f"Seen {keys.__dict__}")
                    else:
                        repos_unseen += 1
                else:
                    repositories.append(shed_repository(keys))

        logging.debug('number of repositories: %d'%(repos_n))
        logging.debug('number of repositories: %d'%(len(repositories)))

        return(repositories)

    def seen_repository(self, keys):
        ID_URL = f"https://toolshed.g2.bx.psu.edu/repository/download?repository_id={keys.repository_id}&changeset_revision={keys.changeset_revision}&file_type=zip"
        if ID_URL in self.seen_repos:
            return(True)
        else:
            return(False)
    
    def get_toolShed_files(self):

        for repo in self.repositories:
            repo.parse_valid_XMLs() ## XML downloading and parsing
            
            self.push_to_DB(repo.meta)
            #self.all_metadata.append(repo.meta)
        
    def export_metadata(self, outfile):
        with open(outfile, 'w') as outf:
            json.dump(self.all_metadata, outf)

    def  push_to_DB(self, repo, log):
        STORAGE_MODE = os.getenv('STORAGE_MODE', 'db')

        if STORAGE_MODE =='db':
            alambique = connect_db()
        else:
            OUTPUT_PATH = os.getenv('OUTPUT_PATH', './data/toolshed.json')

        for entry in repo:
            entry['@id'] = 'https://openebench.bsc.es/monitor/tool/toolshed:{name}:{version}/cmd'.format(name=entry['id'], version=entry['version'])
            if STORAGE_MODE=='db':
                push_entry(entry, alambique)
                
            else:
                save_entry(entry, OUTPUT_PATH, log)

class repositoryKeys():
    def __init__(self, repository_id, changeset_revision):
        self.repository_id = repository_id
        self.changeset_revision = changeset_revision

def get_url(url):
    session = requests.Session()
    try:
        re = session.get(url, timeout=30)
    except Exception as e:
        logging.warning(f'error with {url} - html_request')
        logging.warning(e)
        return(None)
    else:    
        return(re)

class shed_repository(object):
    def __init__(self, keys):
        self.keys = keys
        self.z = None
        self.contentList=[]
        self.validXMLs = []
        self.meta = {}
    
    def parse_valid_XMLs(self): 
        self._get_repository_content()
        self.validXMLs = self._get_validXML()
        self.meta = self._parse_xmls()

    def _get_repository_content(self):
        fileurl = "https://toolshed.g2.bx.psu.edu/repository/download?repository_id={repository_id}&changeset_revision={changeset_revision}&file_type=zip"
        self.url = fileurl.format(repository_id=self.keys.repository_id,  
                            changeset_revision=self.keys.changeset_revision) 
        response = get_url(self.url)
        if response:
            try:
                self.z = zipfile.ZipFile(io.BytesIO(response.content), 'r')
                self.contentList = self.z.namelist()
            except:
                logging.warning(f'error with {self.url} - empty zip')
            
    def _get_validXML(self):
        valids = []
        for f in self.contentList:
            if '.xml' in f and True not in [word in f for word in exclude]:
                fil = self.z.open(f)
                BS = BeautifulSoup(fil, features="xml")
                if self._thisIsATool(BS) == True:
                    valid = [BS, '/'.join(f.split('/')[:-1])]
                    valids.append(valid)
        return(valids)

    def _parse_xmls(self):
        TOOLS = []
        # Parsing the files...
        for Tool in self.validXMLs:
            # build dictionary with macros
            tool = Tool[0]
            base_url = Tool[1]
            if tool.tool.macros:
                imports = [a.get_text() for a in tool.tool.macros.findAll("import")]
                macros = self._get_macros(imports, base_url)
            else:
                macros = {'tokens': {}, 'requirements': []}
                    
            t = {}
            
            t['id'] = self._rMacros(macros['tokens'], tool.tool['id']) if 'id' in tool.tool.attrs.keys() else None
            t['name'] = self._rMacros(macros['tokens'], tool.tool['name']) if 'name' in tool.tool.attrs.keys() else None
            t['version'] = self._rMacros(macros['tokens'], tool.tool['version']) if 'version' in tool.tool.attrs.keys() else None
            t['description'] = self._rMacros(macros['tokens'], tool.tool.description.get_text()) if tool.tool.description else None
            t['code_file'] = self._rMacros(macros['tokens'], tool.tool.code['file']) if tool.tool.code else None
            t['language'] = t['code_file'].split('.')[-1] if tool.tool.code else None
            if tool.tool.command:
                t['command'] = self._rMacros(macros['tokens'], tool.tool.command.get_text())
                if  'interpreter' in tool.tool.command.attrs.keys():
                    t['interpreter'] = self._rMacros(macros['tokens'], tool.tool.command['interpreter']) 
                else:
                    t['interpreter'] = None
            else:
                t['command'] = None
            t['dataFormats'] =  self._parse_in_out(tool)
            t['help'] = self._rMacros(macros['tokens'], str(tool.tool.help.get_text())) if tool.tool.help else None
            t['tests'] = self._existTest(tool)
            t['citation'] = self._get_citations(tool.tool.citations, macros) if tool.tool.citations else None
            # this does not come from XML:
            t['readme'] = self._existREADME()
            
            t['@data_source'] = 'toolshed' 
            t['@source_url'] = self.url
            TOOLS.append(t)

        return(TOOLS)

    def _get_macros(self, macrosList, baseUrl):
        '''
        Takes a list of paths for macros and returns a 
        dictionary with the tokens inside them
        '''
        macros = {}
        tokens = {}
        for imp in macrosList:
            filepath = baseUrl + '/' + imp
            Import = self.z.open(filepath)
            BSmacros = BeautifulSoup(Import, features="xml")
            ##------------- tokens ---------------------------
            tokens = self._parse_tokens(BSmacros, tokens)
        macros['tokens'] = tokens
        #macros['requirements'] = requirements
        return(macros)
            
    def _parse_tokens(self, BSmacros, tokens):
        fields = [a for a in BSmacros.findAll("token")]
        for e in fields:
            if '\\$' not in e.get_text().lstrip():
                tokens[e['name']] = e.get_text().lstrip()
        return(tokens)

    def _existREADME(self):
        for f in self.contentList:
            if 'README' in f and True not in [word in f for word in exclude]:
                return(True)
            else:
                continue
        return(False)

    def _get_citations(self, citations, macros):
        cits = []
        for child in citations.findAll("citation"):
            cits.append({'citation' : self._rMacros(macros['tokens'], str(child.get_text())), 'type':  self._rMacros(macros['tokens'], str(child.get('type', None)))})
        return(cits)
    
    def _parse_in_out(self, tool):
        inOut = {}
        inFormats = []
        outFormats = []
        
        for inp in [a for a in tool.findAll("inputs")]:
            for f in  [a for a in inp.findAll(["param","data"])]:
                inFormats.append(f['format']) if 'format' in f.attrs.keys() else None
                
        for outp in [a for a in tool.findAll("outputs")]:
            for f in  [a for a in outp.findAll(["param", "data"])]:
                outFormats.append(f['format']) if 'format' in f.attrs.keys() else None
        
        inOut['inputs'] = inFormats
        inOut['outputs'] = outFormats
        
        return(inOut)
        
    def _rMacros(self, macroTokens, string):
        '''Checks if extended by macro. 
        If yes, the macro contentet is returned. 
        If not, the mail xml file content if returned.
        '''
        for key in macroTokens.keys():
            if key in string:
                string = string.replace(key, macroTokens[key])
        return(string)
    
    def _existTest(self, tool):
        if tool.findAll("test"):
            return(True)
        else:
            return(False)

    def _thisIsATool(self, BS):
        if BS.findAll('tool'):
            return(True)
        else:
            return(False)

exclude = ['dependencies','dependency','macros.xml','build.xml']

if __name__ == '__main__':
    # The repos metadata from galaxy contain the needed identifiers
    print('READING METADATA FOR IDS')
    GALAXY_METADATA=os.getenv('GALAXY_METADATA', 'galaxy_metadata.json')
    with open(GALAXY_METADATA, 'r') as outfile:
        repositories_metadata = json.load(outfile)
    toolShedMDF = toolShedMetadataFetcher(repositories_metadata)

    print('\nSARTING METADATA ZIP DOWNLOAD AND METADATA FETCHING')
    toolShedMDF.get_toolShed_files()
    
    print('\nExporting metadata as toolshed.json')
    toolShedMDF.export_metadata('toolshed.json')
    
    print('\nLoading to database')
    toolShedMDF.load_to_DB()
