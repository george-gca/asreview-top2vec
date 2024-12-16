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

Using `-f` will process a file and store the results in the file specified in `-o`. `--reduce_dimensionality` will reduce the dimensionality of the data to 5D, `--remove_abstracts` will remove abstracts from the data, and `--remove_urls` will remove urls from the data.

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

Then, open a browser and go to [`http://localhost:6006/`](http://localhost:6006/). If the browser doesn't show anything, refresh it (F5) so that the data is loaded.

## License

MIT license
