import requests
import pandas as pd
import json
from lxml import etree, html
from playwright.sync_api import sync_playwright

base_url = "https://panelinha.com.br"
recipes_url = base_url+"/home/receitas"

source = requests.get(recipes_url)
tree = etree.HTML(source.text)

recipes = tree.xpath('//div[@class="f fc mod jsTrackItem"]')

categories = {}

for e in recipes:
    list_name = e.get('data-item-list-name').encode('latin1').decode('utf-8')
    if list_name == 'Faça sua busca aqui':
        category = e.get('data-item-name').encode('latin1').decode('utf-8')
        e_tree = etree.HTML(html.tostring(e))
        url=e_tree.xpath('//a[@class="w100 f fcr tDn"]/@href')
        
        categories[category]=base_url+url[0]

for k,v in categories.items():
    print(k,v)

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # go to url
    page.goto("https://panelinha.com.br/busca?refinementList%5Bcategories%5D%5B0%5D=Aperitivos&menu%5Bpage_type%5D=Receitas")

    page.wait_for_selector('//span[@class="ais-Stats-text"]')


    page_html = page.content()
    tree = etree.HTML(page_html)

    recipes_aperitivos = tree.xpath('//a[@class="w100 f fcr tDn"]/@href') 

    print(recipes_aperitivos)