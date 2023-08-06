import click

from telerdac.const.click_setting import CONTEXT_SETTINGS
from telerdac.cmd.cmd import device_cmd, license_cmd


@click.group()
def cli():
    pass


@cli.command('device', short_help='device infomation', context_settings=CONTEXT_SETTINGS)
@click.option('--output', '-o', type=str, default='', help='Output hardware information to a file, specify the file path')
def device(output):
    device_cmd(output)


@cli.command('license', short_help='license operation, support gen for license generation and check for license file check', context_settings=CONTEXT_SETTINGS)
@click.argument('operation')
@click.option('--input', '-i', type=str, default='', help='Input license info file or license file')
@click.option('--privkey_path', '-priv', type=str, default='', help='private key path')
@click.option('--pubkey_path', '-pub', type=str, default='', help='public key path')
@click.option('--output', '-o', type=str, default='./license.lic', help='Output license flie path')
def license(operation, input, privkey_path, pubkey_path, output):
    license_cmd(operation, input, privkey_path, pubkey_path, output)
