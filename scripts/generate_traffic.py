#!/usr/bin/env python3
import argparse
import asyncio
import logging
import random

import aiohttp

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
log = logging.getLogger('generate_traffic')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parallel', type=int, default=15)
    parser.add_argument('-n', '--num-queries', type=int, default=10000)
    return parser.parse_args()


def generate_ackermann():
    return f'http://localhost:8000/ackermann/{random.randint(0, 3)}/{random.randint(0, 4)}/'


def generate_factorial():
    return f'http://localhost:8000/factorial/{random.randint(0, 400)}/'


def generate_fibonacci():
    return f'http://localhost:8000/fibonacci/{random.randint(0, 400)}/'


generators = [generate_ackermann, generate_factorial, generate_fibonacci]


async def generate_request(sem, session):
    query = random.choice(generators)()
    async with sem:
        await session.get(query)


async def generate_traffic(args):
    sem = asyncio.Semaphore(args.parallel)
    async with aiohttp.ClientSession() as session:
        requests = [generate_request(sem, session) for x in range(args.num_queries)]
        resp = await asyncio.gather(*requests)
        print(f'Number of queries done: {len(resp)}')


def main():
    args = parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_traffic(args))


if __name__ == '__main__':
    main()
