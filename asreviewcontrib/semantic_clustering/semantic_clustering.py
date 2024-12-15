#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\semantic_clustering\semantic_clustering.py

from pathlib import Path

import numpy as np
from asreview import ASReviewData
from top2vec import Top2Vec
from sklearn.manifold import TSNE

# Setting environment
REMOVE_DUPLICATES = True


def run_clustering_steps(
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
            print("Size before removing duplicates is {0}".format(len(data)))
            data = data[data['dup'].isna()]
            print("Size after removing duplicates is {0}".format(len(data)))
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
        workers=4,
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

    # create file for use in interactive dashboard
    print("Creating file {0}...".format(output_file))
    data['cluster_id'] = topic_nums

    output_file_path = Path(output_file)

    if remove_abstracts:
        data.drop('abstract', axis=1, inplace=True)

    if remove_urls:
        data.drop('url', axis=1, inplace=True)

    data.to_csv(output_file_path.parent / (output_file_path.stem + '_metadata' + output_file_path.suffix), index=None, sep='\t')

    if reduce_dimensionality:
        np.savetxt(output_file, tsne, delimiter='\t')
    else:
        np.savetxt(output_file, model.document_vectors, delimiter='\t')

