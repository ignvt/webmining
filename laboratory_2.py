from collections import Counter

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_page_by_year(source, year):
    response = requests.get(source + f"/{year}")
    if response.status_code == 200 or response.status_code == 304:
        return response.text
    else:
        return None


def get_table_data_by_page(html):
    result_data = []
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find("table", {"class": "rating-table auto"})
    headers = []
    for th in data.find("thead").find_all("th"):
        headers.append(th.get_text(strip=True))
    rows = data.find("tbody").find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        row_to_data = {}
        for i, cell in enumerate(cells):
            row_to_data[headers[i]] = cell.get_text(strip=True).replace("\xa0", "").replace(",", ".")
        result_data.append(row_to_data)
    return result_data


def get_all_data_by_years(source, years, region):
    result_data = []
    region_data = []
    for year in years:
        html = get_page_by_year(source, year)
        if html:
            data_page = get_table_data_by_page(html)
            result_data.extend(data_page)
    if region:
        for value in result_data:
            if value.get("Регион регистрации компании / головной компании") == region:
                region_data.append(value)
        return region_data
    return result_data


def get_total_profit_industry(data, years):
    total_by_ind = {}
    for industry in data:
        total_by_ind[industry.get("Отрасль")] = {"total": 0.0}
        for year in years:
            profit = industry.get(f"Чистая прибыль в {year} г. (млн руб.)", 0.0)
            if profit != "н.д.":
                try:
                    total_by_ind[industry.get("Отрасль")]["total"] += float(profit)
                except ValueError:
                    pass
    return total_by_ind


def get_all_industries(data):
    industries = []
    for industry in data:
        industries.append(industry.get("Отрасль"))
    return set(industries)


def find_max_total(data):
    max_total = 0
    max_industry = None
    for industry, values in data.items():
        total = values.get("total", 0)
        if total > max_total:
            max_total = total
            max_industry = industry
    return max_industry


def company_industry(data, main_industries):
    _list = {}
    for ind in main_industries:
        _list[ind] = []
        for row in data:
            if ind in row.get("Отрасль").lower():
                _list[ind].append(row.get("Регион регистрации компании / головной компании"))
    return _list


def range_by_company_industry(_list):
    ranked_list = {}
    for key, reg in _list.items():
        region_counts = Counter(reg)
        ranked_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)
        ranked_list[key] = ranked_regions
    return ranked_list


def ranked_list_view(_list):
    for ind, regs in _list.items():
        print(ind)
        for region, count in regs:
            print(f"{region}: {count}")


def main():
    source = "https://monocle.ru/reyting400"
    years = [2021, 2022, 2023]
    data = get_all_data_by_years(source, years, None)
    region_data = get_all_data_by_years(source, years, "Пермский край")
    total = get_total_profit_industry(data, years)
    best_industry = find_max_total(total)
    print(f"best_industry {best_industry}")
    total_region = get_total_profit_industry(region_data, years)
    best_industry_region = find_max_total(total_region)
    print(f"best_industry_region {best_industry_region}")
    industries = get_all_industries(data)
    main_industries = ["металлургия", "химическая", "нефтегазовая"]
    _list = company_industry(data, main_industries)
    ranked = range_by_company_industry(_list)
    ranked_list_view(ranked)
    data_csv = pd.read_csv("data-19-structure-4.csv")
    data_csv.columns = [col.strip() for col in data_csv.columns]
    grouped_data = data_csv.groupby("Название региона или Федерального округа")["Число музеев, ед."].sum()
    sorted_data = grouped_data.sort_values(ascending=False)
    print(sorted_data)


if __name__ == "__main__":
    main()
