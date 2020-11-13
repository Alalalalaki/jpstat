import pandas as pd
from requests_html import HTMLSession
import json
import sys


def scrape_stat():
    url_base = 'https://www.e-stat.go.jp/stat-search/files?page=1'
    def url_info_base(
        x): return f"https://www.e-stat.go.jp/retrieve/api_file_modal?params[filters][toukei_cd]={x}&params[depth]=1&params[lang]=ja"

    session = HTMLSession()
    r = session.get(url_base)
    page_info = r.html.find(".stat-paginate-index", first=True)
    if page_info:
        pages = int(page_info.text[2:-3])
    else:
        pages = 1

    stats = []

    for p in range(pages):
        url = url_base[:-1] + str(p+1)
        r = session.get(url)

        tables = r.html.find(".stat-search_result-item1-main")
        for t in tables:
            d = {}
            d["@id"] = t.find(".stat-toukei_code_items > .stat-title", first=True).text
            d["STAT_NAME"] = t.find(".stat-toukei_name_items > .stat-title", first=True).text
            if t.find(".fa.fa-info", first=True):
                url_info = url_info_base(d["@id"])
                r = session.get(url_info)
                info = json.loads(r.html.text)
                d["GOV_ORG"] = info["kikan_kashitsu"]
                d["EXPLANATION"] = info["explanation"]
                d["HP_URL"] = info["exp_url"]

            stats.append(d)

            # sys.stdout.write("-")
            # sys.stdout.flush()

    df = pd.DataFrame(stats)
    return df


def scrape_list(statsCode, year=None):
    url_base = f"https://www.e-stat.go.jp/stat-search/files?layout=dataset&toukei={statsCode}"  # &page=1
    if year:
        url_base += f"&year={year}0"

    session = HTMLSession()
    r = session.get(url_base)
    page_info = r.html.find(".stat-paginate-index", first=True)
    if page_info:
        pages = int(page_info.text[2:-3])
    else:
        pages = 1

    stats = []

    tables = r.html.find(".stat-resource_list-main")
    for t in tables:
        d = {}
        info = t.find(".stat-resource_list-detail-item")
        d["STAT_NAME"] = info[0].text
        d["STAT_CAT"] = info[1].text
        d["SURVEY_DATE"] = info[2].text.replace("調査年月", "").replace("\xa0", "")
        d["OPEN_DATE"] = info[3].text.replace("公開（更新）日", "").replace("\xa0", "")
        file_links = info[4].find("a")
        for fl in file_links:
            if "data-file_type" in fl.attrs.keys():
                d["API"] = True
            else:
                file_type = fl.attrs["data-file_type"]
                d[file_type] = True
        data = t.find(".stat-link_text", first=True)
        d["@id"] = data.attrs["data-value"]
        d["STATISTICS_NAME"] = data.find(".stat-resource_list-detail-item-text", first=True).text.replace("\u3000", "-")

        stats.append(d)

    df = pd.DataFrame(stats)
    return df




