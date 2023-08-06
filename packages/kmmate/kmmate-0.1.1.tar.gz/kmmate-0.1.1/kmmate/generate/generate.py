import typer

app = typer.Typer()

# TODO: Incapsulate docstrings to another file

@app.command(help='Generates a component interface with {name} and implementation for it. Automatically adds Childs to root component')
def component(name: str):
    print(f'Component {name} is successfully generated!')

@app.command(help='Generates a Ktofit API for feature')
def api(name: str):
    print(f'Ktofit API for {name} component is successfully generated!')
