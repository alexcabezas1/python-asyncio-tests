import threading
from urllib.request import urlopen
import time


messages = []

def count_words(content):
    return len(str(content).split())


def download_content(url, url_position):
    request = urlopen(url)
    file_size = request.length    

    content = []
    while True:
        chunk = request.read(1024) # release the GIL
        if not chunk:
            break
        else:
            content.append(str(chunk))

    count = count_words("".join(content))
    message = "A content from the url #{} '{}' was downloaded".format(url_position, url)
    message += "\n>> File size: {}. It has {} words".format(file_size, count)
    messages.append(message)

    request.close()
    

def main(urls):
    threads = []
    for index, url in enumerate(urls):
        t = threading.Thread(target=download_content, args=(url, index))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    for msg in messages:
        print()
        print(msg)


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
    main(urls)
    end = time.time()
    print("\nExecution Time: {}".format(end - start))

