import time
import asyncio
import requests
import aiohttp
from asgiref import sync
from datetime import datetime


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"{func.__name__:<30} started")
        result = func(*args, **kwargs)
        duration = f"{func.__name__:<30} finished in {time.time() - start:.2f} seconds"
        print(duration)
        timed.durations.append(duration)
        return result

    return wrapper


timed.durations = []

# URL va headers
URL = "http://127.0.0.1:8000/posts/"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJNYXRuYXphcjA0IiwiZXhwIjoxNzQzNTkyNjc0fQ.49RI7dcoCfu_0YUyVI1LK9pNr0sdsBgxiamgsg-RD9I",
    "Accept": "application/json",
    "User-Agent": "IntelliJ HTTP Client/PyCharm 2024.3.3",
    "Accept-Encoding": "br, deflate, gzip, x-gzip",
}


@timed
def sync_requests_get_all(n_requests):
    session = requests.Session()
    results = []
    start_time = datetime.now()

    for i in range(n_requests):
        try:
            req_start = datetime.now()
            response = session.get(URL, headers=HEADERS)
            elapsed_time = (datetime.now() - req_start).total_seconds() * 1000
            results.append((response.status_code, elapsed_time))
        except requests.RequestException as e:
            print(f"So'rov #{i + 1} xatosi: {e}")
            results.append((None, None))

    total_time = (datetime.now() - start_time).total_seconds() * 1000
    statuses = [r[0] for r in results if r[0] is not None]
    times = [r[1] for r in results if r[1] is not None]

    print("\nStatistika (sync_requests):")
    print(f"Jami muvaffaqiyatli so'rovlar: {len(statuses)}")
    print(f"Umumiy vaqt: {total_time:.2f} ms")
    print(f"Ortacha vaqt: {sum(times) / len(times):.2f} ms")
    print(f"Maksimal vaqt: {max(times):.2f} ms")
    print(f"Minimal vaqt: {min(times):.2f} ms")


# 2. Requests async wrapper bilan
@timed
def async_requests_get_all(n_requests):
    session = requests.Session()

    def get(url):
        return session.get(url, headers=HEADERS)

    async_get = sync.sync_to_async(get)

    async def get_all():
        results = []
        start_time = datetime.now()

        tasks = []
        for i in range(n_requests):
            tasks.append(async_get(URL))

        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses, 1):
            elapsed_time = (
                (datetime.now() - start_time).total_seconds() * 1000 / n_requests
            )  # Taxminiy
            results.append((response.status_code, elapsed_time))

        total_time = (datetime.now() - start_time).total_seconds() * 1000
        statuses = [r[0] for r in results if r[0] is not None]
        times = [r[1] for r in results if r[1] is not None]

        print("\nStatistika (async_requests):")
        print(f"Jami muvaffaqiyatli so'rovlar: {len(statuses)}")
        print(f"Umumiy vaqt: {total_time:.2f} ms")
        print(f"Ortacha vaqt: {sum(times) / len(times):.2f} ms")
        print(f"Maksimal vaqt: {max(times):.2f} ms")
        print(f"Minimal vaqt: {min(times):.2f} ms")

        return results

    return sync.async_to_sync(get_all)()


# 3. To‘liq async aiohttp bilan
@timed
def async_aiohttp_get_all(n_requests):
    async def get_all():
        async with aiohttp.ClientSession() as session:

            async def fetch(i):
                try:
                    req_start = datetime.now()
                    async with session.get(URL, headers=HEADERS) as response:
                        elapsed_time = (
                            datetime.now() - req_start
                        ).total_seconds() * 1000
                        return response.status, elapsed_time
                except aiohttp.ClientError as e:
                    print(f"So'rov #{i} xatosi: {e}")
                    return None, None

            start_time = datetime.now()
            tasks = [fetch(i + 1) for i in range(n_requests)]
            results = await asyncio.gather(*tasks)

            total_time = (datetime.now() - start_time).total_seconds() * 1000
            statuses = [r[0] for r in results if r[0] is not None]
            times = [r[1] for r in results if r[1] is not None]

            print("\nStatistika (aiohttp):")
            print(f"Jami muvaffaqiyatli so'rovlar: {len(statuses)}")
            print(f"Umumiy vaqt: {total_time:.2f} ms")
            print(f"Ortacha vaqt: {sum(times) / len(times):.2f} ms")
            print(f"Maksimal vaqt: {max(times):.2f} ms")
            print(f"Minimal vaqt: {min(times):.2f} ms")

            return results

    return sync.async_to_sync(get_all)()


if __name__ == "__main__":
    N_REQUESTS = 500

    print("Starting async_aiohttp_get_all...")
    async_aiohttp_get_all(N_REQUESTS)
    print("\nStarting async_requests_get_all...")
    async_requests_get_all(N_REQUESTS)
    print("\nStarting sync_requests_get_all...")
    sync_requests_get_all(N_REQUESTS)

    print("\n----------------------")
    [print(duration) for duration in timed.durations]
