import json
import click


def get_config_path(is_development):
    if is_development:
       path="devconfig.json"
    else:
       path="~/.config.pdf_collections.json"

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
    with click.open_file(path, "w") as f:
        json.dump(config, f)


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
def open():
    click.echo("select one of possible pdfs in selected")

if __name__ == "__main__":
    main(obj={})
