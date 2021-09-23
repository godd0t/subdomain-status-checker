import asyncclick as click
from aiohttp import ClientSession


async def endpoint_hit(domain):
    async with ClientSession() as session:
        try:
            async with session.get(domain) as resp:
                return resp
        except:
            return None


@click.command()
@click.option('--domain', type=click.STRING)
@click.option('--protocol', type=click.STRING)
@click.option('--filename', type=click.Path(exists=True))
async def touch(domain, protocol, filename):
    with open(filename) as f:
        protocols = protocol.split(",")
        subdomains = f.read()
        formatted_subdomains = subdomains.split(",")
        for i in formatted_subdomains:
            for p in protocols:
                fix_url = f"{p}://{i.strip()}.{domain}"
                result = await endpoint_hit(fix_url)
                try:
                    if result.status == 200:
                        click.echo(click.style(f"FOUND {fix_url}  STATUS CODE: {result.status}", fg='green'))
                    else:
                        click.echo(click.style(f"NOT FOUND {fix_url}  STATUS CODE: {result.status}", fg='yellow'))
                except:
                    click.echo(click.style(f"FAILED: {fix_url} doesn't exist!", fg='red'))


if __name__ == '__main__':
    touch(_anyio_backend="asyncio")
