import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent().random

class cs:
    INFO = '\033[93m'
    GREEN = '\033[92m'
    END = '\033[0m'

RU_EN_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}

def slugify(text: str) -> str:
    text = text.lower()
    translit = "".join(RU_EN_MAP.get(c, c) for c in text)
    return re.sub(r"[^a-z0-9]+", "-", translit).strip("-")

async def fetch(session, url, sem):
    headers = {"User-Agent": user_agent}
    async with sem:
        try:
            async with session.get(url, headers=headers, timeout=5) as response:
                if response.status == 200 and 'html' in response.headers.get('Content-Type', ''):
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    date_tag = soup.find('time') or soup.find(class_='tl_article_date')
                    date_text = date_tag.text.strip() if date_tag else "❓ Дата не найдена"

                    print(f"{cs.GREEN}✅ Найдено: {url} — 🗓 {date_text}{cs.END}")
                    return f"✅ {url} — 🗓 {date_text}"
                else:
                    print(f"{cs.INFO}❌ Не найдено: {url}{cs.END}")
        except Exception as e:
            print(f"{cs.INFO}⚠️ Ошибка запроса: {url} | {e}{cs.END}")
    return None

async def parse_title(title: str, offset: int = 2) -> list[str]:
    slug = slugify(title.strip())
    sem = asyncio.Semaphore(20)
    urls = []

    for month in range(1, 13):
        for day in range(31, 0, -1):
            for i in range(1, offset + 1):
                suffix = f"-{i}" if i > 1 else ""
                url = f"https://telegra.ph/{slug}-{month:02}-{day:02}{suffix}"
                urls.append(url)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, sem) for url in urls]
        results = await asyncio.gather(*tasks)

    return [r for r in results if r is not None]
