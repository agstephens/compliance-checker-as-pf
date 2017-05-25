# -*- coding: utf-8 -*-

import os
import argparse
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
        assert os.path.isfile(filepath), "File {} does not exist".format(filepath)
        self.data_set.append(os.path.join(filepath))

        return self

    def run_tests(self, skip_checks, checker_names):
        output = {}
        for data_file in self.data_set:
            # print "Testing {}".format(data_file)
            ds = self.check_suite.load_dataset(data_file)
            output[data_file] = self.check_suite.run(ds, skip_checks, checker_names)
        return output

    def json_output(self, output):
        results_dict = {}
        for filenames in output:
            score_groups = output[filenames]
            results = {}
            for i, (checker, rpair) in enumerate(score_groups.items()):
                groups, errors = rpair
                results[checker] = mfr.check_suite.dict_output('cf', groups, 'test', 1)
            results_dict[filenames] = results
        return json.dumps(results_dict, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate a set of ncdf files')
    parser.add_argument('--basedir')
    args = parser.parse_args()

    mfr = MultiFileRunner(CheckSuite(), args.basedir)
    for root, dirs, files in os.walk(args.basedir):
        for file in files:
            if file.endswith(".nc"):
                # print "Adding {} to the queue".format(file)
                mfr.add_file(os.path.join(root, file))
            else:
                print file
    output = mfr.run_tests([], 'cf')
    print mfr.json_output(output)
