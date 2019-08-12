import os
import re
import time
from tabulate import tabulate

from grammar_fst.Foma.foma import FST
from tools.data_loader import DataLoader
from tokenizer.tokenizer import Tokenizer

from dgisconfig import Config

import config


class ParserFST:

    def __init__(self, fst_name):

        self.path = os.path.join(os.path.dirname(__file__) + '/grammars/')
        self.test_fst = FST.load(os.path.join(self.path, fst_name))

    def parse_text(self, text):
        result = list(self.test_fst.apply_down(text))
        return result


if __name__ == '__main__':

    iterations = 100
    report = []

    _config = Config(combine_path=config.PROJECT_PATH)
    data_loader = DataLoader(config_data=_config)
    tokenizer = Tokenizer()

    parsers = {'Кабели силовые': ParserFST('power_cables.fst'), 'Кабели информационные': ParserFST('info_cables.fst')}

    splitters = '([%s])' % '|'.join([re.escape(el) for el in ["х", "*", "x", "#", "Х", "\\", "X", "×", "="]])
    splitters = re.compile(splitters)

    for category in ['cable']:
        data = data_loader.load_data(category)
        data_count = len(data)

        iter_times = []
        for iteration in range(iterations):

            _data = [
                (' '.join([t.src_str for t in tokenizer.tokenize(text.offer_text, splitters)]), text.category_name)
                for text in data]

            t1 = time.time()
            for t in _data:
                r = parsers[t[1]].parse_text(t[0])
                # print(t[1], t[0], r)
            t2 = time.time()

            iter_times.append(round(t2 - t1, 5))
        report.append([category, data_count, sum(iter_times) / iterations])
        del data

    report = sorted(report, key=lambda x: x[-1])
    print(tabulate(report, headers=['Category', '#data', 'time'], tablefmt='psql'))
    print('Average time per %s iterations.' % (iterations,))