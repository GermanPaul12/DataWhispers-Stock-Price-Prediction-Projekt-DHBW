# Importing required libraries
# os for interacting with the operating system
# pandas for data manipulation
# lxml for parsing HTML
# datetime for handling date and time
import os
import pandas as pd
from lxml import html
from datetime import datetime, timedelta

# Function to convert the number of days since January 1, 1900, to a date
def days_to_date(days_since_1900):
    """
    Funktion, um die Anzahl der Tage seit 1900 in ein Datum umzuwandeln.
    
    Args:
    days_since_1900 (int): Anzahl der Tage seit dem 1. Januar 1900.
    
    Returns:
    datetime.date: Das umgewandelte Datum.
    """
    if isinstance(days_since_1900, str):
        days_since_1900 = int(days_since_1900)
    base_date = datetime(1900, 1, 1)
    delta = timedelta(days=days_since_1900-2)
    target_date = base_date + delta
    return target_date

# Beispielaufruf der Funktion mit der Anzahl der Tage seit 1900
days_since_1900 = 43770  # Beispielwert
converted_date = days_to_date(days_since_1900)
print(f'Das Datum für {days_since_1900} Tage seit 1900 ist: {converted_date.strftime("%Y-%m-%d")}')


# %%
def is_valid_article(tree) -> bool:
    # Den Titel der Webseite auswählen (XPath-Ausdruck)
    title_element = tree.xpath('//title')

    # Den Textinhalt des Titel-Elements überprüfen
    return title_element[0].text != 'Access Denied'

# %%
def extract_features_from_article(file_path:str) -> tuple[str, str]:
    """
    Funktion, die Beautiful Soup und XPath verwendet, um Elemente aus einer HTML-Datei zu extrahieren.
    
    Args:
    file_path (str): Der Pfad zur HTML-Datei.
    
    Returns:
    list: Eine Liste mit den extrahierten Elementen.
    """
    
    
    # HTML-Datei öffnen und als BeautifulSoup-Objekt parsen
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        tree = html.fromstring(content)

    if not is_valid_article(tree):
        raise ValueError('Not a valid article. "Access Denied"')

    title = tree.xpath('/html/body/main/div[11]/div/div/div[1]/h1')[0].text_content()
    content = tree.xpath('/html/body/main/div[11]/div/div/div[3]/div/article/div[2]')[0].text_content()
    
    if content == '' or title == '':
        raise ValueError('Not a valid article. "Title or content is missing"')

    return title, content

# %%
import os
import concurrent.futures

directory_path = './data/'

def process_subfolder(subfolder):
    try:
        date = days_to_date(subfolder)
        files = [f.name for f in os.scandir(os.path.join(directory_path, subfolder)) if f.is_file()]
        processed_articles, failed_articles = 0, 0

        for file in files:
            try:
                title, content = extract_features_from_article(os.path.join(directory_path, subfolder, file))
                url = ''
                data.append((date, url, title, content))
            except Exception as e:
                failed_articles += 1
                # print(f"Failed to load file {file}. {e}")
            else:
                # print(f"Succeeded to load file {file}")
                processed_articles += 1

        print(f"Date: {date.strftime('%Y-%m-%d')}, Processed articles: {processed_articles}, Failed articles: {failed_articles}")
        return processed_articles, failed_articles

    except Exception as e:
        print(f"Error processing subfolder {subfolder}: {e}")
        return 0, 0

# %%
data = []
subfolders = [f.name for f in os.scandir(directory_path) if f.is_dir()]
processed_articles = 0
failed_articels = 0
    
with concurrent.futures.ThreadPoolExecutor() as executor:  # Verwende ThreadPoolExecutor für parallele Ausführung
    futures = [executor.submit(process_subfolder, subfolder) for subfolder in subfolders]

    processed_articles, failed_articles = 0, 0
    for future in concurrent.futures.as_completed(futures):
        processed, failed = future.result()
        processed_articles += processed
        failed_articles += failed

df = pd.DataFrame(data, columns=["date", "url", "title", "content"])
df.to_csv('preprocessed_data.csv')

print('Dataframe saved')
print(f"Processed articles: {processed_articles}, Failed articles: {failed_articles}")