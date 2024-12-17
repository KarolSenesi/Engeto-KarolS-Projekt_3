WEB SCRAPING VOLEBNÍCH VÝSLEDKŮ V PYTHONU
Tento skript provádí web scraping volebních výsledků voleb do Poslanecké
sněmovny Parlamentu České republiky konaných ve dnech 20.10. – 21.10.2017
podle následujícího schématu:

1.) Z konkrétního odkazu na vybraný územní celek (okres) vybere výsledky
za všechny obce.

2.) Za každou obec vybere:
kód obce
název obce
voliče v seznamu
vydané obálky
platné hlasy
kandidující strany (každý sloupec reprezentuje počet hlasů pro danou stranu).
Skript využívá knihovny BeautifulSoup, Requests a Pandas prozpracování HTML.

3.) Vygeneruje a uloží obsah do CSV souboru. Každý řádek představuje
jeden volební okrsek v rámci územního celku. Skript generuje celková
data za obec (nevypisuje zvlášť data za jednotlivé okrsky v obci).

POŽADAVKY
Python 3.9 a vyšší
IDE vývojový nástroj (např. Visual Studio Code, PyCharm atd.)
Internetové připojení pro stahování stránek
Soubor KarolS-Projekt_3-requirements.txt obsahující potřebné knihovny

INSTALACE A SPUŠTĚNÍ
I. Vytvoření a aktivace virtuálního prostředí
Nejprve vytvořte virtuální prostředí:

Otevřete terminál ve složce projektu.
Vytvořte virtuální prostředí příkazem:
python -m venv venv
Aktivujte virtuální prostředí:
Windows:
.\venv\Scripts\activate
Linux / macOS:
source venv/bin/activate
Po aktivaci terminál zobrazí jméno virtuálního prostředí, například (venv).

II. Instalace potřebných knihoven
Všechny potřebné knihovny jsou uvedeny v souboru
KarolS-Projekt_3-requirements.txt. 
Pro jejich instalaci spusťte:
pip install -r KarolS-Projekt_3-requirements.txt

Tímto se nainstalují následující knihovny:

requests - pro stahování HTML stránek
beautifulsoup4 - pro analýzu HTML
pandas - pro zpracování a ukládání dat

III. Spuštění programu
Program spustíte následujícím příkazem se dvěma argumenty:
python KarolS-Projekt_3.py <URL> <vystupni_soubor.csv>
kde:

<URL>: Odkaz na stránku s volebními výsledky.
<vystupni_soubor.csv>: Jméno výstupního CSV souboru, kam se data uloží.
Příklad spuštění:
python KarolS-Projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3106" "vysledky_Strakonice.csv"

KOMENTÁŘ
Předem upozorňuji, že výstupy v souboru CSV bohužel neodpovídají 100%
zadání. U výsledků za jednotlivé strany se zobrazují hodnoty "v %"
namísto hodnot "celkem".

Bohužel je to záhada a nevím, co se děje. Kód odpovídá stránce a rozložení
tabulky. Explicitně je uvedeno, že se má tahat hodnota označená ve zdrojovém
kódu stránky jako t1sa2 a t1sb3 (případně t2sa2 a t2sb3 u druhé
tabulky).

Jelikož vše ukazuje na problém s headery na samotné stránce, doplnil
jsem funkci, která upraví headery do jednotného (lepšího) formátu. Viz
aktuální verze kódu, kterou posílám k validaci. Bohužel se mi stále načítají
hodnoty v %.

Opravdu už nevím, co s tím dál. :-)