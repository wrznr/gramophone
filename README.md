# gramophone /ˈɡɹæməˌfoʊ̯n/
grapheme-phoneme conversion and related stuff

## Description
`gramophone` is a package for hybrid grapheme-to-phoneme conversion using a set of heuristic mappings to determine admissible segmentations, a Conditional Random Field model for labelling candidate segmentations, and a language model over (grapheme,phoneme) segment-pairs to determine the optimal transcription.

We would appreciate `gramophone` users acknowledging its use in their publications. You can cite:

> Kay-Michael Würzner & Bryan Jurish. "A hybrid approach to grapheme-phoneme conversion."
> In Proceedings of the 12th International Conference on Finite State Methods and Natural Language Processing
> (Düsseldorf, Germany, 22nd - 24th June, 2015), 2015.

The full paper can be downloaded [here](http://www.aclweb.org/anthology/W/W15/W15-4811.pdf), and a BibTeX entry can be found [here](http://kaskade.dwds.de/~moocow/gramophone/wj2015gramophone.bib).

## License
The `gramophone` package is distributed under the terms of the [GNU Lesser General Public License (LGPL-v3)](http://kaskade.dwds.de/~moocow/gramophone/COPYING), which itself incorporates the terms and conditions of the [GNU General Public License](http://kaskade.dwds.de/~moocow/gramophone/COPYING.GPL-3).

## Installation
`gramophone` is implemented in Python. In the following, we assume a working Python (Version ≥ 2.7, for Python 3: Version ≥ 3.4) installation as well as a working C++ compiler.

### OpenFst
`gramophone` uses [`OpenFst`](http://www.openfst.org/twiki/bin/view/FST/) for constructing and applying finite-state transducers. In particular, the [Python interface](http://www.openfst.org/twiki/bin/view/FST/PythonExtension) is used. While the Python side can be installed via `pip`, the underlying C++ library has to be installed manually. The latest version of the Python interface **available at the Python package index** is 1.6.9. Obtain the corresponding sources from http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.9.tar.gz and follow the instructions shipped with the package. Make sure to use the `--enable-grm` option while configuring.

### virtualenv
Using [`virtualenv`](https://virtualenv.pypa.io/en/stable/) is highly recommended, although not strictly necessary for installing `gramophone`. It can be installed via:

```console
$ [sudo] pip install virtualenv
```

Create a virtual environement in a subdirectory of your choice (e.g. `env`) using

```console
$ virtualenv env
```

and activate it.

```console
$ . env/bin/activate
```

### Python requirements
`gramophone` uses various 3rd party Python packages which may be best installed using `pip`:

```console
(env) $ pip install -r requirements.txt
```

### Installation
Finally, you are ready to install the package:

```console
(env) $ pip install -e .
```
