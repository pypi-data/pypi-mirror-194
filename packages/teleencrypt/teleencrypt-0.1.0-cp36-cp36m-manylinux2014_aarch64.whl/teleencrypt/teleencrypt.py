import click

from teleencrypt.const.click_setting import CONTEXT_SETTINGS
from teleencrypt.utils.encrypt_utils import operate_model, encrypt_code


@click.group()
def cli():
    pass


@cli.command('code', short_help='Encrypt code', context_settings=CONTEXT_SETTINGS)
@click.option('--file', '-f', type=str, help='configuration file')
def code(file):
    encrypt_code(file)


@cli.command('model', short_help='Encrypt or decrypt model, support operation encrypt and decrypt', context_settings=CONTEXT_SETTINGS)
@click.argument('operation')
@click.option('--input', '-i', type=str, help='model file path')
@click.option('--pubkey_path', '-pub', type=str, help='public key file')
@click.option('--output', '-o', type=str, help='encrypted model file path')
def model(operation, input, pubkey_path, output):
    operate_model(operation, input, pubkey_path, output)
