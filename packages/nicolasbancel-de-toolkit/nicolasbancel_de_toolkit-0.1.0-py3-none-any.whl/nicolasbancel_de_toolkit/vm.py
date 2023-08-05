import click
import subprocess


@click.command()
def start():
    """Start your vm"""
    subprocess.run(
        [
            "gcloud",
            "compute",
            "instances",
            "start",
            "--zone",
            "europe-west1-b",
            "lewagon-data-eng-vm-nicolasbancel",
        ]
    )


@click.command()
def stop():
    """Stop your vm"""
    subprocess.run(
        [
            "gcloud",
            "compute",
            "instances",
            "stop",
            "--zone",
            "europe-west1-b",
            "lewagon-data-eng-vm-nicolasbancel",
        ]
    )


@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/nicolasbancel/folder"""
    subprocess.run(
        [
            "code",
            "--folder-uri",
            "vscode-remote://vscode-remote://ssh-remote+nicolas.bancel.lewagon@34.140.177.24/home/nicolas.bancel.lewagon/code/",
        ]
    )


if __name__ == "__main__":
    connect()
