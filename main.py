import json
import click

def get_config(is_development):

    if is_development:
       path="devconfig.json"
    else:
       path="~/.config.pdf_collections.json"

    #open(path, "w")

    return {
        "collections": [
            {
                "name": "forskning",
                "folder": "~/Documents/skole/kristiania/6_semester/bachelor/forskning"
            }
        ]
    }
   # try:
   #     with open(path, "r") as file:
   #         json_string = file.read()
   #     config = json.loads(json_string)
   #     print(config)
   # except IOError:
   #     print("io eror caught :)")

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
        click.echo("- " + name)
@main.command()
def add():
    click.echo("add directory")

@main.command()
def open():
    click.echo("select one of possible pdfs in selected")

if __name__ == "__main__":
    main(obj={})
