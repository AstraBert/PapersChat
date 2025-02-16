import urllib, urllib.request
from pydantic import Field
from datetime import datetime
from markitdown import MarkItDown
from Bio import Entrez
import xml.etree.ElementTree as ET

md = MarkItDown()

def format_today():
    d = datetime.now()
    if d.month < 10:
          month = f"0{d.month}"
    else:
        month = d.month
    if d.day < 10:
        day = f"0{d.day}"
    else:
        day = d.day
    if d.hour < 10:
        hour = f"0{d.hour}"
    else:
        hour = d.hour
    if d.minute < 10:
        minute = f"0{d.hour}"
    else:
        minute = d.minute
    today = f"{d.year}{month}{day}{hour}{minute}"
    two_years_ago = f"{d.year-2}{month}{day}{hour}{minute}"
    return today, two_years_ago

def arxiv_tool(search_query: str = Field(description="The query with which to search ArXiv database")):
    """A tool to search ArXiv"""
    today, two_years_ago = format_today()
    query = search_query.replace(" ", "+")
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&submittedDate:[{two_years_ago}+TO+{today}]&start=0&max_results=3'
    data = urllib.request.urlopen(url)
    content = data.read().decode("utf-8")
    f = open("arxiv_results.xml", "w")
    f.write(content)
    f.close()
    result = md.convert("arxiv_results.xml")
    return result.text_content

def search_pubmed(query):
    Entrez.email = "astraberte9@gmail.com"  # Replace with your email
    handle = Entrez.esearch(db="pubmed", term=query, retmax=3)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_pubmed_details(pubmed_ids):
    Entrez.email = "your.personal@email.com"  # Replace with your email
    handle = Entrez.efetch(db="pubmed", id=pubmed_ids, rettype="medline", retmode="xml")
    records = handle.read()
    handle.close()
    recs = records.decode("utf-8")
    f = open("biomed_results.xml", "w")
    f.write(recs)
    f.close()

def fetch_xml():
    tree = ET.parse("biomed_results.xml")
    root = tree.getroot()
    parsed_articles = []
    for article in root.findall('PubmedArticle'):
        # Extract title
        title = article.find('.//ArticleTitle')
        title_text = title.text if title is not None else "No title"
        # Extract abstract
        abstract = article.find('.//Abstract/AbstractText')
        abstract_text = abstract.text if abstract is not None else "No abstract"
        # Format output
        formatted_entry = f"## {title_text}\n\n**Abstract**:\n\n{abstract_text}"
        parsed_articles.append(formatted_entry)
    return "\n\n".join(parsed_articles)

def pubmed_tool(search_query: str = Field(description="The query with which to search PubMed database")):
    """A tool to search PubMed"""
    idlist = search_pubmed(search_query)
    if len(idlist) == 0:
        return "There is no significant match in PubMed"
    fetch_pubmed_details(idlist)
    content = fetch_xml()
    return content    
