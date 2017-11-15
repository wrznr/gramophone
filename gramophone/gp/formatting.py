# -*- coding: utf-8 -*-

import json

class Formatter:

    def __init__(self):
        """
        The constructor.
        """
        pass

    def encode(self, io_tuples, fmt):

        fmt = fmt.strip().lower()

        if fmt == "txt":
            return "\n".join("%s\t%s" % (triple[0], triple[1]) for triple in io_tuples)

        elif fmt == "json":
            result = []
            for triple in io_tuples:
                result.append({"word" : triple[0], "phonology" : triple[1], "probability" : "%.5f" % triple[2]})
            return json.dumps(result)
        else:
            return str(io_tuples)
