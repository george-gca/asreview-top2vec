#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\top2vec\top2vec_data.py

from itertools import islice
from pathlib import Path

import pandas as pd
from asreview import ASReviewData
from top2vec import Top2Vec

# Setting environment
REMOVE_DUPLICATES = True


def gather_topics_information(
        asreview_data_object: ASReviewData,
        model_file: str,
        n: int = 10):

    # load data
    print("Loading data...")
    model = Top2Vec.load(model_file)
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

    topic_sizes, _ = model.get_topic_sizes()
    topic_words, word_scores, topic_nums = model.get_topics()

    # store information about the topics
    topics_data = []
    topics_words = []
    output_dir = Path('top2vec/').expanduser()
    output_dir.mkdir(exist_ok=True)

    for topic_num, topic_size, words, scores in zip(topic_nums, topic_sizes, topic_words, word_scores):
        print(f'\nTopic {topic_num} has {topic_size} documents')
        topics_data.append({'Topic': topic_num, 'Documents': topic_size})

        topic_word_scores = [f'{score:.3f} - {word}' for score, word in zip(islice(scores, n), words)]
        topic_word_scores_str = '\n\t'.join(topic_word_scores)
        print(f'{n} most important words:\n\t{topic_word_scores_str}')

        for score, word in zip(scores, words):
            topics_words.append({'Word': word, 'Score': score, 'Topic': topic_num})

    suffix = Path(model_file).stem

    df_topics = pd.DataFrame(topics_data)
    df_topics_words = pd.DataFrame(topics_words)
    df_topics.to_csv(output_dir / f'topics_{suffix}.csv', index=False)
    df_topics_words.to_csv(output_dir / f'topics_words_{suffix}.csv', index=False)
