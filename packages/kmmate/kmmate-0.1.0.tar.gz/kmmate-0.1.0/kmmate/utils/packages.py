import os
from rich import print
from rich.console import Console
from kmmate.utils.files import replace_in_file

# 1. Check if kmm project in current folder
# 2. If yes - okey, if no - throw the exception print
# 3. Rename package in settings.gradle.kts
# 4. Rename package in shared/build.gradle.kts
# 5. Rename package dirs in commonMain, androidMain, iosMain (kotlin/)

class PackageUtils(object):
    
    def __init__(self, project_path: str, project_name: str, package_name: str):
        self.project_path = project_path
        self.project_name = project_name
        self.package_name = package_name
    
    
    def rename_packages(self):
        if not os.path.exists(f'{self.project_path}/build.gradle.kts'):
            print('[bold red]Gradle file is not found!')
            return

        console = Console()
        
        with console.status('[bold green]Renaming package[/bold green] in [bold]settings.gradle.kts[/bold] and [bold]shared/build.gradle.kts[/bold]') as s:
            self.__rename_project_name()
            print(s.status)
            
        with console.status('[bold green]Renaming package directories') as s:
            self.__rename_dirs('shared/src/commonMain/kotlin')
            self.__rename_dirs('shared/src/androidMain/kotlin')
            self.__rename_dirs('shared/src/iosMain/kotlin')
            print(s.status)
        
        with console.status('[bold green]Renaming package definition for each .kt file') as s:
            self.__rename_packages_in_files(os.path.join(self.project_path, 'shared/src/commonMain/kotlin'))
            self.__rename_packages_in_files(os.path.join(self.project_path, 'shared/src/androidMain/kotlin'))
            self.__rename_packages_in_files(os.path.join(self.project_path, 'shared/src/iosMain/kotlin'))
            print(s.status)
            
        
    def __rename_project_name(self):
        file = f'{self.project_path}/settings.gradle.kts'
        shared_build_file = f'{self.project_path}/shared/build.gradle.kts'
        
        # Renames in settings.gradle.kts
        replace_in_file(file, 'KMM_Template', self.project_name)

        # Rename in shared/build.gradle.kts
        replace_in_file(shared_build_file, 'com.sharpyx.kmm_template', f'com.example.{self.project_name}')

    
    def __rename_dirs(self, in_path: str):
        # common_main_dir = os.path.join(self.project_path, 'shared/src/commonMain/kotlin')
        common_main_dir = os.path.join(self.project_path, in_path)
        
        package_dirs = self.package_name.split('.') # com, example, project

        current_dir = common_main_dir

        for index, dir in enumerate(package_dirs):
            if len(package_dirs) == index:
                break
            
            dirs = os.listdir(current_dir)
            
            fromdir = os.path.join(current_dir, dirs[0])
            todir = os.path.join(current_dir, dir)
            
            os.rename(fromdir, todir)

            current_dir = todir

    
    def __rename_packages_in_files(self, root_dir: str):
        for root, _, files in os.walk(root_dir):
            if len(files) == 0:
                continue

            for file in files:
                if file.endswith('.kt'):
                    file_path = os.path.join(root, file)
                    replace_in_file(file_path, 'com.sharpyx.kmm_template', self.package_name)

