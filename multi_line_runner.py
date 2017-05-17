# -*- coding: utf-8 -*-

import os
import json
import inspect
from compliance_checker.runner import CheckSuite


class MultiFileRunner(object):

    def __init__(self, check_suite, basepath):
        self.check_suite = check_suite
        self.check_suite.load_all_available_checkers()
        self.data_set = []
        self.basepath = basepath

    def get_checks(self, checker_name):
        assert len(self.check_suite.checkers) > 0, "No checkers could be found"
        assert checker_name in self.check_suite.checkers, "Checker {} does not exist".format(checker_name)
        
        meths = inspect.getmembers(self.check_suite.checkers[checker_name](), inspect.ismethod)
        # return all check methods not among the skipped checks
        return [x[0] for x in meths if x[0].startswith("check_")]

    def add_file(self, filepath):
        assert os.path.isfile(os.path.join(self.basepath, filepath)), "File {} doesn't exist at {}".format(filepath, self.basepath)
        self.data_set.append(os.path.join(self.basepath, filepath))

        return self

    def run_tests(self, skip_checks, checker_names):
        output = []
        for data_file in self.data_set:
            ds = self.check_suite.load_dataset(data_file)
            output.append(self.check_suite.run(ds, skip_checks, checker_names))
        return output

    def json_output(self, output):
        results_array = []
        for score_groups in output:
            results = {}
            for i, (checker, rpair) in enumerate(score_groups.items()):
                groups, errors = rpair
                results[checker] = mfr.check_suite.dict_output('cf', groups, 'test', 1)
            results_array.append(results)
        return json.dumps(results_array, indent=2, ensure_ascii=False)

basepath = 'data/'
#filepath = 'va_Amon_HadGEM2-ES_rcp45_r1i1p1f1_202101-202101.nc'
filepath = 'ta_Amon_HadGEM2-A_amip_r1i1p1f1_202109-202109.nc'
filepath = 'tasmin_day_HadGEM2-ES_rcp45_r1i1p1f1_20210101-20210130.nc'

if __name__ == "__main__":
    mfr = MultiFileRunner(CheckSuite(), 'data')
    # print mfr.get_checks('cf')
    mfr.add_file(filepath)
    output = mfr.run_tests([], 'cf')
    print mfr.json_output(output)
