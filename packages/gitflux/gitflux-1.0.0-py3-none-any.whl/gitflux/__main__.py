import json
import importlib
from pathlib import Path

import click
from gitflux.commands import command_group


@click.group(commands=command_group)
@click.version_option(message='%(version)s')
@click.option('--config-file', help='Path of configuration file.', type=click.Path(dir_okay=False), expose_value=True, is_eager=True, default=Path(Path.home(), '.gitfluxrc'))
@click.option('-p', '--provider', help='Git service provider.', type=click.Choice(['github', 'gitee']), required=False, default='github')
@click.pass_context
def cli(ctx: click.Context, config_file: Path, **options: dict):
    """A nested command-line utility that helps you manage repositories hosted on Git service providers."""

    ctx.ensure_object(dict)

    config_file = Path(config_file)

    if not config_file.is_file():
        raise FileNotFoundError(f'Configuration file "{config_file}" not found.')

    provider_module = importlib.import_module(f'gitflux.providers.{options["provider"]}')

    config = json.loads(config_file.read_text(encoding='utf-8'))
    ctx.obj['provider'] = provider_module.create_provider(config['providers'][options['provider']]['accessToken'])


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    cli()
