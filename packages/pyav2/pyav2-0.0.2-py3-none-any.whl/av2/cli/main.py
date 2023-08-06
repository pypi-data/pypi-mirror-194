from typing import List, Dict
from concurrent.futures.thread import ThreadPoolExecutor
import click
from rich.console import Console
from rich import print

console = Console()


@click.group()
def av2():
    pass


@av2.command()
@click.option('-i', '--source_video', help='视频在硬盘中的路径')
def info(source_video: str = ...):
    """ view all container """
    import av2
    import json
    import yaml

    with av2.open(source_video) as file:
        print(file.dict())
        print(json.dumps(file.dict(), indent=4))
        print(yaml.dump(file.dict(), indent=4))


@av2.command()
@click.option('-i', '--source_video', help='视频在硬盘中的路径')
def rinfo(source_video: str = ...):
    """ view all container """
    import av

    with av.open(source_video, options={"time_base": "1000"}) as file:
        print(type(file.streams))

        print(dir(file.streams))

        for d in dir(file.streams):
            print(d, ': ', getattr(file.streams, d), '    ',
                  'type:', type(getattr(file.streams, d)))
            print('----------------------')

        videos = file.streams.video
        print(videos)
        print(type(videos))

        print('------------------------------------------------------------------')
        print('------------------------------------------------------------------')

        for video in videos:
            print(video)
            print(type(video))
            print('=====================')

            for v in dir(video):
                print(v, ': ', getattr(video, v), '    ',
                      'type:', type(getattr(video, v)))
                print('---------------------->')

            print('------------------------------------------------------------------')
            print('------------------------------------------------------------------')
            print('------------------------------------------------------------------')
            print('------------------------------------------------------------------')
            
            cc=video.codec_context
            
            for c in dir(cc):
                print(c, ': ', getattr(cc, c), '    ',
                      'type:', type(getattr(cc, c)))
                print('cc ----------------------> c')

        # print(dir(file))
        # print(file.__dict__())
        # print(type(file.metadata))
        # print(file.metadata)


cli = click.CommandCollection(sources=[av2])

if __name__ == '__main__':
    cli()
