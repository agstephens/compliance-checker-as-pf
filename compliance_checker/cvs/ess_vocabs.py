"""
ess_vocabs.py
=============

Holds the ESSVocabs class.

This is a base class for working with controlled vocabularies that can be worked with
using the pyessv library (https://github.com/ES-DOC/pyessv).

For example, the CMIP6 project manages its CVs in GitHub and can be accessed by pyessv
using a local file-system cache of the files.

"""

import os
from netCDF4 import Dataset

# Import library to interact with Controlled Vocabularies
import pyessv



def validate_daterange(frequency):
    if frequency == "yr" or frequency == "decadal":
        template = "yyyy"
    elif frequency == "mon" or frequency == "monClim":
        template = "yyyyMM"
    return template


class ESSVocabs(object):
    """
    Class for working with Vocabularies stored in ESSV format.
    Accessible via `pyessv` library.

    """
    authority = None
    scope = None

    
    def __init__(self, authority, scope):
        """
        Instantiates class by setting authority, scope and loading the CVs 
        from local cache.
        """
        self.authority = authority
        self.scope = scope
        self._cache_controlled_vocabularies()


    def _cache_controlled_vocabularies(self):
        """
        Loads controlled vocabularies once and caches them.
        """
        self._cvs = pyessv.load(self.authority, self.scope)
        self._authority_info = pyessv.load(self.authority)
        self._scope_info = pyessv.load(self.authority, self.scope)


    def _lookup(self, attr):
        "Maps attribute name to lookup value."
        return attr.replace("_", "-") 
        
        
    def check_global_attribute(self, ds, attr, property="label"):
        """
        Checks that global attribute `attr` is in allowed values (from CV).
       
        :param ds: NetCDF4 Dataset object
        :param attr: string - name of attribtue to check.
        :param property: string property of CV term to check (defaults to 'label')
        :return: Integer (0: not found; 1: found (not recognised); 2: found and recognised.
        """
        if not attr in ds.ncattrs():
            return 0
           
        nc_attr = ds.getncattr(attr) 

        allowed_values = [getattr(term, property, None) for term in self._cvs[self._lookup(attr)]]

        if nc_attr not in allowed_values:
            return 1
            
        return 2


    def check_file_name(self, filename, keys=None, delimiter="_", extension=".nc"):
        """
        Checks that components in the file name match CV-allowed values.
        
        E.g.:
        <variable_id>   tas
        <table_id>      Amon
        <source_id>     hadgem3-es
        <experiment_id> piCtrl
        <member_id>     r1i1p1f1
        <grid_label>    gn
        [<time_range>]  201601-210012
        .nc
        
        :param filename: string
        :keys  sequence of attribute keys to look-up values from in CVs.
        :delimiter  string used as delimiter in file name: string.
        :extension  the file extension: string.
        :return: True or raises Exception.
        """
        if not keys or type(keys) not in (type([]), type(())):
            raise Exception("File name checks require an input of attribute keys to check against. "
                            "None given.")
                            
        items = os.path.splitext(filename)[0].split(delimiter)
        
        # Now check
        template = delimiter.join(['{}' for item in items]) + extension
        print template
        
        print pyessv.load(self.authority, self.scope, 'frequency')
        print self._cvs['frequency']
        print pyessv.load(self.authority, self.scope, 'frequency')==self._cvs['frequency']
        collections = tuple([self._cvs[self._lookup(key)] for key in keys])
        print collections
        
        parser = pyessv.create_template_parser(template, collections)

        try:
            parser.parse(filename)
        except pyessv.TemplateParsingError:
            raise Exception("File name {} does not follow required specification.".format(filename))

        return True
