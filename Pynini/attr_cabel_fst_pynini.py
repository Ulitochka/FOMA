import os

from tqdm import tqdm
import time
from tabulate import tabulate

from grammar_fst.Pynini.create_fst import AttributeGrammarFST
from tools.data_loader import DataLoader

from dgisconfig import Config

import config


class CableParser:

    def __init__(self):

        self.path = os.path.join(os.path.dirname(__file__) + '/bin_files/')
        self.attr_grammar_fst = AttributeGrammarFST()
        self.rules = None

    def get_fst(self, fst_names):
        rules = {}
        for fname in fst_names:
            bin_models = {}
            fsts_path = os.path.join(self.path, fname)
            for fst_file in sorted(os.listdir(fsts_path)):
                if fst_file.endswith('fst'):
                    bin_models[fst_file.split('.')[0]] = self.attr_grammar_fst.load(os.path.join(fsts_path, fst_file))
            rules[fname] = bin_models
        return rules

    def parse_block(self, data):
        data_result = []
        for rubric in data:
            rubric_result = []
            for text in sorted(data[rubric]):
                result = self.attr_grammar_fst.singularize(text[0], self.rules[rubric])
                rubric_result.append((text[0], result))
            rubric_result = sorted(rubric_result)
            data_result.append((rubric, rubric_result))
        return sorted(data_result)

    def parse_text(self, rubric, text):
        return self.attr_grammar_fst.singularize(text, self.rules[rubric])


if __name__ == '__main__':

    iterations = 1
    report = []

    _config = Config(combine_path=config.PROJECT_PATH)
    data_loader = DataLoader(config_data=_config)

    cable_parser = CableParser()
    cable_parser.rules = cable_parser.get_fst(fst_names=['Кабели силовые', 'Кабели информационные'])

    for category in ['cable']:
        data = data_loader.load_data(category)
        data_count = len(data)

        iter_times = []
        for iteration in range(iterations):
            t1 = time.time()
            for t in data:
                _ = cable_parser.parse_text(t.category_name, t.offer_text)
            t2 = time.time()
            iter_times.append(round(t2 - t1, 2))
        report.append([category, data_count, sum(iter_times) / iterations])
        del data

    report = sorted(report, key=lambda x: x[-1])
    print(tabulate(report, headers=['Category', '#data', 'time'], tablefmt='psql'))
    print('Average time per %s iterations.' % (iterations,))
