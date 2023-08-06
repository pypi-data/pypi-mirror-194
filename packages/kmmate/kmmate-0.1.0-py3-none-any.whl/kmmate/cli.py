import os
import shutil
import typer
from kmmate.utils.framework import FrameworkUtils
from kmmate.utils.packages import PackageUtils
from kmmate.utils.sample import SampleUtils
from rich import print
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.padding import Padding
from kmmate import config

app = typer.Typer(
    name='kmmate',
    no_args_is_help=True
)

@app.command(
    name='new',
    short_help='Creates a new KMM project based on template with {name}.',
)
def new(name: str = typer.Argument('', help='Name of the project')):
    console = Console()
    
    current_dir = os.getcwd()
    project_name = ''
    project_package_name = ''
    project_with_sample = True

    if not name:
        project_name = Prompt.ask('What is project name? :sunglasses: ')
    else:
        project_name = name.split('/')[-1]

    print(Padding("", (0, 1)))
    project_package_name = Prompt.ask('Choose the package name :package: ')
    
    print(Padding("", (0, 1)))
    project_with_sample = Confirm.ask('Do you want to have sample of usage withing your project? :magnifying_glass_tilted_left:', default=True)
        
    print(Padding("", (0, 1)))
    new_name = Prompt.ask('You can optionally give a new name for your shared framework', default='shared')
    print(Padding("", (0, 1)))
    
    project_path = f'{current_dir}/{project_name}'
    
    # 1. Clonning the repo
    with console.status("[bold green]Clonning the repository...") as _:
        os.system(f'git clone --quiet {config.TEMPLATE_REPOSITORY} {project_name}')
        shutil.rmtree(f'{project_path}/.git')
        os.chdir(project_path)
        os.system('git init')

    
    # 2. Rename packages
    package_util = PackageUtils(
        project_path=project_path, 
        project_name=project_name,
        package_name=project_package_name
    )
    package_util.rename_packages()

    # 2.1. Rename the output framework name (default is shared)
    if new_name != 'shared':
        framework_util = FrameworkUtils(project_path, project_package_name)
        framework_util.rename_framework(new_name)

    # 3. If user do not want to have example, then delete sample files
    if not project_with_sample:
        sample_util = SampleUtils(project_path)
        sample_util.remove_sample()

    print(Padding("", (0, 1)))
    print(f'[bold green]Successfully create a project with name {project_name}! Happy codding!')

@app.callback()
def callback():
    pass

if __name__ == "__main__":
    app()
