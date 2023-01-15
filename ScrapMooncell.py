import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions

servant_list_site = 'https://fgo.wiki/w/%E8%8B%B1%E7%81%B5%E5%9B%BE%E9%89%B4/%E6%95%B0%E6%8D%AE' 
servant_list_core = 'https://fgo.wiki/index.php?title=Widget:ServantsList/core&action=edit'
servant_site = 'https://fgo.wiki/w/'

options = EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

ser = Service('C:\msedgedriver.exe')
driver = webdriver.Edge(service = ser, options=options)

# get all servants' link name
driver.get(servant_list_site)
all_servants = driver.find_element(By.CLASS_NAME, 'mw-parser-output')
all_servants = re.findall('name_link=(.*) name_other', all_servants.text)
all_servants.reverse()

# get all servants' info
driver.get(servant_list_core)
textarea = driver.find_element(By.TAG_NAME, 'textarea')
textarea = textarea.text.split('\n')

servant_list = []
for row in textarea:
    servant_list.append(row.split(','))

header = servant_list[0]
servant_list = servant_list[1:]

# make dataframe
df = pd.DataFrame(servant_list, columns=header)
df['Servant'] = all_servants
df = df[['Servant','star','class_link']]
df.rename(columns={'avatar':'Avatar','star':'Rarity','class_link':'Class'}, inplace=True)

# scrap materials required
results = []
for index in df.index:
    driver.get(servant_site + df['Servant'][index])
    table_c = driver.find_elements(By.XPATH, "//table[@class='wikitable nomobile']")
    result = df.loc[index].values.tolist()
    for t in table_c:
        # direct to skill level table
        if '1→2' in t.text[:4]:
            # number if materials needed
            counts = t.text.split('\n')
            counts = [count for count in counts if '→' not in count]
            stopping_index = counts.index('总计')
            counts = counts[:stopping_index]
            
            # materials' name
            table_m = t.find_elements(By.TAG_NAME, 'a')
            materials = []
            for i, material in enumerate(table_m):
                if i == stopping_index:
                    break
                materials.append(material.get_attribute('title'))
            
            # a few cleanning 
            counts = list(map(lambda count: count.replace('万', '0000'), counts))
            materials = list(map(lambda material: material if len(material)!=0 else material.replace('', 'QP'), materials))
            
            # map materials & count based on level
            requirement = {}
            requirements = []
            for i, material in enumerate(materials):
                requirement[material] = int(counts[i])
                if material == 'QP':
                    requirements.append(requirement)
                    requirement = {}
            
            # sort result based on level
            result += sorted(requirements, key=lambda qp:qp['QP'])
    results.append(result)

# make results' dataframe 
header = ['Servant', 'Rarity', 'Class'] + ['S'+str(num) for num in range(2,11)] + ['A'+str(num) for num in range(2,11)]
df_results = pd.DataFrame(results, columns=header)

df_results.to_csv('materials_required.csv', index=False, encoding='utf-8-sig')