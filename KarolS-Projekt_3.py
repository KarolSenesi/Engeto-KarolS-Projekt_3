"""
KarolS-Projekt_2: Třetí projekt do Engeto Online Python Akademie
Web scraping volebních výsledků

author: Karol Seneši
email: senesi.charles@seznam.cz
discord: KarolS. (immaculate_gull_26453)
akademie: python-24-4-2024
"""

import sys
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Funkce pro získání obsahu stránky z dané URL
def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Chyba při načítání URL: {e}")
        sys.exit(1)

# Funkce pro přetvoření headerů v HTML do jednotného formátu
def fix_headers(soup):
    # Prochází všechny <td> elementy a upravuje atribut 'headers'
    for td in soup.find_all('td'):
        headers = td.get('headers')
        if headers:
            # Pokud je headers seznam, spojí ho do řetězce
            if isinstance(headers, list):
                headers = ' '.join(headers)
            # Rozdělení a oprava headery (odstranění druhé části 'sb')
            new_headers = headers.split()
            if len(new_headers) == 2 and "sb" in new_headers[1]:
                td['headers'] = new_headers[0]
    return soup

# Funkce pro analýzu hlavní stránky a získání odkazů na obce
def parse_main_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    municipalities = []
    # Procházení řádků tabulky a získání odkazů a názvů obcí
    for row in soup.select('table tr'):
        link = row.find('a')
        if link:
            href = link['href']
            name = row.find_all('td')[1].text.strip()
            municipalities.append((href, name))
    return municipalities

# Funkce pro analýzu stránky obce a získání volebních výsledků
def parse_municipality_page(html, code, name):
    soup = BeautifulSoup(html, 'html.parser')
    soup = fix_headers(soup)  # Oprava headery na stránce

    # Získání základních informací
    voters = soup.find('td', headers='sa2').text.strip()
    envelopes = soup.find('td', headers='sa3').text.strip()
    valid_votes = soup.find('td', headers='sa6').text.strip()

    # Získání výsledků stran
    party_results = {}
    for prefix in ['t1', 't2']:
        names = [
            cell.text.strip()
            for cell in soup.find_all('td', headers=f"{prefix}sa1")
        ]
        votes = [
            cell.text.strip()
            for cell in soup.find_all('td', class_='cislo',
                                      headers=f"{prefix}sa2")
        ]
        # Spárování názvů stran a jejich hlasů
        for i in range(len(names)):
            party_name = names[i]
            vote_value = votes[i] if i < len(votes) else "0"
            party_results[party_name] = vote_value

    # Vytvoření slovníku s výsledky obce
    results = {
        'Kód obce': code,
        'Název obce': name,
        'Voliči v seznamu': voters,
        'Vydané obálky': envelopes,
        'Platné hlasy': valid_votes,
    }
    results.update(party_results)
    return results, list(party_results.keys())

# Funkce pro uložení dat do CSV souboru
def save_to_csv(data, filename, parties):
    predefined = [
        "Občanská demokratická strana", "Řád národa - Vlastenecká unie",
        "CESTA ODPOVĚDNÉ SPOLEČNOSTI", "Česká str.sociálně demokrat.",
        "Radostné Česko", "STAROSTOVÉ A NEZÁVISLÍ",
        "Komunistická str.Čech a Moravy", "Strana zelených",
        "ROZUMNÍ-stop migraci,diktát.EU", "Strana svobodných občanů",
        "Blok proti islam.-Obran.domova", "Občanská demokratická aliance",
        "Česká pirátská strana", "Referendum o Evropské unii", "TOP 09",
        "ANO 2011", "Dobrá volba 2016", "SPR-Republ.str.Čsl. M.Sládka",
        "Křesť.demokr.unie-Čsl. lid.", "Česká strana národně sociální",
        "REALISTÉ", "SPORTOVCI", "Dělnic.str.sociální spravedl.",
        "Svob.a př.dem.-T.Okamura (SPD)", "Strana Práv Občanů"
    ]

    columns = ['Kód obce', 'Název obce', 'Voliči v seznamu',
               'Vydané obálky', 'Platné hlasy'] + predefined
    df = pd.DataFrame(data)

    # Zajištění, že všechny sloupce existují
    for party in predefined:
        if party not in df.columns:
            df[party] = "0"

    df = df[columns]
    df.to_csv(filename, index=False, encoding='utf-8-sig')

# Hlavní funkce programu
def main():
    if len(sys.argv) != 3:
        print("Chyba: Zadejte 2 argumenty: URL a název výstupního souboru.")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    # Načtení hlavní stránky
    html = fetch_page_content(url)
    municipalities = parse_main_page(html)

    all_data = []
    all_parties = set()

    # Zpracování jednotlivých obcí
    for relative_link, name in municipalities:
        match = re.search(r'xobec=(\d+)', relative_link)
        if not match:
            print(f"Varování: Nelze najít kód obce pro {relative_link}")
            continue

        code = match.group(1)
        full_url = f"https://www.volby.cz/pls/ps2017nss/{relative_link}"
        municipality_html = fetch_page_content(full_url)

        results, parties = parse_municipality_page(municipality_html,
                                                   code, name)
        all_data.append(results)
        all_parties.update(parties)

    # Uložení výsledků do CSV souboru
    save_to_csv(all_data, output_file, sorted(all_parties))
    print(f"Data byla úspěšně uložena do souboru {output_file}.")

# Spuštění programu
if __name__ == "__main__":
    main()
