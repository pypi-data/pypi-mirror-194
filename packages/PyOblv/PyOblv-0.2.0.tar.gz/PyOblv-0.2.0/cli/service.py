import json

import typer

from . import utils

app = typer.Typer()


@app.command(help="To create a new service")
def create(repo_owner: str = typer.Argument(..., help=("Repository Owner")), repo_name: str = typer.Argument(...,help=("Repository Name")), ref: str = typer.Argument(..., help=("Service ref name")), tag : bool = typer.Option(False, "--tag",help="If provided, the ref is considered to be a tag on repository"), service_file : str = typer.Option(None,help="Service yaml file in json format. Not allowed with --tag")):
    try:
        client = utils.read_credentials()
        if tag:
            client.add_service(repo_owner=repo_owner,repo_name=repo_name,ref=ref,ref_type="tag")
        else:
            args = {}
            if service_file!=None:
                with open(service_file,"r") as f:
                    args = json.load(f)
            client.add_service(repo_owner=repo_owner,repo_name=repo_name,ref=ref, data=args)
    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    except Exception as e:
        print(e)
    else:
        print("Successfully added the service")

@app.command(help="To remove an existing service")
def remove(repo_owner: str = typer.Argument(..., help=("Repository Owner")), repo_name: str = typer.Argument(...,help=("Repository Name")), ref: str = typer.Argument(..., help=("Service ref name")), tag : bool = typer.Option(False, "--tag", help="If provided, the ref is considered to be a tag on repository")):
    try:
        client = utils.read_credentials()
        if tag:
            client.remove_service(repo_owner=repo_owner,repo_name=repo_name,ref=ref,ref_type="tag")
        else:
            client.remove_service(repo_owner=repo_owner,repo_name=repo_name,ref=ref)
    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    except Exception as e:
        print(e)
    else:
        print("Successfully removed the service")

@app.command(help="To fetch user's services list")
def fetch():
    try:
        client = utils.read_credentials()
        print(client.user_services())
    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    except Exception as e:
        print(e)

@app.command(help="To updates user's service")
def update(repo_owner: str = typer.Argument(..., help=("Repository Owner")), repo_name: str = typer.Argument(...,help=("Repository Name")), ref: str = typer.Argument(..., help=("Service ref name")), tag : bool = typer.Option(False, "--tag", help="If provided, the ref is considered to be a tag on repository"), service_file : str = typer.Option(None,help="Service yaml file in json format. Not allowed with --tag")):
    try:
        client = utils.read_credentials()
        if tag:
            client.update_service(repo_owner=repo_owner,repo_name=repo_name,ref=ref,ref_type="tag")
        else:
            args = {}
            if service_file!=None:
                with open(service_file,"r") as f:
                    args = json.load(f)
            client.update_service(repo_owner=repo_owner,repo_name=repo_name,ref=ref, data=args)
    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    except Exception as e:
        print(e)
    else:
        print("Successfully updated the service")
