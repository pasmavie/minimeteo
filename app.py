#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import time
import pathlib
import os

from selenium.webdriver.support.ui import Select
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional

DATA_DIR = pathlib.Path(os.getcwd()) / "DATA"

URLS = {
    'highresolution': 'https://www.lamma.rete.toscana.it/mare/modelli/vento-mare.php?area=T',
    'lowresolution':'https://www.lamma.rete.toscana.it/mare/modelli/vento-mare-hr.php?area=B',
}

def cycle_and_download(
    driver: webdriver.chrome.webdriver.WebDriver,
    url: str, 
    data_name: Optional[str]= None
):
    data_name = data_name or ''.join(e for e in url if e.isalnum())
    driver.get(url=url)
    area_dropdown = Select(driver.find_element_by_id('aree'))
    available_areas = [o.get_attribute('value') for o in area_dropdown.options] 
    for i in available_areas:  # Ugly loop
        area_dropdown.select_by_value(i)
        selected_area_str = area_dropdown.first_selected_option.text.replace(' ', '')
        maptype_dropdown = Select(driver.find_element_by_id('campi'))
        available_maptypes = [o.get_attribute('value') for o in maptype_dropdown.options]
        for mt in available_maptypes:
            selected_maptype_str = maptype_dropdown.first_selected_option.text.replace(' ', '')
            save_path = DATA_DIR / data_name / selected_area_str / selected_maptype_str
            if not save_path.exists():
                os.makedirs(save_path)
            # A simpler alternative to the code below exists: driver.find_element_by_id('zipfile').click()
            # but it doesn't allow to save the map names and times...
            time_dropdown = Select(driver.find_element_by_id('display-data'))
            available_times = [o.get_attribute('value') for o in time_dropdown.options]
            for t in available_times:
                time_dropdown.select_by_value(t)
                selected_time_str = time_dropdown.first_selected_option.text.replace(' ', '')
                save_path = save_path / f'{selected_area_str}_{selected_time_str}.png'
                driver.save_screenshot(str(save_path.resolve()))


if __name__ == "__main__":
    driver = webdriver.Chrome(ChromeDriverManager().install())
    f = functools.partial(cycle_and_download, driver=driver)
    for map_name, url in URLS.items():
        f(url=url, data_name=map_name)
