import asyncclick as click
from aiohttp import ClientSession
from typing import Optional, BinaryIO
import typer


async def endpoint_hit(domain):
    async with ClientSession() as session:
        try:
            async with session.get(domain) as resp:
                return resp
        except:
            return None


async def result_return(url):
    result = await endpoint_hit(url)
    try:
        if result.status == 200:
            click.echo(click.style(f"FOUND {url}  STATUS CODE: {result.status}", fg='green'))
        else:
            click.echo(click.style(f"NOT FOUND {url}  STATUS CODE: {result.status}", fg='yellow'))
    except:
        click.echo(click.style(f"FAILED: {url} doesn't exist!", fg='red'))


@click.command()
@click.option('--domain', type=click.STRING, required=False)
@click.option('--protocol', type=click.STRING, required=False)
@click.option('--filename', type=click.Path(exists=True), required=True)
@click.option('--bulk', type=click.Path(exists=True), required=False)
async def touch(
        filename: BinaryIO, bulk: Optional[BinaryIO],
        protocol: typer.Argument("https"), domain: Optional[str] = None
):
    with open(filename) as f:
        protocols = protocol.split(",")
        subdomains = f.readlines()
        if bulk is None:
            for i in subdomains:
                for p in protocols:
                    fix_url = f"{p}://{i.strip()}.{domain}"
                    await result_return(fix_url)
        else:
            with open(bulk) as b:
                domain_list = b.readlines()
                for domain in domain_list:
                    for protocol in protocols:
                        for subdomain in subdomains:
                            fix_url = f"{protocol}://{subdomain.strip()}.{domain.strip()}"
                            await result_return(fix_url)


if __name__ == '__main__':
    touch(_anyio_backend="asyncio")
