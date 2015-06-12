from unittest import TestCase
import pandas as pd
import numpy as np
import userinput, unittest
from os.path import expanduser


class TestUserInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        home = expanduser('~')
        user_input_fn = home + r'/modules/cpr/goterm/test/UserInput_test_3.txt'
        cls._ui = userinput.UserInput(user_input_fn, col_sample_an='sample_an', col_background_an='background_an',
                                      col_background_int='background_int')

    def test_get_sample_an_frset_1(self):
        sample_an_frset = frozenset(['AAA111', 'AAA112', 'AAA113', 'CAA111', 'CAA112', 'CAA113'])
        self.assertEqual(sample_an_frset, self._ui.get_sample_an_frset())

    def test_get_sample_an_frset_all_1(self):
        sample_an_frset = frozenset(['AAA111', 'AAA112', 'AAA113', 'CAA111', 'CAA112', 'CAA113', 'DAA111'])
        self.assertEqual(sample_an_frset, self._ui.get_sample_an_frset_all())

    def test_get_background_an_set(self):
        background_an_set = set(['AAA111','AAA112','AAA113','CAA111','CAA112','CAA113', 'BBB111', 'BBB112', 'BBB113', 'EEE111', 'EEE123'])
        self.assertEqual(background_an_set, self._ui.get_background_an_set())

    def test_get_background_an_all_set(self):
        background_an_all_set = set(['AAA111','AAA112','AAA113','CAA111','CAA112','CAA113', 'BBB111', 'BBB112', 'BBB113', 'DAA111', 'EEE111', 'EEE123', 'FFF111'])
        self.assertEqual(background_an_all_set, self._ui.get_background_an_all_set())

    def test_df_int_noNaNs(self):
        '''
        every AN should have corresponding intensity
        '''
        sum_background_int_NaNs = sum(self._ui.df_int.loc[pd.isnull(self._ui.df_int[self._ui.col_background_int]), self._ui.col_background_int])
        self.assertEqual(sum_background_int_NaNs, 0)

    def test_df_all_noNaNs_inAN(self):
        '''
        no NaNs in background_AN column
        '''
        sum_background_an_NaNs = sum(self._ui.df_all.loc[pd.isnull(self._ui.df_all[self._ui.col_background_an]), self._ui.col_background_an])
        self.assertEqual(sum_background_an_NaNs, 0)





        # def test_get_sample_ser_all_1(self):
        #     sample_ser_all = pd.Series(data=['AAA111','AAA112','AAA113','CAA111','CAA112','CAA113','DAA111'], name=self._ui.col_sample_an)
        #     sample_ser_all.index = sample_ser_all.tolist()
        #     assertEqual(sample_ser_all, self._ui.get_sample_ser_all())



        # def test_get_sample_ser_int_1(self):
        #     sample_ser_int = pd.Series(data=['AAA111','AAA112','AAA113','CAA111','CAA112','CAA113'], name=self._ui.col_sample_an)
        #     sample_ser_int.index = sample_ser_int.tolist()
        #     assert_series_equal(sample_ser_int, self._ui.get_sample_ser_int())
        #
        # def test_get_background_df_all_1(self):
        #     d = {self._ui.col_background_an: ['AAA111','AAA112','AAA113','CAA111','CAA112','CAA113', 'BBB111', 'BBB112', 'BBB113', 'DAA111', 'EEE111', 'EEE123', 'FFF111'],
        #          self._ui.col_background_int: [11.1,    11.2,    11.3,    13.1,    13.1,    13.1,     12.1,     12.2,    12.3,      np.nan,   14.1,     14.1,     np.nan]}
        #     background_df_all = pd.DataFrame(d)
        #     background_df_all.index = background_df_all[self._ui.col_background_an].tolist()
        #     assert_frame_equal(background_df_all.sort(self._ui.col_background_an), self._ui.get_background_df_all().sort(self._ui.col_background_an), check_names=True)
        #     # print(background_df_all)
        #     # print('####')
        #     # print(self._ui.get_background_df_all().sort(self._ui.col_background_an))
        #
        # def test_get_background_df_int_1(self):
        #     d = {self._ui.col_background_an: ['AAA111','AAA112','AAA113','CAA111','CAA112','CAA113', 'BBB111', 'BBB112', 'BBB113', 'EEE111', 'EEE123'],
        #          self._ui.col_background_int: [11.1,    11.2,    11.3,    13.1,    13.1,    13.1,     12.1,     12.2,    12.3,      14.1,     14.1]}
        #     background_df_int = pd.DataFrame(d)
        #     background_df_int.index = background_df_int[self._ui.col_background_an].tolist()
        #     assert_frame_equal(background_df_int.sort(self._ui.col_background_an), self._ui.get_background_df_int().sort(self._ui.col_background_an), check_names=True)
        #
        # def test_get_background_df_all_minsample_1(self):
        #     d = {self._ui.col_background_an: ['BBB111', 'BBB112', 'BBB113', 'EEE111', 'EEE123', 'FFF111'],
        #          self._ui.col_background_int: [12.1,     12.2,    12.3,      14.1,     14.1,     np.nan]}
        #     background_df_all_minsample = pd.DataFrame(d)
        #     background_df_all_minsample.index = background_df_all_minsample[self._ui.col_background_an].tolist()
        #     assert_frame_equal(background_df_all_minsample.sort(self._ui.col_background_an), self._ui.get_background_df_all_minsample().sort(self._ui.col_background_an), check_names=True)
        #
        # def test_get_background_df_int_minsample_1(self):
        #     d = {self._ui.col_background_an: ['BBB111', 'BBB112', 'BBB113', 'EEE111', 'EEE123'],
        #          self._ui.col_background_int: [12.1,     12.2,    12.3,      14.1,     14.1]}
        #     background_df_int_minsample = pd.DataFrame(d)
        #     background_df_int_minsample.index = background_df_int_minsample[self._ui.col_background_an].tolist()
        #     assert_frame_equal(background_df_int_minsample.sort(self._ui.col_background_an), self._ui.get_background_df_int_minsample().sort(self._ui.col_background_an), check_names=True)


suite = unittest.TestLoader().loadTestsFromTestCase(TestUserInput)
unittest.TextTestRunner(verbosity=2).run(suite)
