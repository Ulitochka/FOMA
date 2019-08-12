import unittest
from pprint import pprint

from grammar_fst.Foma.attr_cabel_fst_foma import ParserFST


class TestParserFST(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_power_cable_parser = ParserFST('power_cables.fst')
        cls.test_info_cable_parser = ParserFST('info_cables.fst')

    def test_parse_power(self):
        test_data = [
            ['Кабель ВВГ - Пнг ( А ) 3 х 2 . 5 мм 50 м',
             'O O O O O O O B-Количество жил O B-Сечение провода_кв.мм I-Сечение провода_кв.мм I-Сечение провода_'
             'кв.мм O '
             'B-Длина_м I-Длина_м'],
            ['Кабель КГ 1 х 16 мм на отрез',
             'O O B-Количество жил O B-Сечение провода_кв.мм I-Сечение провода_кв.мм O O'],
            ['Кабель ВВГп - НГ 3 х 2 . 5 мм 50 м ( ГОСТ )',
             'O O O O B-Количество жил O B-Сечение провода_кв.мм I-Сечение провода_кв.мм I-Сечение провода_кв.мм O '
             'B-Длина_м '
             'I-Длина_м O O O'],
            ['Кабель NYM 3 х 4 мм на отрез ( ГОСТ )',
             'O O B-Количество жил O B-Сечение провода_кв.мм I-Сечение провода_кв.мм O O O O O'],
            ['Кабель NYM 2 х 6 мм на отрез ( ГОСТ )',
             'O O B-Количество жил O B-Сечение провода_кв.мм I-Сечение провода_кв.мм O O O O O'],
            ['Провод ПВС 2 х 1 мм на отрез ( ГОСТ )',
             'O O B-Количество жил O B-Сечение провода_кв.мм I-Сечение провода_кв.мм O O O O O'],
            ['Провод ПВС 3 Х 1 . 5 мм 10 м ( ГОСТ )', '']
        ]

        true_result = [
            ('Кабель ВВГ - Пнг ( А ) 3 х 2 . 5 мм 50 м',
             'Кабель ВВГ - Пнг ( А ) Zili х CableSection CableSection CableSection мм Len м'),

            ('Кабель КГ 1 х 16 мм на отрез', 'Кабель КГ Zili х CableSection мм на отрез'),

            ('Кабель ВВГп - НГ 3 х 2 . 5 мм 50 м ( ГОСТ )',
             'Кабель ВВГп - НГ Zili х CableSection CableSection CableSection мм Len м ( ГОСТ )'),

            ('Кабель NYM 3 х 4 мм на отрез ( ГОСТ )', 'Кабель NYM Zili х CableSection мм на отрез ( ГОСТ )'),

            ('Кабель NYM 2 х 6 мм на отрез ( ГОСТ )', 'Кабель NYM Zili х CableSection мм на отрез ( ГОСТ )'),

            ('Провод ПВС 2 х 1 мм на отрез ( ГОСТ )', 'Провод ПВС Zili х CableSection мм на отрез ( ГОСТ )'),

            ('Провод ПВС 3 Х 1 . 5 мм 10 м ( ГОСТ )',
             'Провод ПВС Zili Х CableSection CableSection CableSection мм Len м ( ГОСТ )')

        ]

        fact_result = [(t[0], self.test_power_cable_parser.parse_text(t[0])[0]) for t in test_data]
        # pprint(fact_result)
        self.assertEqual(true_result, fact_result)

    def test_parse_info(self):
        test_data = [
            ['Кабель сетевой UTP cat 5e 4 х 2 х 0 . 51 мм 10 м',
             'O O O O O B-Количество жил O B-Количество соединительных проводов O B-Диаметр_мм I-Диаметр_мм '
             'I-Диаметр_мм O B-Длина_м I-Длина_м'],

            ['Удлинитель компьютерный UTP4 cat5e 3 м , цвет серый', ''],

            ['Кабель информационный экранированный FTP Cat 5e 4 х 2 х 0 , 52 V / PE tr Parlan уличный с тросом 100016',
             ''],

            ['КАБЕЛЬ ИНФОРМАЦИОННЫЙ PANDUIT TX5500 PUZ5504BU-CEG КАТ.5Е U/UTP НЕЭКРАН LSZH (IEC 60332-3) '
             'ВНУТРЕННИЙ 305М'],

            ['Кабель UTP 4PR 24AWG, CAT5e наружный (OUTDOOR) (бухта 305 м) СМАРТКИП, 1шт. в упаковке, арт. C-054-1', '']

        ]

        true_result = [
            (
                'Кабель сетевой UTP cat 5e 4 х 2 х 0 . 51 мм 10 м',
                'Кабель сетевой UTP cat 5e Zili х NumberConnectingWires х Diameter Diameter Diameter мм Len м'
            ),

            (
                'Удлинитель компьютерный UTP4 cat5e 3 м , цвет серый',
                'Удлинитель компьютерный UTP4 cat5e Len м , цвет серый'
            ),

            (
                'Кабель информационный экранированный FTP Cat 5e 4 х 2 х 0 , 52 V / PE tr Parlan уличный с тросом 100016',
                'Кабель информационный экранированный FTP Cat 5e Zili х NumberConnectingWires х Diameter Diameter Diameter V / PE tr Parlan уличный с тросом 100016'
            ),

            (
                'КАБЕЛЬ ИНФОРМАЦИОННЫЙ PANDUIT TX5500 PUZ5504BU-CEG КАТ.5Е U/UTP НЕЭКРАН LSZH (IEC 60332-3) ВНУТРЕННИЙ 305М',
                'КАБЕЛЬ ИНФОРМАЦИОННЫЙ PANDUIT TX5500 PUZ5504BU-CEG КАТ.5Е U/UTP НЕЭКРАН LSZH (IEC 60332-3) ВНУТРЕННИЙ LenМ'
            ),

            (
                'Кабель UTP 4PR 24AWG, CAT5e наружный (OUTDOOR) (бухта 305 м) СМАРТКИП, 1шт. в упаковке, арт. C-054-1',
                'Кабель UTP 4PR 24AWG, CAT5e наружный (OUTDOOR) (бухта Len м) СМАРТКИП, 1шт. в упаковке, арт. C-054-1'
            )
        ]

        fact_result = [(t[0], self.test_info_cable_parser.parse_text(t[0])[0]) for t in test_data]
        # pprint(fact_result)
        self.assertEqual(true_result, fact_result)

        if __name__ == '__main__':
            unittest.main()
