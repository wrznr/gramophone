# -*- coding: utf-8 -*-

import pywrapfst as fst
import regex as re

class Aligner:

    def __init__(self, mapping=None):
        """
        The constructor.

        Maybe called with or without a mapping.
        """

        self.clear()
        if mapping:
            self.load(mapping)

    def clear(self):
        """
        Clears all internal data.
        """

        self.syms = fst.SymbolTable()
        self.E = fst.Fst()
        self.Ig = fst.Fst()
        self.Ip = fst.Fst()
        self.Ip_r = re.compile(u"")

        self.status = 0

    def chain(self,g):
        """
        Constructs a (letter) chain transducer for a string.
        """
        
        t = fst.Fst()
        if self.status > 0:
            t.set_input_symbols(self.syms)
            t.set_output_symbols(self.syms)
            src = t.add_state()
            t.set_start(src)
            for c in g:
                dest = t.add_state()
                t.add_arc(src,fst.Arc(self.syms.find(c), self.syms.find(c), "0", dest))
                src = dest
            t.set_final(dest)
        return t

    def segment(self,g):
        '''
        Generate possible segmentations for a string represented as a transducer
        '''

        t2 = self.chain(g)
        return fst.compose(t2,self.Ig)

    def expand(self,g):
        '''
        Generate possible transcriptions for a string represented as a transducer
        '''

        t2 = self.chain(g)
        return fst.compose(t2,self.Ip)

    def align(self,g,p):
        '''
        Aligns a grapheme and phoneme sequence pair.
        '''

        t3 = self.segment(g)
        t3.project(project_output=True)

        t4 = self.expand(p)
        t4.project(project_output=True)

        if t4.num_arcs(t4.start()) == 0:
            sys.stderr.write(u"Empty expansion: %s %s\n" % (g, p))
            return fst.Fst()

        t5 = fst.compose(t3,self.E)
        t6 = fst.compose(t5,t4)

        return t6

    def extract_alignments(self,alignment_fst):
        '''
        Extracts all alignments encoded in an alignment fst.
        '''
        in_segs = []
        out_segs = []

        paths = self.enumerate_paths(alignment_fst.start(),[],[],alignment_fst)

        for path in paths:
            cur_in = u""
            cur_out = u""
            for arc in path:
                isym = self.syms.find(arc.ilabel).decode("utf-8")
                osym = self.syms.find(arc.olabel).decode("utf-8")
                if isym == u'|':
                    in_segs.append(cur_in)
                    cur_in = u""
                elif isym != u'ε':
                    cur_in += isym
                if osym == u'µ':
                    out_segs.append(cur_out)
                    cur_out = u""
                elif osym != u'ε':
                    cur_out += osym
            break

        return [in_segs,out_segs]

    def enumerate_paths(self,state,path,paths,fsm):
        '''
        Returns a list of all paths from a given state to a final state.
        '''

        if fsm.final(state).to_string() == b'0':
            paths += [path]
        for arc in fsm.arcs(state):
            new_path = path
            new_path.append(arc)
            paths = self.enumerate_paths(arc.nextstate, new_path, paths, fsm)
        return paths
        

    def load(self,mapping):
        """
        Loads a mapping.

        This function loads an alignment
        scheme and fills all internal data
        structures.
        """

        if self.status != 0:
            self.clear()

        # local variables
        g_set = {}
        p_set = {}

        
        # start/final state E
        zero_E = self.E.add_state()
        self.E.set_start(zero_E)
        self.E.set_final(zero_E)

        # start/final state Ig
        zero_Ig = self.Ig.add_state()
        self.Ig.set_start(zero_Ig)
        self.Ig.set_final(zero_Ig)

        # start/final state Ip
        zero_Ip = self.Ip.add_state()
        self.Ip.set_start(zero_Ip)
        self.Ip.set_final(zero_Ip)

        # designated state E
        one = self.E.add_state()

        # "return" arc E
        self.syms.add_symbol(u'ε')
        self.syms.add_symbol(u'µ')
        self.syms.add_symbol(u'|')
        self.E.add_arc(one, fst.Arc(self.syms.find(u'ε'), self.syms.find(u'µ'), "0", zero_E))
        
        # interpret mapping
        with open(str(mapping),"r") as f:
            mapping_data = f.read()
            for line in mapping_data.split(u"\n"):
                fields = line.split(u"\t")
                if len(fields) < 2:
                    continue

                # add previously unseen graph sequence
                if not fields[0] in g_set:
                    dst_E = zero_E
                    dst_I = zero_Ig
                    for c in fields[0]:
                        if not c in self.syms:
                            self.syms.add_symbol(c)

                        # editor arc
                        src_E = dst_E
                        dst_E = self.E.add_state()
                        self.E.add_arc(src_E, fst.Arc(self.syms.find(c), self.syms.find(u'ε'), "0", dst_E))

                        # Ig arc
                        src_I = dst_I
                        dst_I = self.Ig.add_state()
                        self.Ig.add_arc(src_I, fst.Arc(self.syms.find(c), self.syms.find(c), "0", dst_I))

                    g_set[fields[0]] = dst_E
                    self.Ig.add_arc(dst_I, fst.Arc(self.syms.find(u'ε'), self.syms.find(u'|'), "0", zero_Ig))

                # add previously unseen phon sequence
                if not fields[1] in p_set:
                    src_E = self.E.add_state()
                    src_I = zero_Ip
                    p_set[fields[1]] = src_E
                    for c in fields[1][:-1]:
                        if not c in self.syms:
                            self.syms.add_symbol(c)

                        # editor arc
                        dst_E = self.E.add_state()
                        self.E.add_arc(src_E, fst.Arc(self.syms.find(u'ε'), self.syms.find(c), "0", dst_E))
                        src_E = dst_E

                        # Ip arc
                        dst_I = self.Ip.add_state()
                        self.Ip.add_arc(src_I, fst.Arc(self.syms.find(c), self.syms.find(c), "0", dst_I))
                        src_I = dst_I

                    # last symbol
                    if not fields[1][-1] in self.syms:
                        self.syms.add_symbol(fields[1][-1])

                    # editor arc
                    self.E.add_arc(src_E, fst.Arc(self.syms.find(u'ε'), self.syms.find(fields[1][-1]), "0", one))

                    # Ip arc
                    dst_I = self.Ip.add_state()
                    self.Ip.add_arc(src_I, fst.Arc(self.syms.find(fields[1][-1]), self.syms.find(fields[1][-1]), "0", dst_I))
                    self.Ip.add_arc(dst_I, fst.Arc(self.syms.find(u'ε'), self.syms.find(u'µ'), "0", zero_Ip))
                self.E.add_arc(g_set[fields[0]], fst.Arc(self.syms.find(u'|'), self.syms.find(u'ε'), "0", p_set[fields[1]]))

        self.E.set_input_symbols(self.syms)
        self.E.set_output_symbols(self.syms)
        self.Ig.set_input_symbols(self.syms)
        self.Ig.set_output_symbols(self.syms)
        self.Ip.set_input_symbols(self.syms)
        self.Ip.set_output_symbols(self.syms)
        
        self.Ip_r = re.compile(u"%s" % u"|".join(u"%s" % re.escape(pat) for pat in sorted(list(p_set), key=len, reverse=True)), re.UNICODE)

        self.status = 1
        self.E.draw('/tmp/e.dot')
        self.Ig.draw('/tmp/g.dot')
        self.Ip.draw('/tmp/p.dot')
        #assert(None)
