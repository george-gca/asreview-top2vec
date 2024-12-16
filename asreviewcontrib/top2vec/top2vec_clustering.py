#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\top2vec\top2vec_clustering.py

from multiprocessing import cpu_count
from pathlib import Path

import numpy as np
from asreview import ASReviewData
from top2vec import Top2Vec
from sklearn.manifold import TSNE

# Setting environment
REMOVE_DUPLICATES = True


def run_clustering(
        asreview_data_object: ASReviewData,
        output_file: str,
        reduce_dimensionality: bool=False,
        remove_abstracts: bool=False,
        remove_urls: bool=False):

    # load data
    print("Loading data...")
    data = asreview_data_object.to_dataframe().reset_index().drop(columns=['record_id'])

    # remove emptry abstracts
    data = data[data['abstract'] != '']

    if REMOVE_DUPLICATES:
        try:
            data["dup"] = asreview_data_object.df["duplicate_record_id"]
            print(f"Size before removing duplicates is {len(data)}")
            data = data[data['dup'].isna()]
            print(f"Size after removing duplicates is {len(data)}")
        except KeyError:
            pass

    # reset index
    data.reset_index(drop=True, inplace=True)

    # train top2vec model
    documents_ids = data['title'].to_list()

    model = Top2Vec(
        data['abstract'].to_list(),
        embedding_model='doc2vec',
        # speed='learn',
        ngram_vocab=True,
        split_documents=True,
        use_corpus_file=True,
        document_ids=documents_ids,
        # keep_documents=False,
        workers=cpu_count()//2,
    )

    # topic_nums, topic_score, topics_words, word_scores = model.get_documents_topics(documents_ids)
    topic_nums, _, _, _ = model.get_documents_topics(documents_ids)

    if reduce_dimensionality:
        # run t-sne
        print("Running t-SNE...")
        tsne = TSNE(n_components=5,
            max_iter=1000,
            perplexity=6,
            n_jobs=4,
            learning_rate=2000,
            early_exaggeration=12).fit_transform(model.document_vectors)

    # create files
    output_file_path = Path(output_file)
    metadata_file = output_file_path.parent / (output_file_path.stem + '_metadata' + output_file_path.suffix)
    data['cluster_id'] = topic_nums

    print(f"Creating files {output_file} and {metadata_file}...")

    if remove_abstracts and 'abstract' in data.columns:
        data.drop('abstract', axis=1, inplace=True)

    if remove_urls and 'url' in data.columns:
        data.drop('url', axis=1, inplace=True)

    # saving top2vec model
    model.save(output_file_path.parent / (output_file_path.stem + '_model'))
    data.to_csv(metadata_file, index=None, sep='\t')

    if reduce_dimensionality:
        np.savetxt(output_file, tsne, delimiter='\t')
    else:
        np.savetxt(output_file, model.document_vectors, delimiter='\t')

