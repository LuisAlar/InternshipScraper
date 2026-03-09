import httpx
import re
from typing import List,Dict, Any  
from bs4 import BeautifulSoup

# fetch data from github repo 
def fetch_readme(repo_url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md"
) -> str:
    print("fetching Data..")

    response = httpx.get(repo_url)
   

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

# parse data into clean table 
def parse_html_table(html_text: str) -> List[Dict[str,Any]]:
    print("parsing Mardown Tables...")
    internships = []

    soup = BeautifulSoup(html_text, 'html.parser')
    # find all tables rows in the doc
    rows = soup.find_all("tr")

    headers = ['company', 'role', 'location', 'link', 'date_posted']

    for row in rows:
        cells = row.find_all(['td', 'th'])

        if len(cells) != 5:
            continue

        # 3. Extract the clean text from each cell
        company = cells[0].get_text(strip=True)
        role = cells[1].get_text(strip=True)
        location = cells[2].get_text(strip=True)
        
        # 4. Extract the href (URL) from the link column if it exists
        link_tag = cells[3].find('a')
        link_url = link_tag['href'] if link_tag and link_tag.has_attr('href') else ""
        
        date_posted = cells[4].get_text(strip=True)
        
        # 5. Skip table headers or closed roles
        if company.lower() == 'company' or 'closed' in location.lower() or '🔒' in link_url:
            continue
            
        internships.append({
            'company': company,
            'role': role,
            'location': location,
            'url': link_url,
            'date_posted': date_posted
        })
        
    return internships


    

def clean_parse_data(internships: List[Dict[str, Any]]) -> List[Dict[str,Any]]:
    cleaned = []

    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for item in internships:
        if 'company' in item:
            match = link_pattern.search(item['company'])
            if match:
                item['company'] = match.group(1) # Gets the text part
        
        # Let's clean the link field too
        link_key = next((k for k in item.keys() if 'link' in k or 'application' in k), None)
        if link_key and item[link_key]:
            # Some roles might be marked as closed like "🔒" or "Closed"
            if 'close' in item[link_key].lower() or '🔒' in item[link_key]:
                continue # Skip closed internships! (Saves compute!)
                
            match = link_pattern.search(item[link_key])
            if match:
                item['url'] = match.group(2) # Gets the URL part
        
        cleaned.append(item)
        
    return cleaned


def extract_github_internships() -> List[Dict[str, Any]]:
    raw_md = fetch_readme()
    raw_internships = parse_html_table(raw_md)
    clean_internships = clean_parse_data(raw_internships)

    print(f"Successfully extracted {len(clean_internships)} open internships!")
    return clean_internships

# This block lets you run this file directly to test it:
if __name__ == "__main__":
    results = extract_github_internships()
    if results:
        print("Here is the first extracted internship:")
        print(results[0])

