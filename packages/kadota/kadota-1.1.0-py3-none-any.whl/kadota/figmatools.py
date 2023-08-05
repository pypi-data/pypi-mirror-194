import requests
import json
import pprint

class FigmaFile:
    def __init__(self, access_token, file_id):
        # Set up the Figma file connection
        self.endpoint = 'https://api.figma.com/v1'
        self.access_token = access_token
        self.file_id = file_id
        # We'll need this for subsequent requests
        self.headers = {'X-Figma-Token': self.access_token}

        # Report successful connection
        self.file_url = f'{self.endpoint}/files/{self.file_id}'
        file_data = self.get_file_data()
        print(f'Connected to figma file')
        print(f'File name: {file_data["name"]}')
        print(f'File url:  {self.file_url}')
        
    def get_file_data(self):
        """
        Retrieves the data for the Figma file. Includes name, 
        thumbnails, owners, version, etc.

        Importantly, it includes the full node hierarchy for the file.
        """
        response = requests.get(self.file_url, headers=self.headers)
        return json.loads(response.text)

    def get_elements(self, element_name=None):
        """
        Gets elements that match the specified page and/or element name.
        
        If page_id is not None, the search is restricted to the specified page.
        
        If element_name is not None, the search is restricted to elements with the specified name.
        
        If neither page_id nor element_name is specified, all elements are returned.
        """
        elements = []
        file_data = self.get_file_data()
        
        # Traverse the document hierarchy to find the matching elements
        def traverse(node):
            element_filter = element_name is None or node['name'] == element_name
            if element_filter:
                elements.append(node)
            
            # Non page elements have children, search those too
            if 'children' in node:
                for child in node['children']:
                    traverse(child)
        
        for node in file_data['document']['children']:
            traverse(node)
        
        return elements

    def get_page_ids_by_name(self, page_name):
        """
        Gets the page ids that match the given page name.
        """
        page_ids = []
        file_data = self.get_file_data()
        for node in file_data['document']['children']:
            if node['type'] == 'CANVAS' and node['name'] == page_name:
                page_ids.append(node['id'])
        return page_ids
