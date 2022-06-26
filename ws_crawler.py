import argparse
import os
import pathlib

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

from whoscores.spiders.WS_spider import WSSpider


@defer.inlineCallbacks
def football_transfer_crawl(output_path):
    configure_logging()
    settings = get_project_settings()
    # url = 'https://www.transfermarkt.com/uefa/klubrangliste/statistik/stat'
    url = 'https://www.footballtransfers.com/en/transfers/confirmed'
    out_file_path = os.path.join(output_path, 'footballtransfer')
    settings['FEEDS'] = {
        f'{out_file_path}_leagues.json': {
            'format': 'json',
            'overwrite': True,
        }
    }
    runner = CrawlerRunner(settings)
    yield runner.crawl(WSSpider, url)
    reactor.stop()


def main(args) -> None:
    output_path = args.output_folder
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
    football_transfer_crawl(output_path)
    reactor.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--output_folder',
        type=str,
        required=False,
        default='footballtransfer',
        help='Path for output folder',
    )
    args = parser.parse_args()
    main(args)
