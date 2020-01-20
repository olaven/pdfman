#!/usr/bin/env python3

import json, subprocess, os
from pathlib import Path
import click


def get_config_path(is_development):
    if is_development:
       path="devconfig.json"
    else:
       path= str(Path.home()) + "/.config.pdf_collections.json"

    return path

def get_config(is_development):

    path = get_config_path(is_development)
    try:

        with click.open_file(path, "r") as f:
            json_string = f.read()
        config = json.loads(json_string)
    except FileNotFoundError:
        config = {"collections": []}
        update_config(is_development, config)

    return config

def update_config(is_development, config):
    path = get_config_path(is_development)
    with click.open_file(path, "w+") as f:
        json.dump(config, f)

def get_pdfs(path):
    files = [file for file in os.scandir(path) if Path(file.path).suffix == ".pdf"]
    return files

def open_one(path, pdf_files):

    pdf_files.sort(key=lambda f: f.name)
    for index in range(0, len(pdf_files)):
        number = click.style(str(index), fg="blue")
        name = pdf_files[index].name
        click.echo(number + " - " + name)

    user_choice = click.prompt('Which one do you want to read?', type=int)

    try:
        selected_pdf = pdf_files[user_choice]
        os.system("open " + selected_pdf.path)
    except IndexError:
        click.echo(click.style("This number was not an option..", fg="red"))



def open_all(path, pdf_files):
    for pdf_file in pdf_files:
        os.system("open " + pdf_file.path)



@click.group()
@click.option('--development', 'development', flag_value=True, default=False)
@click.pass_context
def main(ctx, development):
    ctx.ensure_object(dict)
    ctx.obj['DEVELOPMENT'] = development

@main.command()
@click.pass_context
def list(ctx):

    config = get_config(is_development=ctx.obj["DEVELOPMENT"])

    click.echo(click.style("Added collections:", fg="green", bold=True))
    for collection in config.get("collections"):
        name = collection.get("name")
        path = collection.get("path")
        click.echo("- " + click.style(name, fg="blue") + " " + path)

@main.command()
@click.argument('name', type=click.STRING)
@click.argument('path', type=click.Path(exists=True))
@click.pass_context
def add(ctx, name, path):
    is_development = ctx.obj["DEVELOPMENT"]
    config = get_config(is_development)
    config.get("collections").append({
        "name": name,
        "path": path
    })
    update_config(is_development, config)

@main.command()
@click.argument("name", type=click.STRING)
@click.option("--all", "should_open_all", flag_value=True, default=False)
@click.pass_context
def open(ctx, name, should_open_all):

    is_development = ctx.obj["DEVELOPMENT"]
    config = get_config(is_development)

    for collection in config.get("collections"):
        if collection.get("name") == name:

            path = collection.get("path")
            pdf_files = get_pdfs(path)

            if should_open_all:
                open_all(path, pdf_files)
            else:
                open_one(path, pdf_files)
            return
    click.echo(click.style("Could not find this collection..", fg="yellow"))

@main.command()
@click.argument("pdfs", type=click.File(), nargs=-1)
@click.argument("name", type=click.STRING)
@click.pass_context
def move(ctx, pdfs, name):
    is_development = ctx.obj["DEVELOPMENT"]
    config = get_config(is_development)

    for collection in config.get("collections"):
        if collection.get("name") == name:

            path = collection.get("path")
            for pdf in pdfs:
                os.system("mv " + pdf.name + " " + path)
                click.echo(click.style(pdf.name + " moved", fg="green"))
            return
    click.echo(click.style("Could not find this collection..", fg="yellow"))

if __name__ == "__main__":
    main(obj={})
