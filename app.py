import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import time

# 1. Ввести url страницы
# 2. Выбрать тег
# 3. Забрать тег из html
# 4. Сохранить в файл

def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html, element): #Забираем со страницы указанные теги
    soup = BeautifulSoup(html, "html.parser")
    pageData = soup.findAll(element)
    data = []

    for i in pageData:
        content = str(i).strip("</" + element + ">")
        data.append(content)

    output_in_file(data)

def output_in_file(data):
    with open("data.txt", "a", encoding="utf-8") as outFile:
        for i in data:
            outFile.write(i + "\n")
        outFile.write("\n\n\n*******************************************************************************************\n\n\n")

def main():
    option = input("Вас приветствует html-парсер." + "\n" +
                    "Введите 1, если вы хотите спарсить ОДИН сайт. " + "\n" +
                    "Введите 2, если хотите начать парсинг НЕСКОЛЬКИХ сайтов: ")

    if option == "1":
        tag = input("\n" + "Введите тег, который вы хотите спарсить (например, a): ").lower()
        link = input("Введите URL сайта: ") #"https://python.ru/post/97/"

        t0 = time()
        get_page_data( get_html(link), tag )
        print("\n--- %s seconds ---" % (time() - t0))

        print("\n" + "DONE!")
        input()
    else:
        # --- 0.671875 seconds ---
        tag = input("\n" + "Введите тег, который вы хотите спарсить (например, a): ").lower()
        action = input("Введите URL'ы сайтов, с которых вы хотите забрать данные, в файл links.txt.")

        if action == "":
            t0 = time()
            asyncio.run(main2(tag))
            print("\n\n--- %s seconds ---" % (time() - t0))
            print("\n" + "DONE!")
            input()

async def async_get_page_data(html, element):
    soup = BeautifulSoup(html, "html.parser")
    pageData = soup.findAll(element)
    data = []

    for i in pageData:
        content = str(i).strip("</" + element + ">")
        data.append(content)

    output_in_file(data)


async def async_get_html(url, session, element):
    async with session.get(url) as link:
        html = await link.text()
        await async_get_page_data(html, element)

async def main2(element):
    urls = []
    tasks = []

    with open("links.txt", "r") as linksFile:
        for line in linksFile:
            newline = line.replace("\n", "")
            urls.append(newline)

    async with aiohttp.ClientSession() as session:
        for i in range(len(urls)):
            task = asyncio.create_task(async_get_html(urls[i], session, element))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    main()
