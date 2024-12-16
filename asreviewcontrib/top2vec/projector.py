#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\top2vec\projector.py

from pathlib import Path

from tensorboard.plugins import projector


def create_projector_config(data_path, metadata_path):
    """Function to be called to create the tensorboard projector config"""
    config = projector.ProjectorConfig()
    embedding = config.embeddings.add()
    data_path = Path(data_path)
    logdir = data_path.parent
    embedding.tensor_name = data_path.stem
    embedding.tensor_path = str(Path(data_path).relative_to(logdir))

    if metadata_path is not None and len(metadata_path) > 0:
        embedding.metadata_path = str(Path(metadata_path).relative_to(logdir))

    projector.visualize_embeddings(logdir, config)
