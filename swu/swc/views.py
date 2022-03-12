from django.shortcuts import render
import requests
import pandas as pd    
from pandas.io.json import json_normalize
import json

# Create your views here.
def collections(request):
    '''

    '''
    url = "https://swapi.dev/api/planets"
    res = requests.get(url)
    json_data = json.loads(res.text)
    planets = json_normalize(json_data, record_path =['results'])
    next_page = json_data['next']
    frames = [planets]
    while next_page is not None:
        res = requests.get(next_page)
        json_data = json.loads(res.text)
        next_page = json_data['next']
        print(next_page)
        nplanets = json_normalize(json_data, record_path =['results'])
        frames.append(nplanets)
    all_planets = pd.concat(frames)
    all_planets_short = all_planets[['name','url']]
    all_planets_short.rename(columns={"name": "homeworld name", "url": "homeworld"}, inplace=True)
    all_planets_short
    
    '''

    '''
    purl = "https://swapi.dev/api/people"
    pres = requests.get(purl)
    pjson_data = json.loads(pres.text)
    people = json_normalize(pjson_data, record_path =['results'])
    pnext_page = pjson_data['next']
    pframes = [people]
    while pnext_page is not None:
        pres = requests.get(pnext_page)
        pjson_data = json.loads(pres.text)
        pnext_page = pjson_data['next']
        new_people = json_normalize(pjson_data, record_path =['results'])
        pframes.append(new_people)
    all_people = pd.concat(pframes)
    all_people_short = all_people[['name','height','mass','hair_color','skin_color','eye_color','birth_year','gender','homeworld','url']]
    all_people_short

    out_df = pd.merge(all_people_short, all_planets_short,  how='left', left_on=['homeworld'], right_on = ['homeworld'])
    df_html = out_df.to_html(border=1, classes='table table-striped table-bordered table-sm')

    new_context = {'df_html':df_html}
    return render(request, 'swapi/collections.html', new_context)