import typer
import os
from fastmvc import __version__
from fastmvc.generator import build_base, gen_scaffold, gen_authlib
from typing import List
import fastmvc.utilities as utils

app = typer.Typer()


@app.command()
def version():
    """ show current version of FastMVC"""
    typer.echo(f"FastMVC {__version__}")


def __choose_platform(param_platform):
    plats = utils.platforms()
    if param_platform:
        try:
            selected_platform = utils.Platform[param_platform]
        except:
            selected_platform = None
    else:
        typer.secho('\n'.join(f"[{k}] {v.name}" for k, v in plats.items()))
        selected_platform = typer.prompt("Which platform would you like to build for?")
        selected_platform = plats.get(selected_platform)
    if not selected_platform:
        typer.secho(f"Please choose a valid Platform. {list(plats.values())}", fg='red')
    return selected_platform


@app.command()
def new(project: str, platform: str or None = None):
    """ create a new project """
    plat = __choose_platform(platform)
    if not plat:
        return
    
    new_folder = os.path.join(os.curdir, project)
    try:      
        typer.secho(f"\nBuilding new project: {project}\n", fg='green')
        build_base(new_folder, project, plat)
        typer.echo(f"\n{project} was created.\n")
    except FileExistsError:
        typer.secho(f"'{project}' already exists in this folder.\n", fg='red')
    

@app.command()
def server():
    """ run the app locally """
    utils.run_server()


@app.command()
def s():
    """ alias for 'server' """
    server()


@app.command()
def scaffold(obj: str, attributes: List[str]):
    """ create a router and views for a described object """
    typer.secho(f"\nScaffolding views and router for: {obj}\n", fg='green')
    gen_scaffold(os.curdir, obj, attributes)
    typer.echo(f"\n{obj} was created.\n")


@app.command()
def auth():
    """ generate authorization framework for users """
    typer.secho(f"\nGenerating views and router for: User\n", fg='green')
    gen_authlib(os.curdir)
    typer.echo(f"\nAuth was created.\n")


# @app.command()
# def set_project_key(project_key: str):
#     """ set your development project key for Deta for faster builds """
#     utils.set_project_key(project_key)
#     typer.secho("Project Key successfully set.", fg='green')


# @app.command()
# def clear_project_key():
#     """ clear your Deta development project key """
#     utils.clear_project_key()
#     typer.secho("Project Key successfully cleared.", fg='green')


@app.command()
def view_config():
    """ view your development configurations """
    conf = utils.config()
    typer.echo(conf)
