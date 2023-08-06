import os
from kmmate.utils.files import replace_in_file


class FrameworkUtils(object):

    def __init__(self, project_path: str, package_name: str):
        self.project_path = project_path
        self.package_name = package_name


    def rename_framework(self, new_name: str):
        file_path = os.path.join(self.project_path, 'shared', 'build.gradle.kts')
        replace_in_file(file_path, '"shared"', f'"{new_name}"')
        self.__rename_shared_folder(new_name)
        self.__rename_sdk_file(new_name)
        self.__rename_ios_import(new_name)
        

    def __rename_shared_folder(self, new_name: str):
        dir_path = os.path.join(self.project_path, 'shared')
        to_dir = os.path.join(self.project_path, new_name)
        os.rename(dir_path, to_dir)

        # Rename import local module
        replace_in_file(os.path.join(self.project_path, 'settings.gradle.kts'), ':shared', f':{new_name}')
        # Rename import local module in androidApp dir
        replace_in_file(os.path.join(self.project_path, 'androidApp/build.gradle.kts'), ':shared', f':{new_name}')


    def __rename_sdk_file(self, new_name: str):
        dir_to_sdk_file = os.path.join(
            self.project_path,
            new_name,
            'src/commonMain/kotlin',
            self.package_name.replace('.', '/')
        ) 
        file_path = os.path.join(dir_to_sdk_file, 'SharedSdk.kt')
        new_file_path = os.path.join(dir_to_sdk_file, f'{new_name}.kt')

        # Rename file
        os.rename(file_path, new_file_path)

        # Rename object name
        replace_in_file(new_file_path, 'object SharedSdk', f'object {new_name}')
        
    
    def __rename_ios_import(self, new_name: str):
        ios_path = os.path.join(self.project_path, 'iosApp') 
        
        for root, _, files in os.walk(ios_path):
            if len(files) == 0:
                continue

            for file in files:
                if file.endswith('.swift'):
                    file_path = os.path.join(root, file)
                    replace_in_file(file_path, 'import shared', f'import {new_name}')

