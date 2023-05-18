from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pymongo
from streamlit_chat import message

'''
# Viewer of Chat Experinemts Manager
'''

myclient = pymongo.MongoClient('mongodb://mongo:27017/')


def make_nested_dict_flat(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(make_nested_dict_flat(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append(
                (new_key, 'list (not parsed)'))
        else:
            items.append((new_key, v))
    return dict(items)


db = myclient.train_log

cursor = db['metrics'].find(sort=[('_id', -1)])
metrics_dict = {}
for document in cursor:
    name = document['name']
    if isinstance(name, str) and len(document['values']) == 1:
        if not document['run_id'] in metrics_dict:
            metrics_dict[document['run_id']] = {}
        metrics_dict[
            document['run_id']
        ][f'metrics_{name}'] = document['values'][0]

runs = []
cursor = db['runs'].find(sort=[('_id', -1)])
for document in cursor:
    metric_dict_for_doc = {}
    run_id = document['_id']
    if run_id in metrics_dict:
        for key in metrics_dict[run_id]:
            metric_dict_for_doc[key] = metrics_dict[run_id][key]
    doc_dict = {
        'run_id': run_id,
        'status': document['status'],
        **metric_dict_for_doc,
        **make_nested_dict_flat(document['config'])
    }
    runs.append(doc_dict)
run_df = pd.DataFrame.from_dict(runs).set_index('run_id')
st.dataframe(run_df)

# User input
exp_id = st.text_input('Enter experiment id for its detail')
# Check if user has entered a name
if exp_id:
    st.table(run_df.loc[int(exp_id)])
    cursor = db['iterations'].find(
        {'run_id': int(exp_id)}, sort=[('iteration', 1)])
    iterations = []
    for document in cursor:
        flat_dict = make_nested_dict_flat(document)
        del flat_dict['_id']
        del flat_dict['run_id']
        iterations.append(flat_dict)
    if len(iterations) > 0:
        iteration_df = pd.DataFrame.from_dict(
            iterations).set_index('iteration')
        st.table(iteration_df)

        st.altair_chart(
            alt.Chart(iteration_df.rename(
                columns={'result.score': 'score'}))
            .mark_bar()
            .encode(
                alt.X('score:Q'),
                y='count()'))

    itr = st.text_input('Enter iteration for chat log')
    if itr:
        cursor = db['conversations'].find(
            {'run_id': int(exp_id), 'iteration': int(itr)}
        )
        for doc in cursor:
            for conv in doc['conversation_log']:
                if conv['text'] is not None:
                    message(conv['text'],
                            is_user=conv['sender_type'] == 'user')
