def get_links_from(sources):
    import requests
    from lxml import html
    links = []
    for source in sources:
        print('looking through ' + source[0])
        try:
            page = requests.get(source[0])
        except:
            page = requests.get(source[0], headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'})
        webpage = html.fromstring(page.content)
        anchors = webpage.xpath('//a/@href')
        print('links in ' + source[0] + '= ' + str(len(anchors)))
        if source[2]:
            [links.append(source[0] + link) for link in anchors if
             (source[1] in link) and not ((source[0] + link in links) or (link in links))]
        else:
            if source[3] is not None:
                [links.append(source[3] + link) for link in anchors if
                 (source[1] in link) and not ((source[3] + link in links) or (link in links))]
            else:
                [links.append(link) for link in anchors if
                 (source[1] in link) and not ((source[0] + link in links) or (link in links))]
    print('total links: ' + str(len(links)))
    return links


def download_url(url, directory="."):
    # type: (str, str) -> None
    from urllib.request import unquote, urlopen
    filename = url.rsplit('/', 1)[-1]
    filename = unquote(filename)
    print('downloading ' + filename + ' from ' + url)
    response = urlopen(url)
    web_content = response.read()
    print('saving as ' + directory + "/" + filename)
    f = open(directory + "/" + filename, 'w')
    f.write(web_content)
    f.close()


def download_cleaned_text_from_element(url, selector, path="."):
    from urllib.request import unquote, urlopen
    from bs4 import BeautifulSoup
    filename = url.rsplit('/', 1)[-1]
    directory_name = url.rsplit('/', 2)[-2]
    filename = unquote(filename) + ".txt"
    print('downloading ' + filename + ' from ' + url)
    response = urlopen(url)
    soup = BeautifulSoup(response, "lxml")
    content = soup.select_one(selector)
    dir_path = path + "\\" + directory_name
    file_path = dir_path + "\\" + filename
    print('saving as ' + file_path)
    try:
        import os
        os.makedirs(dir_path)
    except OSError as e:
        import errno
        if e.errno != errno.EEXIST:
            raise
    f = open(file_path, 'w')
    f.write(remove_extra_lines(strip_html(str(content))))
    f.close()


def remove_extra_lines(content):
    import re
    return re.sub("[\r\n]+", "\n", content)


def strip_html(content):
    import re
    return re.sub("<[!--\w/\. ]*>", "", content)


"""
for link in get_links_from([
    ["https://www.azlyrics.com/e/eminem.html", "lyrics/eminem", False, "https://www.azlyrics.com/e/"],
    ["https://www.azlyrics.com/d/drake.html", "lyrics/drake", False, "https://www.azlyrics.com/d/"],
    ["https://www.azlyrics.com/s/script.html", "lyrics/script", False, "https://www.azlyrics.com/s/"]

]):
    download_as_txt(link,
                    selector="body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-of-type(5)",
                    path="Z:\\Projects\\Python\\lyrics")
"""

import webbrowser

for link in get_links_from([
    ["http://www.mohamedaly.info/teaching/cmp-462-spring-2013", "attredirects=0&d=1", False,
     "http://www.mohamedaly.info"]
]):
    webbrowser.open(link)
