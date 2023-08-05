import requests
import json
import pprint

import utils

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

    def get_all_elements(self):
        """
        Gets all elements in the Figma file. 
        
        There are four types of elements: frames, groups, components, and instances.

        Frames are the basic building blocks of a design. You can use them to create 
        different types of layouts, such as columns, grids, or even just a single element.

        Groups are a way to organize elements in a frame.

        Components are reusable elements that you can create once and then use in multiple places.

        Instances are copies of components that you can place in your design. You can make 
        changes to an instance without affecting the original component.
        """
        elements = []

        def traverse(node):
            if 'children' in node:
                for child in node['children']:
                    traverse(child)
            else:
                elements.append(node)

        for node in self.get_file_data()['document']['children']:
            traverse(node)

        return elements

# Main entry point for simple testing / showing usage
if __name__ == "__main__":

    # Load keys from keys.json and create a FigmaFile object to access a specific file
    keys = utils.load_keys()
    figma_file = FigmaFile(
        keys["figma-access-token"], 
        keys["figma-file-id"]
    )

    # Retrive all the elements and print their names (non unique) and ids (unique)
    elements = figma_file.get_all_elements()
    print(f"Found {len(elements)} elements:")
    for element in elements:
        print(f"\t{element['name']} ({element['id']})")
