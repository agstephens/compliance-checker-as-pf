import os

# Set which vocabs to use
os.environ["ESSV_VOCABS_ACTIVE"] = "eustace-team"

if 0:
 import pyessv
 cv = pyessv.load('eustace-team', 'eustace')
 print [(x.name, x.label) for x in cv['frequency']]

from compliance_checker.cvs.ess_vocabs import ESSVocabs
import netCDF4

authority = "eustace-team"
scope = "eustace"

ev = ESSVocabs(authority, scope)
ncfile = "compliance_checker/tests/data/test_cdl_global_atts.nc"

ds = netCDF4.Dataset(ncfile)

def test_global_attribute_missing():
    resp = ev.check_global_attribute(ds, 'source', property="label")
    assert(resp == 0)
    print "PASS: no attribute."


def test_global_attribute_unknown_value():
    resp = ev.check_global_attribute(ds, 'frequency', property="name")
    assert(resp == 1)
    print "PASS: attribute found but unknown value."


def test_global_attribute_valid_value():
    resp = ev.check_global_attribute(ds, 'institution_id', property="label")
    print resp
    assert(resp == 2)
    print "PASS: attribute found with valid value."


def test_check_file_name_fails():

    filename = "MOHC_day.nc"
    keys = ('institution_id', 'frequency')
    try:
        ev.check_file_name(filename, keys=keys, extension=".nc")
    except Exception, err:
        assert (str(err) == "File name MOHC_day.nc does not follow required specification.")


def test_check_file_name_success():

    filename = "mohc_day.nc"
    keys = ('institution_id', 'frequency')
    resp = ev.check_file_name(filename, keys=keys, extension=".nc")
    assert (resp == True)



def run_tests():
    tests = [test_global_attribute_missing,
             test_global_attribute_unknown_value,
             test_global_attribute_valid_value,
             test_check_file_name_fails,
             test_check_file_name_success
            ]

    for test in tests:
         print "Running test: {}".format(test.__name__)
         test()


if __name__ == "__main__":

    run_tests()    
