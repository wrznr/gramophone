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
            return "\n".join("%s\t%s" % (pair[0], pair[1]) for pair in io_tuples)

        elif fmt == "json":
            result = []
            for pair in io_tuples:
                result.append({"word" : pair[0], "hyphenation" : pair[1]})
            return json.dumps(result)
        else:
            return str(io_tuples)
