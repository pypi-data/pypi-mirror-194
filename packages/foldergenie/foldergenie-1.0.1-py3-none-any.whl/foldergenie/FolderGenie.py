import sys
import os
from pathlib import Path

class FolderGenie:
    def __init__(self, filename):
        self.filename = filename
        self.tree = {}
        self.__create_folder_tree()
        
    def create_directories(self, node, path):
        # skip root
        if node['name'] != 'root':
        # Create the path to the directory
            path = os.path.join(path, node['name'])
            current_directory = Path(path)
        
        # Create a file if the node has an extension, else create a directory
            if node['is_file']:
                current_directory.touch()
            else:
                current_directory.mkdir()

        # If the node has no children, return
        if not node['children']:
            return

        # Recursively create directories for all children nodes
        for child in node['children']:
            self.create_directories(child, path)
        
    def __create_folder_tree(self):
        # Open the file and read its contents
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        
        # Create a dictionary of nodes and their indentation level
        nodes = [{'name': line.strip(), 'indent': len(line) - len(line.lstrip()), 'is_file': '.' in line, 'children': []} for line in lines]
        
        # Create the tree structure of nodes
        stack = []
        root_node = {'name': 'root', 'indent': -1, 'is_file': False, 'children': []}
        stack.append(root_node)

        for node in nodes:
            while node['indent'] <= stack[-1]['indent']:
                stack.pop()

            stack[-1]['children'].append(node)
            stack.append(node)

        self.tree = root_node
        
    def generate_folders(self):
        self.create_directories(self.tree, os.getcwd())

if __name__ == "__main__":
    # Check for the correct number of arguments
    if len(sys.argv) != 2:
        print('Incorrect number of arguments')
        print('Syntax: python3 foldergenie.py path/to/your/input_file')
        sys.exit()

    # Generate the folders using the input file
    genie = FolderGenie(sys.argv[1])
    genie.generate_folders()
