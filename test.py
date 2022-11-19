from unidecode import unidecode
import requests
from bs4 import BeautifulSoup as bs
import unicodedata
from openpyxl import Workbook

# islower returns false for - and symbols if no lower case letter

def strip_accents(text):

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

def check_if_at_least_one_lowercase_letter(text):
    for c in text:
        if c.islower():
            return True
    return False

# get raw text from website (using beautiful soup)
# includes advertisements, comments, ...
def scrape_page(url):
    # add url here and to main

    # excel file instructions
    wb = Workbook()
    wb['Sheet'].title = "Extracted names and emails"
    sh1 = wb.active
    sh1['A1'].value = 'Fullname'
    sh1['B1'].value = 'Email'
    line_counter = 1

    # html = requests.get(url).content
    # soup = bs(html, 'html.parser')
    with open('index.html', 'rt', encoding='utf-8') as fp:
        soup = bs(fp, 'html.parser')
    mydivs = soup.find_all("div", {"class": "single_libel"})
    for div in mydivs: 
        name = div.find("a").text
        sh1['A'+str(line_counter+1)].value = name.strip()
        names = name.split()
        i = 0
        email=""
        for word in names:
            word = strip_accents(word)
            if(check_if_at_least_one_lowercase_letter(word)):
                word = word.lower()
                if(i==0):
                    email = word
                    i = i+1
                else:
                    email = email + "-" + word
            else:
                word = word.lower()
                if(i == 1):
                    email = email + "." + word
                    i = i+1
                else:
                    email = email + "-" + word
        email = email + "@test.com"
        sh1['B'+str(line_counter+1)].value = email 
        line_counter = line_counter + 1
        print(email)
    """next_page_link = soup.find("a", class_="next")
    if next_page_link is not None:
        href = next_page_link.get("href")
        scrape_page(href)
    else:
        print ("Done")"""
    wb.save("FL-ExtractedEmailsSheet.xlsx")

    
# column name, column lastname, column email
if __name__ == "__main__":
    scrape_page("")
