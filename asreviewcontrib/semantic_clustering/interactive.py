#!/usr/bin/python
# -*- coding: utf-8 -*-
# Path: asreviewcontrib\semantic_clustering\interactive.py

import numpy as np
from tensorboard.plugins import projector
from pathlib import Path


def run_app(filepath, metadata):
    """Function to be called to create the tensorboard projector config"""
    config = projector.ProjectorConfig()
    embedding = config.embeddings.add()
    logdir = Path(filepath).parent
    embedding.tensor_name = "Teste"
    embedding.metadata_path = str(Path(metadata).relative_to(logdir))
    embedding.tensor_path = str(Path(filepath).relative_to(logdir))
    projector.visualize_embeddings(logdir, config)

