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
`gramophone` is implemented in Python. In the following, we assume a working Python 3 (Version ≥ 3.4) installation.

### virtualenv

Using [`virtualenv`](https://virtualenv.pypa.io/en/stable/) is highly recommended, although not strictly necessary for installing `gramophone`. It can be installed via

```console
$ [sudo] pip install virtualenv
```
