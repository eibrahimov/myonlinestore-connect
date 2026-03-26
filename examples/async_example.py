"""Async usage example for the MyOnlineStore Connect API client."""

import asyncio
import os

from myonlinestore import ConnectClient
from myonlinestore.pagination import aiterate_all


async def main():
    async with ConnectClient(
        store_token=os.environ["MOS_STORE_TOKEN"],
        partner_token=os.environ.get("MOS_PARTNER_TOKEN"),
    ) as client:

        # Fetch articles and orders concurrently
        articles_task = asyncio.create_task(client.articles.alist(limit=50))
        orders_task = asyncio.create_task(client.orders.alist(limit=50))

        articles, orders = await asyncio.gather(articles_task, orders_task)

        print(f"Fetched {len(articles.items)} articles and {len(orders.items)} orders")

        # Async iteration through all pages
        count = 0
        async for article in aiterate_all(client.articles.alist, page_size=100):
            count += 1
        print(f"Total articles iterated: {count}")


if __name__ == "__main__":
    asyncio.run(main())
