from office365.sharepoint.client_context import ClientContext , ClientCredential
import os

class SharePoint:

    def __init__(self, client_id, client_secret, sharepoint_url, sharepoint_site, root_folder) -> None:
        client_credentials = ClientCredential(client_id, client_secret)
        self.ctx = ClientContext(sharepoint_site).with_credentials(client_credentials)
        self.sp_url = sharepoint_url
        self.sp_site = sharepoint_site
        self.root_folder = root_folder
        self.dict_names = {}
        self.dict_path = {}
        self.file_list = []

    def _get_list_for_map(self, folder):
        files = self.ctx.web.get_folder_by_server_relative_url(folder).files
        folders = self.ctx.web.get_folder_by_server_relative_url(folder).folders
        self.ctx.load(folders)
        self.ctx.load(files)
        self.ctx.execute_query()
        files_list= []      
        folders_list = []

        for folder in folders:
            folder_name = folder.properties['Name']
            if folder_name != 'Forms':
                fold_nombre_path = (folder.properties['Name'], folder.properties['ServerRelativeUrl'])
                folders_list.append(fold_nombre_path)

        for file in files:
            file_nombre_path = (file.properties['Name'], file.properties['ServerRelativeUrl'])
            files_list.append(file_nombre_path)

        return folders_list, files_list
        
    def _map_dicts(self, folder, dict_names={}, dict_path={}):
        folders_list, files_list = self._get_list_for_map(folder)
        for name, path in folders_list:
            dict_names[name] = {}
            dict_path[path] = {}
        if files_list:
            dict_names['Archivos'] = list(zip(*files_list))[0]
            dict_path['Archivos'] = list(zip(*files_list))[1]
        if folders_list:
            for name, path in folders_list:
                self._map_dicts(path,dict_names[name], dict_path[path])
        return dict_names, dict_path
    
    def _get_file_list(self, folder):
        files = self.ctx.web.get_folder_by_server_relative_url(folder).files
        folders = self.ctx.web.get_folder_by_server_relative_url(folder).folders
        self.ctx.load(folders)
        self.ctx.load(files)
        self.ctx.execute_query()
        for file in files:
            self.file_list.append(
                    # tupla de paths para descarga y subida
                    (
                    file.properties['ServerRelativeUrl'], #path para SharePoint
                    file.properties['ServerRelativeUrl'].replace('/' + os.path.relpath(self.sp_site, self.sp_url).replace(os.sep, '/') + '/','') # path para Blob Storage
                    )
            )
        if folders:
            for folder in folders:
                if folder.properties['Name'] != 'Forms':
                    self._get_file_list(folder.properties['ServerRelativeUrl'])

    def run(self, map_dicts=False):
        if map_dicts:
            self.dict_names, self.dict_path = self._map_dicts(self.root_folder)
        self._get_file_list(self.root_folder)

    def get_file(self, file):
        return self.ctx.web.get_file_by_server_relative_path(file).open_binary_stream().execute_query().value
