###
from bs4 import BeautifulSoup
import json
import math
import numpy as np
import pandas as pd
import re
import requests
import setuptools
from splinter import Browser
###
def test():
    print("THIS IS A TEST :)")
###
def variables_to_csv(url):
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    table_rows = browser.find_by_tag("tr")
    variable_list = []
    for i in range(len(table_rows)):
        table_row_html = BeautifulSoup(table_rows[i].html, "html.parser")
        try:
            variable = table_row_html.find_all("td")[0].text
            concept = table_row_html.find_all("td")[2].text
            label = table_row_html.find_all("td")[1].text
            variable_list.append([variable,
                                  concept,
                                  label])
        except IndexError:
            continue
    variable_df = pd.DataFrame(variable_list, columns=["Variable",
                                                       "Concept",
                                                       "Label"])
    y = re.search('(20..)',url)
    t = re.search('(?<=acs/)(.*?)(?=/variables)',url)
    year = y.group(0)
    api_name = t.group(0).replace("/", "_")
    csv_name = api_name + "_" + year + "_variables.csv"

    variable_df.to_csv(csv_name, index=False)
    return variable_df
###
def complete_geography_urls_to_csv(url):
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    table_rows = browser.find_by_tag("tr")
    geography_level = 0
    initial_letter = "a"
    geography_url_list = []
    for i in range(len(table_rows)):
        try:
            table_row_html = BeautifulSoup(table_rows[i].html, "html.parser")

            row_level = table_row_html.find_all("td")[1].text
        except (IndexError):
            continue
        for link in table_row_html.find_all("a"):
                href = link.get('href')
                pattern = re.compile('(?=:)(.*?)((?<=[\*])|(?=[\%])|(:\d+)|(:\w+))', re.S)
                cleaned_href = re.sub(pattern, ':{}', href)
                pattern = re.compile('(?<=get=)(.*?)(?=&)', re.S)
                formatted_href = "https://api.census.gov" + re.sub(pattern, '{variables}', cleaned_href) + "&key={census_api_key}"
        try:
            if int(row_level) > geography_level:
                geography_level = int(row_level)
                initial_letter = "a"
                row_gl = str(geography_level) + initial_letter
        except (ValueError):
            next_letter = chr(ord(initial_letter) + 1)
            initial_letter = next_letter
            row_gl = str(geography_level)+ next_letter
        geography_url_list.append([row_gl, formatted_href])

    y = re.search('(20..)',url)
    t = re.search('(?<=acs/)(.*?)(?=/examples)',url)
    year = y.group(0)
    api_name = t.group(0)
    csv_name = api_name + "_" + year + "_geography_urls.csv"


    geography_urls_df = pd.DataFrame(geography_url_list, columns=["Code", "API url"])
    geography_urls_df = pd.DataFrame(geography_url_list, columns=["Code", "API url"])
    geography_urls_df.to_csv(csv_name, index=False)
    return geography_urls_df
###
def partial_geography_urls_to_csv(url):
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    table_rows = browser.find_by_tag("tr")
    geography_level = 0
    initial_letter = "a"
    geography_url_list = []
    for i in range(len(table_rows)):
        try:
            table_row_html = BeautifulSoup(table_rows[i].html, "html.parser")

            row_level = table_row_html.find_all("td")[1].text
        except (IndexError):
            continue
        for link in table_row_html.find_all("a"):
                href = link.get('href')
                pattern = re.compile('(?=:)(.*?)((?<=[\*])|(?=[\%])|(:\d+)|(:\w+))', re.S)
                cleaned_href = re.sub(pattern, ':{}', href)
                formatted_href = re.search('(?=for=)(.*?)($)', cleaned_href).group(0)
        try:
            if int(row_level) > geography_level:
                geography_level = int(row_level)
                initial_letter = "a"
                row_gl = str(geography_level) + initial_letter
        except (ValueError):
            next_letter = chr(ord(initial_letter) + 1)
            initial_letter = next_letter
            row_gl = str(geography_level)+ next_letter
        geography_url_list.append([row_gl, formatted_href])

    y = re.search('(20..)',url)
    t = re.search('(?<=acs/)(.*?)(?=/examples)',url)
    year = y.group(0)
    api_name = t.group(0)
    csv_name = api_name + "_" + year + "_geography_urls.csv"


    geography_urls_df = pd.DataFrame(geography_url_list, columns=["Code", "API url"])
    geography_urls_df = pd.DataFrame(geography_url_list, columns=["Code", "API url"])
    geography_urls_df.to_csv(csv_name, index=False)
    return geography_urls_df
###
def sub_variable_list(csv_name, variable):
    variables_df = pd.read_csv(csv_name)
    sub_variable_list = variables_df[variables_df["Variable"].str.contains(variable)]["Variable"].to_list()
    return sub_variable_list
###
def sub_variable_df(csv_name, variable):
    variables_df = pd.read_csv(csv_name)
    sub_variable_df = variables_df[variables_df["Variable"].str.contains(variable)]
    return sub_variable_df
###
def sub_variable_str(csv_name, variable):
    variables_df = pd.read_csv(csv_name)
    sub_variable_list = variables_df[variables_df["Variable"].str.contains(variable)]["Variable"].to_list()
    sub_variable_str = ","
    sub_variable_str = sub_variable_str.join(sub_variable_list)

    return sub_variable_str
###
def geography_url_builder (geography_level, gl_parameters):
    if type(gl_parameters) == tuple:
        gl_parameters = list(gl_parameters)
    elif type(gl_parameters) != list:
        gl_parameters = [gl_parameters]
    geography_urls_df = pd.read_csv("acs5_2018_geography_urls.csv")
    url = geography_urls_df["API url"].loc[geography_urls_df["Code"] == geography_level].to_list()[0]
    geography_url = url.format(*gl_parameters)

    return geography_url
###
def geoid_constructor(df):
    try:
        if all(x in df.columns for x in ["State", "County", "Tract", "Block Group"]) == True:
            df["Geoid"] = df["State"] + df["County"] + df["Tract"] + df["Block Group"]
        elif all(x in df.columns for x in ["State", "County", "Tract"]) == True:
            df["Geoid"] = df["State"] + df["County"] + df["Tract"]
        return df
    except KeyError:
        return df
###
def census_api_query(csv_file_name, parent_variable, year_list, geography_level, gl_parameters, api_key):
    api_name = re.search('(?=acs)(.*?)(?=_2)', csv_file_name).group(0).replace("_", "/")
    api_year = re.search('(?<=_)(.*?)(?=.csv)',csv_file_name).group(0)
    # Using the sub_variable_list function
    query_variable_list = sub_variable_list(csv_file_name, parent_variable)
    geography_url = geography_url_builder(geography_level, gl_parameters)
    geography_param_len = len(gl_parameters)
    geography_value = ""
    # Using the sub_variable_df function
    label_df = sub_variable_df(csv_file_name, parent_variable)[["Label", "Concept"]].reset_index(drop=True)
    result_df = pd.DataFrame()
    ind = 0
    if len(query_variable_list) > 50:
        div = 50
        # Initializing a variable to hold the number of sets of variables
        lim = math.ceil(len(query_variable_list) / div)
        # Initializing a list to hold the lists of variables
        sets = [query_variable_list[(i * div):(i * div + div)] for i in range(0, lim)]
        for year in year_list:
            try:
                base_url = f"https://api.census.gov/data/{year}/acs/{api_name}?get="
                # Using the geography_url_builder function
                row_df = pd.DataFrame()
                for i in range(len(sets)):
                    sub_variable_str = ","
                    sub_variable_str = sub_variable_str.join(sets[i])
                    complete_url = base_url+f"{sub_variable_str}&{geography_url}&key={api_key}"
                    if ind == 0:
                        print(complete_url)
                    api_response = requests.get(complete_url).json()
                    var_names = api_response[0][:-geography_param_len]
                    geog_param_names = [name.title() for name in api_response[0][-geography_param_len:]]
                    for i in range(len(api_response)-1):
                        current_entry = api_response[i+1]
                        current_entry_geog = api_response[i+1][-geography_param_len:]
                        current_entry_data = api_response[i+1][:-geography_param_len]
                        geog_df = pd.DataFrame(np.repeat([current_entry_geog], len(current_entry_data), axis=0), columns=geog_param_names)
                    intermediate_df = pd.DataFrame([var_names, current_entry_data], index=["Variable", "Value"]).transpose()
                    row_df = pd.concat([row_df, intermediate_df]).reset_index(drop=True)
                row_df = pd.concat([row_df, geog_df, label_df], axis=1)
                row_df["Year"] = str(year)
                result_df = pd.concat([result_df, row_df])
            except json.decoder.JSONDecodeError as e:
                na_lst = []
                for i in range(len(query_variable_list)):
                    na_lst.append(np.NaN)
                row_df = pd.DataFrame([var_names, na_lst], index=["Variable", "Value"]).transpose()
                row_df = pd.concat([row_df, geog_df, label_df], axis=1)
                row_df["Year"] = str(year)
                result_df = pd.concat([result_df, row_df])
                continue
            ind +=1
    else:
        sub_variable_str = ","
        sub_variable_str = sub_variable_str.join(query_variable_list)
        for year in year_list:
            try:
                base_url = f"https://api.census.gov/data/{year}/acs/{api_name}?get="
                complete_url = base_url+f"{sub_variable_str}&{geography_url}&key={api_key}"
                if ind == 0:
                        print(complete_url)
                api_response = requests.get(complete_url).json()
                var_names = api_response[0][:-geography_param_len]
                geog_param_names = [name.title() for name in api_response[0][-geography_param_len:]]
                for i in range(len(api_response)-1):
                    current_entry = api_response[i+1]
                    current_entry_geog = api_response[i+1][-geography_param_len:]
                    current_entry_data = api_response[i+1][:-geography_param_len]
                    geog_df = pd.DataFrame(np.repeat([current_entry_geog], len(current_entry_data), axis=0), columns=geog_param_names)
                    row_df = pd.DataFrame([var_names, current_entry_data], index=["Variable", "Value"]).transpose()
                    row_df = pd.concat([row_df, geog_df, label_df], axis=1)
                    row_df["Year"] = str(year)     
                    result_df = pd.concat([result_df, row_df], axis=0)
                    
            except json.decoder.JSONDecodeError as e:
                na_lst = []
                for i in range(len(query_variable_list)):
                    na_lst.append(np.NaN)
                row_df = pd.DataFrame([var_names, na_lst], index=["Variable", "Value"]).transpose()
                row_df = pd.concat([row_df, geog_df, label_df], axis=1)
                row_df["Year"] = str(year)
                result_df = pd.concat([result_df, row_df])
                continue
            ind +=1
    cols = list(result_df.columns)
    cols = cols[-1:] + cols[0:-1]
    result_df = result_df[cols].reset_index(drop=True)
    geoid_constructor(result_df)
    return result_df