#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\semantic_clustering\semantic_clustering.py

from tqdm import tqdm
from pathlib import Path
from top2vec import Top2Vec
# import numpy as np
import pandas as pd
import numpy as np
# from sklearn.cluster import KMeans
# from numpy.linalg import norm
# from transformers import AutoTokenizer, AutoModel
# from transformers import logging
# import seaborn as sns
# from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Setting environment
# logging.set_verbosity_error()
# sns.set()
tqdm.pandas()

REMOVE_DUPLICATES = True


def run_clustering_steps(
        asreview_data_object,
        output_file,
        transformer='allenai/scibert_scivocab_uncased'):

    # load data
    print("Loading data...")
    # data = pd.DataFrame({
    #     "title": asreview_data_object.title,
    #     "abstract": asreview_data_object.abstract,
    #     "included": asreview_data_object.included,
    #     # "url": asreview_data_object.url,
    # })
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

    topic_nums, topic_score, topics_words, word_scores = model.get_documents_topics(documents_ids)
    # topic_nums, _, _, _ = model.get_documents_topics(documents_ids)

    # run t-sne
    # print("Running t-SNE...")
    # tsne = TSNE(n_components=3,
    #     max_iter=1000,
    #     perplexity=6,
    #     n_jobs=4,
    #     learning_rate=2000,
    #     early_exaggeration=12).fit_transform(model.document_vectors)

    # create file for use in interactive dashboard
    print("Creating file {0}...".format(output_file))
    # data['x'] = tsne[:, 0]
    # data['y'] = tsne[:, 1]
    # data['z'] = tsne[:, 2]
    data['cluster_id'] = topic_nums

    # data[['x', 'y', 'z']].to_csv(output_file_1, index=None, header=False, sep='\t')
    output_file_path = Path(output_file)
    np.savetxt(output_file, model.document_vectors, delimiter='\t')
    data.to_csv(output_file_path.parent / (output_file_path.stem + '_metadata' + output_file_path.suffix), index=None, sep='\t')

