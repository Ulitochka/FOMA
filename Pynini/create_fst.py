import os
import itertools
import distutils.dir_util

import pynini
from pynini import *


class AttributeGrammarFST:

    def __init__(self):

        self.path = os.path.join(os.path.dirname(__file__) + '/bin_files/')

        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        splitters = ['x', 'X', ' х ']
        cyrillic_chars = [chr(i) for i in range(1024, 1123)]
        latin_chars = [chr(i) for i in range(1, 91)] + [chr(i) for i in range(94, 128)]
        latin_diacr_chars = [chr(i) for i in range(128, 256)]
        escaped_chars = ['\\[', '\\]', '\\\\', '«', '»']

        alphabet = latin_chars + cyrillic_chars + escaped_chars

        self.bigrams = [''.join(el) + ' ' for el in list(itertools.product(digits, alphabet))]
        self.cable_splitters = pynini.union(*splitters).optimize()
        self.cable_floats = pynini.union(' . ').optimize()
        self.cable_length_0 = pynini.union(' мм ').optimize()
        self.cable_length_1 = pynini.union(' м', '[EOS]').optimize()
        self.cable_digits = pynini.union(*digits).star.optimize()
        self.ngram_comb = pynini.union(*self.bigrams).optimize()
        self.alphabet = pynini.union(*alphabet).closure().optimize()

        self.rules = None

    def singularize(self, string, rules):
        results = []
        for r in rules:
            results.append((r, pynini.shortestpath(pynini.compose(string.strip(), rules[r])).stringify()))
        return sorted(results)

    def save(self, rules, block_name='default'):
        new_path = os.path.join(self.path, block_name)
        distutils.dir_util.mkpath(new_path)

        for r in rules:
            self.rules[r].draw(os.path.join(new_path, '%s.dot' % (r,)))
            self.rules[r].write(os.path.join(new_path, '%s.fst' % (r,)))

    def load(self, path):
        f = Fst()
        return f.read(path)


class CableGrammar(AttributeGrammarFST):

    def __init__(self):
        super().__init__()

        attr_map_0 = pynini.transducer(self.cable_digits, '#жил')
        attr_map_1 = pynini.transducer(self.cable_digits, 'Сечение_кабеля')
        attr_map_2 = pynini.transducer(self.cable_digits, 'Длина_кабеля')
        attr_map_3 = pynini.transducer('.', 'Сечение_кабеля')

        attr_map_0_rc = self.cable_splitters
        attr_map_0_lc = pynini.union(" ")
        attr_map_0_s = pynini.cdrewrite(attr_map_0, attr_map_0_lc, attr_map_0_rc, self.alphabet).optimize()

        attr_map_1_rc = self.cable_splitters
        attr_map_1_lc = self.cable_floats
        attr_map_1_s = pynini.cdrewrite(attr_map_1, attr_map_1_rc, attr_map_1_lc, self.alphabet).optimize()

        attr_map_2_rc = self.cable_floats
        attr_map_2_lc = self.cable_length_0
        attr_map_2_s = pynini.cdrewrite(attr_map_1, attr_map_2_rc, attr_map_2_lc, self.alphabet).optimize()

        attr_map_3_rc = self.cable_length_0
        attr_map_3_lc = self.cable_length_1
        attr_map_3_s = pynini.cdrewrite(attr_map_2, attr_map_3_rc, attr_map_3_lc, self.alphabet).optimize()

        attr_map_4_rc = self.cable_digits
        attr_map_4_lc = self.cable_digits
        attr_map_4_s = pynini.cdrewrite(attr_map_3, attr_map_4_rc, attr_map_4_lc, self.alphabet).optimize()

        attr_map_5_rc = self.cable_splitters
        attr_map_5_lc = self.cable_length_0
        attr_map_5_s = pynini.cdrewrite(attr_map_1, attr_map_5_rc, attr_map_5_lc, self.alphabet).optimize()

        attr_map_comp_0 = pynini.compose(pynini.compose(attr_map_1_s, attr_map_2_s).optimize(), attr_map_4_s).optimize()

        self.rules = {
            'жилы': attr_map_0_s,
            'сечение_кабеля_0': attr_map_comp_0,
            'длина_кабеля': attr_map_3_s,
            'сечение_кабеля_1': attr_map_5_s
        }


class CableInfoGrammar(AttributeGrammarFST):

    def __init__(self):

        super().__init__()

        attr_map_0 = pynini.transducer(self.cable_digits, '#жил')
        attr_map_1 = pynini.transducer(self.cable_digits, 'Длина_кабеля')
        attr_map_2 = pynini.transducer(self.cable_digits, 'Диаметр')
        attr_map_3 = pynini.transducer(self.cable_digits, '#соединительных_проводов')
        attr_map_4 = pynini.transducer(' . ', ' Диаметр ')

        attr_map_0_lc = self.ngram_comb
        attr_map_0_rc = self.cable_splitters
        attr_map_0_s = pynini.cdrewrite(attr_map_0, attr_map_0_lc, attr_map_0_rc, self.alphabet).optimize()

        attr_map_3_lc = self.cable_splitters
        attr_map_3_rc = self.cable_splitters
        attr_map_3_s = pynini.cdrewrite(attr_map_3, attr_map_3_lc, attr_map_3_rc, self.alphabet).optimize()

        attr_map_2_lc = self.cable_floats
        attr_map_2_rc = self.cable_length_0
        attr_map_2_s = pynini.cdrewrite(attr_map_2, attr_map_2_lc, attr_map_2_rc, self.alphabet).optimize()

        attr_map_4_lc = self.cable_splitters
        attr_map_4_rc = self.cable_floats
        attr_map_4_s = pynini.cdrewrite(attr_map_2, attr_map_4_lc, attr_map_4_rc, self.alphabet).optimize()

        attr_map_5_lc = self.cable_digits
        attr_map_5_rc = self.cable_digits
        attr_map_5_s = pynini.cdrewrite(attr_map_4, attr_map_5_lc, attr_map_5_rc, self.alphabet).optimize()

        attr_map_6_rc = self.cable_length_0
        attr_map_6_lc = self.cable_length_1
        attr_map_6_s = pynini.cdrewrite(attr_map_1, attr_map_6_rc, attr_map_6_lc, self.alphabet).optimize()

        attr_map_comp_0 = pynini.compose(pynini.compose(attr_map_2_s, attr_map_4_s).optimize(), attr_map_5_s).optimize()

        self.rules = {
            'жилы': attr_map_0_s,
            'соединительные_провода': attr_map_3_s,
            'диаметр': attr_map_comp_0,
            'длина_кабеля': attr_map_6_s
        }


if __name__ == '__main__':

    rules_grammars = {
        'Кабели силовые': CableGrammar(),
        'Кабели информационные': CableInfoGrammar()
    }

    for rb in rules_grammars:
        rules_grammars[rb].save(rules_grammars[rb].rules, block_name=rb)
