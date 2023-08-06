import typer
import requests
from bs4 import BeautifulSoup as soup

app = typer.Typer()


@app.command()
def top(number: int):
    """
    top <number> : show top <number> sites URL on
    www.alexa.com/topsites/

    MAX NUMBER: 50
    """

    if number > 50:
        typer.echo("MAX NUMBER: 50\nPlease try again !")
        raise typer.Exit(code=1)
    elif number == 0:
        typer.echo("Must not be 0\nPlease try again !")
        raise typer.Exit(code=1)
    response = requests.get("https://www.alexa.com/topsites")
    page_soup = soup(response.text, "html.parser")
    container = page_soup.find("div", {"class": "listings table"})
    items = container.find_all("div", {"class": "td DescriptionCell"})
    for number, item in enumerate(items[:number], start=1):
        website = item.find("a").text
        url = item.find("a")["href"]
        typer.echo(str(number) + ". " + website + " : " + url.replace("/siteinfo/", "www."))


@app.command()
def country(country: str):
    """
    country <country> : show top 20 sites URL on www.alexa.com/topsites/

    Start with Capital Letter for example:\n
    Taiwan
    """

    country_dict = {'Albania': 'countries/AL', 'Algeria': 'countries/DZ', 'Argentina': 'countries/AR', 'Armenia': 'countries/AM', 'Australia': 'countries/AU', 'Azerbaijan': 'countries/AZ', 'Bahrain': 'countries/BH', 'Bangladesh': 'countries/BD', 'Belarus': 'countries/BY', 'Bolivia': 'countries/BO', 'Bosnia and Herzegovina': 'countries/BA', 'Brazil': 'countries/BR', 'Bulgaria': 'countries/BG', 'Cambodia': 'countries/KH', 'Cameroon': 'countries/CM', 'Canada': 'countries/CA', 'Chile': 'countries/CL', 'China': 'countries/CN', 'Colombia': 'countries/CO', 'Costa Rica': 'countries/CR', "Cote d'Ivoire": 'countries/CI', 'Czech Republic': 'countries/CZ', 'Dominican Republic': 'countries/DO', 'Ecuador': 'countries/EC', 'Egypt': 'countries/EG', 'Ethiopia': 'countries/ET', 'France': 'countries/FR', 'Georgia': 'countries/GE', 'Germany': 'countries/DE', 'Ghana': 'countries/GH', 'Greece': 'countries/GR', 'Guatemala': 'countries/GT', 'Hong Kong': 'countries/HK', 'India': 'countries/IN', 'Indonesia': 'countries/ID', 'Iran': 'countries/IR', 'Iraq': 'countries/IQ', 'Israel': 'countries/IL', 'Italy': 'countries/IT', 'Jamaica': 'countries/JM', 'Japan': 'countries/JP', 'Jordan': 'countries/JO', 'Kazakhstan': 'countries/KZ', 'Kenya': 'countries/KE', 'Kuwait': 'countries/KW', 'Kyrgyzstan': 'countries/KG', 'Lebanon': 'countries/LB', 'Libya': 'countries/LY', 'Macedonia': 'countries/MK', 'Malaysia': 'countries/MY', 'Mauritania': 'countries/MR', 'Mauritius': 'countries/MU', 'Mexico': 'countries/MX', 'Moldova': 'countries/MD', 'Mongolia': 'countries/MN', 'Morocco': 'countries/MA', 'Nepal': 'countries/NP', 'Netherlands': 'countries/NL', 'New Zealand': 'countries/NZ', 'Nicaragua': 'countries/NI', 'Nigeria': 'countries/NG', 'Oman': 'countries/OM', 'Pakistan': 'countries/PK', 'Palestinian Territory': 'countries/PS', 'Panama': 'countries/PA', 'Peru': 'countries/PE', 'Philippines': 'countries/PH', 'Poland': 'countries/PL', 'Puerto Rico': 'countries/PR', 'Qatar': 'countries/QA', 'Romania': 'countries/RO', 'Russia': 'countries/RU', 'Saudi Arabia': 'countries/SA', 'Senegal': 'countries/SN', 'Serbia': 'countries/RS', 'Singapore': 'countries/SG', 'South Africa': 'countries/ZA', 'South Korea': 'countries/KR', 'Spain': 'countries/ES', 'Sri Lanka': 'countries/LK', 'Sudan': 'countries/SD', 'Sweden': 'countries/SE', 'Switzerland': 'countries/CH', 'Syrian Arab Republic': 'countries/SY', 'Taiwan': 'countries/TW', 'Tanzania': 'countries/TZ', 'Thailand': 'countries/TH', 'Trinidad and Tobago': 'countries/TT', 'Tunisia': 'countries/TN', 'Turkey': 'countries/TR', 'Uganda': 'countries/UG', 'Ukraine': 'countries/UA', 'United Arab Emirates': 'countries/AE', 'United Kingdom': 'countries/GB', 'United States': 'countries/US', 'Uruguay': 'countries/UY', 'Uzbekistan': 'countries/UZ', 'Venezuela': 'countries/VE', 'Vietnam': 'countries/VN', 'Yemen': 'countries/YE'}

    if country in country_dict:
        response = requests.get(f"https://www.alexa.com/topsites/{country_dict[country]}")
        page_soup = soup(response.text, "html.parser")
        container = page_soup.find("div", {"class": "listings table"})
        items = container.find_all("div", {"class": "td DescriptionCell"})
        for number, item in enumerate(items[:20], start=1):
            website = item.find("a").text
            url = item.find("a")["href"]
            typer.echo(str(number) + ". " + website + " : " + url.replace("/siteinfo/", "www."))
    else:
        typer.echo("Must be a country and start with capital letter!")
        raise typer.Exit(code=1)
