import rich_click as click
from fusion.commands import scan, imp, find, export  # sub-commands

@click.group()
def cli():
    """Fusion – correlate Nmap & SpiderFoot intelligence."""

cli.add_command(scan.cli,  name="scan")
cli.add_command(imp.cli,   name="import")
cli.add_command(find.cli,  name="find")
cli.add_command(export.cli,name="export")

if __name__ == "__main__":
    cli()

