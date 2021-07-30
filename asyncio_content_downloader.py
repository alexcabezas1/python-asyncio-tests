import asyncio
import aiohttp
from urllib.request import urlopen
import time


async def count_words(content):
    return len(str(content).split())


async def download_content_blocking(url, url_position):
    request = urlopen(url)
    file_size = request.length    

    content = []
    while True:
        chunk = request.read(1024) # blocking code
        if not chunk:
            break
        else:
            content.append(str(chunk))

    count = await count_words("".join(content))
    result = "A content from the url #{} '{}' was downloaded".format(url_position, url)
    result += "\n>> File size: {}. It has {} words".format(file_size, count)
    
    return result


async def download_content_nonblocking(url, url_position):
    file_size = 0

    content = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            file_size = response.headers.get('CONTENT-LENGTH')
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                else:
                    content.append(str(chunk))

    count = await count_words("".join(content))
    result = "A content from the url #{} '{}' was downloaded".format(url_position, url)
    result += "\n>> File size: {}. It has {} words".format(file_size, count)
    
    return result


async def main(urls):
    downloader = download_content_nonblocking

    tasks = [downloader(url, index) for index, url in enumerate(urls)]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print()
        print(result)


if __name__ == '__main__':
    urls = [
        'http://www.gutenberg.org/files/58152/58152-0.txt',
        'https://www.gutenberg.org/files/58145/58145-0.txt',
        'https://www.gutenberg.org/files/58140/58140-0.txt',
        'http://www.gutenberg.org/cache/epub/25449/pg25449.txt',
        'https://www.gutenberg.org/files/24518/24518-0.txt',
        'http://www.gutenberg.org/cache/epub/14557/pg14557.txt',
        'http://www.gutenberg.org/cache/epub/32950/pg32950.txt'
    ]

    start = time.time()  
    
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(urls))
    finally:
        event_loop.close()

    end = time.time()
    print("\nExecution Time: {}".format(end - start))
