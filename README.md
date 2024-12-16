# ASReview Top2Vec
This repository contains the Top2Vec plugin for [ASReview](https://github.com/asreview/asreview). It applies [Top2Vec](https://github.com/ddangelov/Top2Vec) clustering to an [ASReview data object](https://asreview.readthedocs.io/en/stable/generated/asreview.ASReviewData.html), in order to cluster records based on semantic differences. The end result can be visualized in an interactive dashboard with the help of [TensorBoard's Embedding Projector](https://projector.tensorflow.org/).

![Embedding projector](/docs/top2vec_tensorboard.gif)

## Installation

The packaged is called `asreview-top2vec` and can be installed from the
download folder with:

```shell
pip install .
```

or from the command line directly with:

```shell
python -m pip install git+https://github.com/george-gca/asreview-top2vec.git
```

If you want to install the package in development mode, i.e. you can edit the package and test it without having to reinstall it, use the following:

```shell
pip install -e .
```

### Commands

For help use:

```shell
asreview top2vec -h
asreview top2vec --help
```

Other options are:

```shell
asreview top2vec -f <input> -o <output.tsv>
asreview top2vec --filepath <input> --output <output.tsv>
```

```shell
asreview top2vec -f <input> -o <output.tsv> --reduce_dimensionality --remove_abstracts --remove_urls
```

```shell
asreview top2vec -c <output.tsv> -m <output_metadata.tsv>
asreview top2vec --create_projector_config <output.tsv> --metadata <output_metadata.tsv>
```

```shell
asreview top2vec -v
asreview top2vec --version
```

## Usage

The functionality of the Top2Vec extension is implemented in a [subcommand extension](https://asreview.readthedocs.io/en/stable/extensions_dev.html#subcommand-extensions). The following commands can be run:

### Processing

In the processing phase, a dataset is processed and clustered for use in the interactive interface. The following options are available:

```shell
asreview top2vec -f <input.tsv or url> -o <output_file.tsv> --reduce_dimensionality --remove_abstracts --remove_urls
```

Using `-f` will process a file and store the results in the file specified in `-o`. `--reduce_dimensionality` will reduce the dimensionality of the data to 5D, `--remove_abstracts` will remove abstracts from the data, and `--remove_urls` will remove urls from the data. Note that usually you won't need to use `--reduce_dimensionality`, as the Embedding Projector can handle high-dimensional data and display it in 3D or 2D. This is only useful if you have a really large amount of data. The `--remove_abstracts` and `--remove_urls` options are useful when the abstracts and urls are not needed in the visualization.

Top2Vec uses an [`ASReviewData` object](https://asreview.readthedocs.io/en/stable/generated/asreview.ASReviewData.html), and can handle files, urls and benchmark sets:

```shell
asreview top2vec -f benchmark:van_de_schoot_2017 -o output.tsv
asreview top2vec -f van_de_Schoot_2017.tsv -o output.tsv
asreview top2vec -f https://raw.githubusercontent.com/george-gca/ai_conferences_info/refs/heads/main/ASReview/NeurIPS/neurips_2020.tsv
```

If an output file is not specified, `output.tsv` is used as output file name. The name of the generated metadata file is the same as the output file, but with `_metadata` appended to the name, as `output_metadata.tsv`. This metadata is used for the visualization in the [TensorBoard's Embedding Projector](https://projector.tensorflow.org/). It is recommended to create a directory to store the output files, as the command will generate the original output file, the metadata, and also the saved top2vec model. The following command will create a directory and store the output files in it:

```shell
mkdir output_dir
asreview top2vec -f van_de_Schoot_2017.tsv -o output_dir/output.tsv
```

### Creating a projector config

The projector config is created with the following command:

```shell
asreview top2vec -c <output.tsv> -m <output_metadata.tsv>
```

This command will create a projector config file that can be used to visualize the data in the local [TensorBoard's Embedding Projector](https://projector.tensorflow.org/). The metadata file is used to add additional information to the visualization. Note that this command does not run a projector, but only creates the config file. Also, this step is not needed if you'll use the online version of the Embedding Projector.

### Embedding Projector

You can either use the online [TensorBoard's Embedding Projector](https://projector.tensorflow.org/) to visualize the data, using both the data and metadata files created with the `-f` command, or use a local [Tensorboard](https://www.tensorflow.org/tensorboard) installation to visualize the data. The following command will start a local Tensorboard server:

```shell
tensorboard --logdir=./output_dir/
```

Then, open a browser and go to [`http://localhost:6006/#projector`](http://localhost:6006/#projector). If the browser doesn't show anything, refresh it (F5) so that the data is loaded. For more information about the embedding projector, see the official [TensorBoard's Embedding Projector](https://research.google/blog/open-sourcing-the-embedding-projector-a-tool-for-visualizing-high-dimensional-data/) release post.

At first opening, the Embedding Projector will show the data in a 3D visualization, like this one:

![Embedding projector first load](/docs/embedding_projector_01.png)

The Top2Vec model automatically assigns topics for each document. You can visualize this information by enabling the `Color by` option and selecting the `cluster_id` field. This will color the data points according to the topic assigned by the Top2Vec model. The following image shows the data colored by the topic field:

![Selecting colored by topic in Embedding projector](/docs/embedding_projector_02.png)

![Embedding projector colored by topic](/docs/embedding_projector_03.png)

By default, the Embedding Projector shows the data in 3D using the PCA dimensionality reduction algorithm. You can change this algorithm by selecting one of the options in the lower left. For example, selecting the t-SNE algorithm will show the data in 3D:

![Selecting t-SNE in Embedding projector](/docs/embedding_projector_04.png)

If you select a data point, you can see its nearest neighbours in the original space, and also some information about the document in the right panel. This information is taken from the metadata file. The following image shows the information about a document:

![Embedding projector document information](/docs/embedding_projector_05.png)

### Fetching topics information

The topics information can be fetched from the Top2Vec model using the following command:

```shell
asreview top2vec -t <input.tsv or url> --model_file <top2vec model file> -w <10>
```

This command will fetch the topics information from the trained Top2Vec model using the input file and write it both to the console and to some files. The `-w` option specifies the number of words to show for each topic. The model file is the file generated by the processing command and the input file must be the same input given during the processing stage. The output files generated in this process are stored as `top2vec/topics_{suffix}.csv` and `top2vec/topics_words_{suffix}.csv`, where `{suffix}` is the name of the input file without the extension.

An example of its console output given the input `https://raw.githubusercontent.com/george-gca/ai_conferences_info/refs/heads/main/ASReview/NeurIPS/neurips_2020.tsv` and the top2vec model trained from this file is:

```txt
Topic 0 has 370 documents
10 most important words:
        0.658 - bounds
        0.650 - sqrt
        0.648 - establish
        0.627 - smooth
        0.627 - convex
        0.626 - analysis
        0.615 - rate
        0.609 - constant
        0.608 - optimal
        0.607 - bound

Topic 1 has 334 documents
10 most important words:
        0.668 - images
        0.632 - object
        0.616 - image
        0.615 - visual
        0.597 - supervision
        0.593 - available
        0.591 - dataset
        0.586 - com
        0.578 - art
        0.576 - self supervision

Topic 2 has 189 documents
10 most important words:
        0.770 - reinforcement
        0.739 - agent
        0.690 - policy
        0.681 - policies
        0.670 - rl
        0.667 - environment
        0.653 - episodic reinforcement
        0.650 - actions
        0.634 - optimal policies
        0.629 - deep reinforcement

Topic 3 has 155 documents
10 most important words:
        0.729 - resnet
        0.694 - cifar
        0.671 - imagenet
        0.604 - accuracy
        0.601 - pruning
        0.596 - on cifar
        0.590 - comparable
        0.584 - smaller
        0.577 - cifar cifar
        0.567 - comparable accuracy

Topic 4 has 123 documents
10 most important words:
        0.647 - dynamical
        0.615 - dynamical system
        0.612 - dynamical systems
        0.596 - here
        0.589 - brain
        0.563 - series forecasting
        0.560 - capture
        0.557 - time series
        0.554 - connections between
        0.551 - neural

Topic 5 has 119 documents
10 most important words:
        0.677 - variational
        0.676 - posterior distribution
        0.672 - monte
        0.648 - posterior
        0.644 - posterior distributions
        0.604 - carlo
        0.595 - monte carlo
        0.594 - inference
        0.578 - exponential family
        0.567 - new family

Topic 6 has 109 documents
10 most important words:
        0.708 - width
        0.656 - infinite width
        0.648 - bit width
        0.639 - network width
        0.629 - limit
        0.623 - blur kernel
        0.618 - finite width
        0.615 - reproducing kernel
        0.606 - kernel ntk
        0.591 - tangent kernel

Topic 7 has 107 documents
10 most important words:
        0.733 - combinatorial
        0.704 - combinatorial optimization
        0.633 - solving
        0.606 - semidefinite programming
        0.573 - programming
        0.543 - solution
        0.543 - solve
        0.537 - problems
        0.533 - solutions
        0.531 - hard

Topic 8 has 92 documents
10 most important words:
        0.769 - graph
        0.754 - graphs
        0.745 - gnns
        0.735 - gnns have
        0.728 - networks gnns
        0.704 - nodes
        0.666 - graph neural
        0.665 - gnn
        0.656 - node
        0.645 - graph sat

Topic 9 has 77 documents
10 most important words:
        0.760 - attacks
        0.715 - adversarial
        0.715 - adversarial attacks
        0.706 - adversarial attack
        0.692 - attack
        0.680 - robustness
        0.672 - against
        0.670 - adversarial robustness
        0.662 - robustness against
        0.651 - adversarial perturbations

Topic 10 has 68 documents
10 most important words:
        0.686 - horizon
        0.659 - planning horizon
        0.648 - time horizon
        0.639 - near
        0.635 - reward free
        0.633 - optimal policies
        0.621 - near optimal
        0.621 - exploration
        0.617 - states
        0.613 - reward

Topic 11 has 61 documents
10 most important words:
        0.749 - group fairness
        0.741 - fairness
        0.737 - groups
        0.645 - group
        0.642 - individual fairness
        0.641 - fairness constraints
        0.550 - metrics
        0.546 - clustering
        0.521 - sensitive
        0.509 - empirically validate

Topic 12 has 60 documents
10 most important words:
        0.749 - causal
        0.747 - causal effects
        0.743 - treatment effect
        0.719 - causal effect
        0.717 - structural causal
        0.701 - treatment effects
        0.674 - treatment
        0.669 - causal inference
        0.666 - effect estimation
        0.651 - effect

Topic 13 has 56 documents
10 most important words:
        0.824 - normalizing
        0.819 - normalizing flows
        0.796 - flows
        0.779 - normalizing flow
        0.640 - likelihood
        0.613 - optical flow
        0.604 - transformations
        0.601 - flow
        0.597 - gradient flow
        0.578 - vaes

Topic 14 has 51 documents
10 most important words:
        0.787 - gans
        0.779 - gan
        0.656 - networks gans
        0.596 - generator
        0.577 - text generation
        0.571 - generation
        0.546 - generative
        0.522 - generated
        0.520 - image generation
        0.479 - generative adversarial

Topic 15 has 50 documents
10 most important words:
        0.786 - domain adaptation
        0.775 - source domain
        0.765 - domain
        0.743 - target domain
        0.711 - adaptation
        0.707 - target domains
        0.701 - domain invariant
        0.676 - domain specific
        0.665 - source
        0.620 - target

Topic 16 has 45 documents
10 most important words:
        0.780 - meta
        0.727 - continual
        0.661 - tasks
        0.658 - meta learning
        0.653 - continual learning
        0.612 - adapt
        0.542 - task
        0.496 - task agnostic
        0.474 - framework
        0.468 - adaptation
```

## License

MIT license
