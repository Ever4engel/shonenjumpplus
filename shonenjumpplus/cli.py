import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('cid')
@click.option('-u', '--username', required=True)
@click.option('-p', '--password', required=True)
def download(cid, username, password):
    print('hello world')


def main():
    cli()


if __name__ == '__main__':
    main()
