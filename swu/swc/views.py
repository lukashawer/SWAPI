from django.shortcuts import render, redirect, get_object_or_404
import requests
import pandas as pd    
from pandas.io.json import json_normalize
from django.core.files.base import ContentFile
from swc.models import Document
from datetime import datetime
import json

# Create your views here.
def refres_collection(request):
    '''
    Retrieving all planets in a loop dropping unnecessary columns
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
        nplanets = json_normalize(json_data, record_path =['results'])
        frames.append(nplanets)
    all_planets = pd.concat(frames)
    all_planets_short = all_planets[['name','url']]
    all_planets_short.rename(columns={"name": "homeworld", "url": "homeworld_url"}, inplace=True)
    
    '''
    Retrieving all characters in a loop and dropping unnecessary columns
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
    all_people_short.rename(columns={"homeworld": "homeworld_url","url": "character_url"}, inplace=True)

    '''
    Joining both tables and saving them to csv and DB
    '''
    out_df = pd.merge(all_people_short, all_planets_short,  how='left', left_on=['homeworld_url'], right_on = ['homeworld_url'])
    
    temp_file = ContentFile(out_df.to_csv(index=False, header=True, encoding="latin-1" , line_terminator='\n'))
    now = datetime.now()
    date_time_stamp = now.strftime("%m%d%Y_%H%M%S")
    file_name = 'Collection_' + date_time_stamp + '.csv'
    new_doc = Document()
    new_doc.filename.save(name=file_name, content=temp_file, save=False)
    new_doc.save()

    return redirect('swc:collections')

def collections(request):
    docs = Document.objects.all().order_by('-date')
    if docs.count() < 1:
        return redirect('swc:refres_collection')

    new_context = {'docs':docs}
    return render(request, 'swapi/collections.html', new_context)

def collection(request, id, rows):
    doc = get_object_or_404(Document, pk=id)
    next_v = rows+10
    if not doc:
        return redirect('swc:refres_collection')
    out_df = pd.read_csv(doc.filename.path, encoding="latin-1") 
    df_html = out_df.head(rows).to_html(border=1, classes='table table-striped table-bordered table-sm')

    new_context = {'df_html':df_html, 'next_v':next_v, 'collection':doc}
    return render(request, 'swapi/collection.html', new_context)

def grouping_stat(request, doc_id, new_q, curent_q=None):
    doc = get_object_or_404(Document, pk=doc_id)
    out_df = pd.read_csv(doc.filename.path, encoding="latin-1") 

    g_list = None
    if curent_q is not None:
        g_list = curent_q.split(',')
        if new_q in g_list: 
            g_list.remove(new_q)
        else:
            g_list.append(new_q)
    else:
        g_list = [new_q]

    if g_list is None or len(g_list) < 1:
        return redirect('swc:collection', doc_id, 200)

    col_list = list(out_df.columns.values)
    new_curent_q = ','.join(g_list)  
    ret_df = out_df.groupby(g_list).size().reset_index(name='counts')
    df_html = ret_df.to_html(border=1, classes='table table-striped table-bordered table-sm')

    new_context = {'df_html':df_html, 'collection':doc, 'curent_q':new_curent_q, 'groupings':col_list}
    return render(request, 'swapi/grouping.html', new_context)

