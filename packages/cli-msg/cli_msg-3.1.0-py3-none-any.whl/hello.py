import click

from .utils.messages import print_hello, print_world, print_hello_world

@click.command()
@click.option("-h", "--hello", is_flag=True, help="Print Hello")
@click.option("-w", "--world", is_flag=True, help="Print World")
@click.option("-hw", "--hello_world", is_flag=True, help="Print Hello World")
def cli(hello: bool, world: bool, hello_world: bool) -> None:
    if hello:
        print_hello()
    elif world:
        print_world()
    elif hello_world:
        print_hello_world()

if __name__ == "__main__":
    cli()