# Diagnosis: GitHub Parser Extracting 0 Internships

## The Symptom
Running `python src/ingest/github.py` successfully fetches data but outputs `0` internships. 

## The Root Cause
**You correctly identified the issue!** As noted in your task file: *"the function is stripping it by `|` but bc its html, wouldn't it not get anything?"*

Exactly. We assumed the GitHub `README.md` was using standard Markdown tables (which look like this: `| Company | Role |`). However, to support logos and custom formatting, the SimplifyJobs repository actually embeds raw **HTML tables** (`<table>`, `<tr>`, `<td>`) directly inside their Markdown file!

Because our `parse_markdown_table` function was looking for lines starting and ending with the `|` character, it skipped every single line of the HTML table, resulting in 0 internships.

## The Professional Solution (BeautifulSoup)
In the ETL (Extract, Transform, Load) world, dealing with unexpected data formats is standard practice. When we encounter HTML data in Python, the industry standard tool for parsing it is **BeautifulSoup** (which we already installed as `bs4` during the environment setup).

### How to fix it:
Instead of splitting the text by `\n` and hunting for `|`, we will use `BeautifulSoup` to search the document for `<tr>` (Table Row) and `<td>` (Table Data) elements.

Here is the updated logic we need to implement in `src/ingest/github.py`:

```python
from bs4 import BeautifulSoup

def parse_html_table(html_text: str) -> List[Dict[str, Any]]:
    print("Parsing HTML tables with BeautifulSoup...")
    internships = []
    
    # 1. Load the text into BeautifulSoup
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # 2. Find all table rows in the document
    rows = soup.find_all('tr')
    
    # The headers for this specific SimplifyJobs table
    headers = ['company', 'role', 'location', 'link', 'date_posted']
    
    for row in rows:
        # Find all cells in this row
        cells = row.find_all(['td', 'th'])
        
        # If the row doesn't have 5 columns, it's not a standard internship row
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
```

**Next Steps:**
I can update your `src/ingest/github.py` file to replace the markdown parser with this BeautifulSoup HTML parser, or you can copy and implement it manually to learn how it works!
