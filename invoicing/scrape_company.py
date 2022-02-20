from bs4 import BeautifulSoup
import requests


def get_company_data(srch_str):
    srch_str = srch_str.replace(" ", "+")
    response = requests.get(f"https://www.firmas.lv/lv/uznemumi/meklet?q={srch_str}")
    firmas = response.text
    soup = BeautifulSoup(firmas, "html.parser")
    h2_tag = soup.find_all(class_="mb-0")
    companies = []
    count = 0
    for company in h2_tag:
        count += 1
        companies.append({
            "nr": count,
            "name": company.getText().strip(),
            "href": company.find("a").get("href")
        })
    for company in companies:
        print(f"{company['nr']}: {company['name']}")
    return companies

def get_company(company):
    response = requests.get(f"https://www.firmas.lv{company['href']}")
    firma = response.text
    soup = BeautifulSoup(firma, "html.parser")
    h1 = soup.find("h1")
    company_name = h1.get_text()
    div = soup.find('div', id="Pamatdati")
    tds = div.find_all('td')
    company_data = [td.get_text().strip() for td in tds]
    company_info = {
        "name": company_name,
        "registration": company_data[3][:11],
        "vat": company_data[4][:13],
        "address": company_data[6][:-29]
    }

    for key, value in company.items():
        print(f"{key}: {value}")

    return company_info
