from importlib.metadata import version, PackageNotFoundError
from requests.exceptions import ConnectionError
import click
import sys
import requests
import time
import os


try:
    __version__ = version("sleakops-cli")
except PackageNotFoundError:
    # package is not installed
    pass

API_URL = os.environ.get("SLEAKOPS_API_URL", "https://api.sleakops.com/api/")

MAX_POLLING = int(os.environ.get("MAX_POLLING", 1000))
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 10))


def action(path, data, headers, wait):
    try:
        response = requests.post(path, json=data, headers=headers)
    except ConnectionError:
        click.echo(f"Could not reach {path}")
        sys.exit(1)
    if not response.ok:
        result_message = response.json() if response.status_code == 400 else response.reason
        click.echo(f"Something went wrong: {result_message}")  # api key wrong
        sys.exit(1)
    elif wait:
        created = False
        retries = 0
        id = response.json()["id"]
        while not created and retries < MAX_POLLING:
            try:
                state_response = requests.get(f"{path}{id}", headers=headers)
            except ConnectionError:
                click.echo(f"Could not reach {path}")
                sys.exit(1)
            if state_response.ok:
                state = state_response.json()["state"]
                if state == "initial":
                    click.echo("Build queued...")
                elif state == "creating":
                    click.echo("Building project...")
                elif state == "error":
                    click.echo(
                        f"Something went wrong: {state_response.json()['errors']}"
                    )
                    sys.exit(1)
                elif state == "created":
                    click.echo("Image builded correctly!")
                    created = True
                    sys.exit(0)
            retries += 1
            time.sleep(SLEEP_TIME)
    sys.exit(0)


@click.group()
def cli_build():
    pass


@click.group()
def cli_deploy():
    pass


@cli_build.command()
@click.option("-p", "--project", required=True, help="Project name.")
@click.option("-b", "--branch", required=True, help="Repository branch.")
@click.option("-c", "--commit", show_default=True, help="Commit.")
@click.option("-t", "--tag", help="Tag for the image")
@click.option(
    "-w",
    "--wait",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run build and wait for it to finish.",
)
@click.option(
    "-k",
    "--key",
    envvar="SLEAKOPS_KEY",
    help="Sleakops access key. It can be used with this option or get from SLEAKOPS_KEY environment var.",
)
def build(project, branch, commit, tag, wait, key):
    path = f"{API_URL}cli-build/"
    headers = {"Authorization": f"Api-Key {key}"}

    data = {
        "project_env": {
            "project_name": project,
        },
        "branch": branch,
    }
    data.update({"commit": commit}) if commit else None
    data.update({"tag": tag}) if tag else None

    action(path, data, headers, wait)


@cli_deploy.command()
@click.option("-p", "--project", required=True, help="Project name.")
@click.option("-e", "--env", required=True, help="Environment.")
@click.option("-b", "--build", required=False, help="Build id.")
@click.option("-t", "--image", default="latest", show_default=True, help="Image tag.")
@click.option(
    "-w",
    "--wait",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run build and wait for it to finish.",
)
@click.option(
    "-k",
    "--key",
    envvar="SLEAKOPS_KEY",
    help="Sleakops access key. It can be used with this option or get from SLEAKOPS_KEY environment var.",
)
def deploy(project, env, build, image, wait, key):
    path = f"{API_URL}cli-deployment/"
    headers = {"Authorization": f"Api-Key {key}"}

    data = {
        "project_env": {
            "project_name": project,
            "environment_name": env,
        }
    }
    data.update({"build": build}) if build else None
    data.update({"image": image}) if image else None

    action(path, data, headers, wait)


cli = click.CommandCollection(sources=[cli_build, cli_deploy])

if __name__ == "__main__":
    cli()
