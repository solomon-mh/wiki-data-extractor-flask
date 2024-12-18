import requests  # Import the requests library for making HTTP requests.
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing and navigating HTML content.
import wikipediaapi  # Import wikipediaapi to interact with Wikipedia pages.



def extract_birth_city_info(name):
    """
    Extract birth info  from a Wikipedia page using requests and BeautifulSoup.
    """
    try:
        url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"  # Create the URL
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch Wikipedia page for {name}. HTTP status code: {response.status_code}")
            return None, None
        
        # Parse the page HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

         # Extract Infobox
        birth_info = "Unknown"
        infobox = soup.find('table', class_='infobox')

        if infobox:
            for row in infobox.find_all('tr'):
                header = row.find('th')
                if header and 'born' in header.text.lower():
                    birth_td = row.find('td')  # Find the corresponding <td> for "born"
                    if birth_td:
                        # Case 1: Check if there's a div with the class "birthplace"
                        birthplace_div = birth_td.find('div', class_='birthplace')
                        if birthplace_div:
                            birth_info = birthplace_div.text.strip()
                        # Case 2: Check if the td itself has a class like "birth_place"
                        elif 'birthplace' in birth_td.get('class', []):
                            print(birth_td)
                            birth_info = birth_td.text.strip()
                        else:
                            # Extract all text from the <td>, removing unwanted parts
                            birth_info = birth_td.get_text(separator=" ", strip=True)
                            # print("Raw birth info:", birth_info)

                            # Extract location based on <a> tags
                            location_parts = []
                            for a_tag in birth_td.find_all('a'):
                                location_parts.append(a_tag.get_text(strip=True))  # Collect text from all <a> tags

                            # Add any additional text directly after the last <a> tag
                            last_a_tag = birth_td.find_all('a')[-1] if birth_td.find_all('a') else None
                            if last_a_tag and last_a_tag.next_sibling:
                                extra_text = last_a_tag.next_sibling.strip()
                                if extra_text:  # Ensure there is meaningful text
                                    location_parts.append(extra_text)

                            # Join collected parts to form the final location string
                            birth_location = ", ".join(location_parts)
                            birth_info = birth_location
                            # print("Extracted birth location:", birth_location)
                    break
        return birth_info
    except Exception as e:
        print(f"Error while processing {name}: {e}")
        return None, None
def extract_early_life(name):
    """
    Extract the 'Early life' section using wikipedia-api.
    """
    try:
        wiki_wiki = wikipediaapi.Wikipedia('wiki-data-extractor','en')
        page = wiki_wiki.page(name)

        if not page.exists():
            print(f"Wikipedia page does not exist for {name}")
            return ""

        # Extract Early Life Section
        content = page.text
        early_life = ""
        start = content.find('Early life')
        if start != -1:
                    # List of section headings that could indicate the end of "Early life"
            section_headings = ['Career','Club career','Youth career', 'Amateur career', 'Personal life','Politics', 'Later life', 'Professional Career','Business career','Mid-life','Mid life','Nursing career','Apprenticeships']  # Add more if needed

            # Find the first occurrence of any of these section headings after 'Early life'
            end = -1
            for heading in section_headings:
                heading_start = content.find(heading, start)
                if heading_start != -1:
                    if end == -1 or heading_start < end:
                        end = heading_start

            # Extract the "Early life" section text
            if end == -1:
                early_life_text = content[start:]  # If no section heading is found, take the rest of the content
            else:
                early_life_text = content[start:end]

            early_life = early_life_text

        return early_life

    except Exception as e:
        print(f"Error while processing early life for {name}: {e}")
        return ""
