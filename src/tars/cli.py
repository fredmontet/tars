import click
from importlib import import_module, util

from tars import Tars


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Tars(environment='server')


@cli.command()
@click.option('--paths', '-p', default=None, multiple=True)
@click.option('--frequency', '-f', default='00:01:00')
@click.option('--duration', '-d', default=None)
@click.pass_obj
def start(tars, paths, frequency, duration):
    # load strategy from path
    for p in paths:
        spec = util.spec_from_file_location('module', p)
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)
        strategy = module.func()
        tars.load(strategy)
    # start tars
    tars.start(frequency, duration)


@cli.command()
@click.pass_obj
def stop(tars):
    tars.stop()


if __name__ == '__main__':
    cli()
