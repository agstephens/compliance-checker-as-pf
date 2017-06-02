
# coding: utf-8

# # CMIP6 vocabularies with pyessv 

# 1. pyessv is a pragmatic, simple to use vocabulary management tool
# 2. pyessv archive has been [seeded](https://github.com/ES-DOC/pyessv-writer/blob/master/sh/write_wcrp_cmip6.py) with CV's pulled from [WCRP-CMIP CMIP6 CVs](https://github.com/WCRP-CMIP/CMIP6_CVs)
# 3. pyessv CV data model:  
#    3.1  Authority (e.g. WCRP)  
#    3.2  Scope (e.g. CMIP6)  
#    3.3  Collection (e.g. institution-id)  
#    3.4  Term (e.g. noaa-gfdl)  

# ## 0.  Pre-Requisites

# 1.  Download pyessv-archive repository to local file system:  
#     
#     git clone https://github.com/ES-DOC/pyessv-archive.git YOUR_WORK_DIRECTORY  
#     
# 
# 2.  Create ES-DOC pyessv folder:  
# 
#     mkdir ~/.esdoc/pyessv-archive
#     
# 3.  Create authority sym links:
# 
#     ln -s YOUR_WORK_DIRECTORY/pyessv-archive/wcrp ~/.esdoc/pyessv-archive

# ## 1.  Setup

# In[ ]:

import pyessv


# ## 2.  Loading

# In[ ]:

# Load the WCRP authority (once loaded it is cached).
wcrp = pyessv.load('wcrp')
assert isinstance(wcrp, pyessv.Authority)


# In[ ]:

# Load the WCRP-CMIP6 scope.
cmip6 = pyessv.load('wcrp', 'cmip6')
assert isinstance(cmip6, pyessv.Scope)


# In[ ]:

# Load the WCRP-CMIP6 institutional collection.
institutions = pyessv.load('wcrp', 'cmip6', 'institution-id')
assert isinstance(institutions, pyessv.Collection)


# In[ ]:

# Load the WCRP-CMIP6 IPSL institution.
gfdl = pyessv.load('wcrp', 'cmip6', 'institution-id', 'noaa-gfdl')
assert isinstance(gfdl, pyessv.Term)


# ## 3.  Iteration

# In[ ]:

# Iterate all scopes managed by an authority.
for scope in wcrp:
    assert isinstance(scope, pyessv.Scope)


# In[ ]:

# Iterate all collections within a scope.
for collection in cmip6:
    assert isinstance(collection, pyessv.Collection)


# In[ ]:

# Iterate all terms within a collection.
for term in institutions:
    assert isinstance(term, pyessv.Term)


# ## 4.  Key based access

# In[ ]:

# Set pointer to a scope within an authority.
assert wcrp['cmip6'] == cmip6


# In[ ]:

# Set pointer to a collection within a scope.
assert cmip6['institution-id'] == institutions


# In[ ]:

# Set pointer to a term within a collection.
assert institutions['noaa-gfdl'] == gfdl


# ## 5.  Properties

# ### Authority properties

# In[ ]:

# Canonical name (always lower cased).
print wcrp.name


# In[ ]:

# Label for UI purposes.
print wcrp.label


# In[ ]:

# Description.
print wcrp.description


# In[ ]:

# Homepage / URL.
print wcrp.url


# In[ ]:

# Namespace.
print wcrp.namespace


# ### Scope properties

# In[ ]:

# Canonical name (always lower cased).
print cmip6.name


# In[ ]:

# Label for UI purposes.
print cmip6.label


# In[ ]:

# Description.
print cmip6.description


# In[ ]:

# Homepage / URL.
print cmip6.url


# In[ ]:

# Namespace.
print cmip6.namespace


# ### Collection properties

# In[ ]:

# Canonical name (always lower cased).
print institutions.name


# In[ ]:

# Label for UI purposes.
print institutions.label


# In[ ]:

# Description.
print institutions.description


# In[ ]:

# Homepage / URL.
print institutions.url


# In[ ]:

# Namespace.
print institutions.namespace


# ### Term properties

# In[ ]:

# Canonical name (always lower cased).
print gfdl.name


# In[ ]:

# Label for UI purposes.
print gfdl.label


# In[ ]:

# Creation date
print gfdl.create_date


# In[ ]:

# Universally unique identifier (assigned at point of creation).
print gfdl.uid


# In[ ]:

# Collection position identifier.
print gfdl.idx


# In[ ]:

# Governance status.
print gfdl.status


# In[ ]:

# Namespace (authority:scope:collection:term).
print gfdl.namespace


# ## Discovery

# In[ ]:

# Scopes within an authority are sorted.
for scope in wcrp:
    print scope


# In[ ]:

# Collections within a scope are sorted.
for collection in cmip6:
    print collection


# In[ ]:

# Terms within a collection are sorted.
for term in institutions:
    print term


# ## Encoding

# In[ ]:

# Encode authority as a python dictionary.
assert isinstance(pyessv.encode(wcrp, 'dict'), dict)

# Encode scope as a python dictionary.
assert isinstance(pyessv.encode(cmip6, 'dict'), dict)

# Encode collection as a python dictionary.
assert isinstance(pyessv.encode(institutions, 'dict'), dict)

# Encode term as a python dictionary.
assert isinstance(pyessv.encode(gfdl, 'dict'), dict)


# In[ ]:

# Encode authority as a JSON text blob.
assert isinstance(pyessv.encode(wcrp, 'json'), basestring)
assert isinstance(pyessv.encode(wcrp), basestring)

# Encode scope as a JSON text blob.
assert isinstance(pyessv.encode(cmip6), basestring)
assert isinstance(pyessv.encode(cmip6, 'json'), basestring)

# Encode collection as a JSON text blob.
assert isinstance(pyessv.encode(institutions), basestring)
assert isinstance(pyessv.encode(institutions, 'json'), basestring)

# Encode term as a JSON text blob.
assert isinstance(pyessv.encode(gfdl), basestring)
assert isinstance(pyessv.encode(gfdl, 'json'), basestring)


# ## Parsing - name validation & substitution

# #### A canonical name is returned upon a successful parse

# In[ ]:

# Parse authority.
assert pyessv.parse('wcrp') == 'wcrp'

# Parse scope.
assert pyessv.parse('wcrp', 'cmip6') == 'cmip6'

# Parse collection.
assert pyessv.parse('wcrp', 'cmip6', 'institution-id') == 'institution-id'

# Parse term.
assert pyessv.parse('wcrp', 'cmip6', 'institution-id', 'ipsl') == 'ipsl'


# #### A parsing error is raised upon an unsuccessful parse

# In[ ]:

# Parse invalid authority.
try:
    pyessv.parse('xxx')
except pyessv.ParsingError:
    pass

# Parse invalid scope.
try:
    pyessv.parse('wcrp', 'xxx')
except pyessv.ParsingError:
    pass

# Parse invalid collection.
try:
    pyessv.parse('wcrp', 'cmip6', 'xxx')
except pyessv.ParsingError:
    pass

# Parse invalid term.
try:
    pyessv.parse('wcrp', 'cmip6', 'institution-id', 'xxx')
except pyessv.ParsingError:
    pass


# #### Set strict = false in order to parse mixed-case & synonyms

# In[ ]:

assert pyessv.parse('wCRp', strict=False) == 'wcrp'


# In[ ]:

assert pyessv.parse('wCRp', 'cMIp6', strict=False) == 'cmip6'


# In[ ]:

assert pyessv.parse('wCRp', 'cMIp6', 'inSTitutION-id', strict=False) == 'institution-id'


# In[ ]:

assert pyessv.parse('wCRp', 'cMIp6', 'inSTitutION-id', 'IPsl', strict=False) == 'ipsl'


# ## Regular Expressions

# In[ ]:

# Create a collection specifying a regular expression to be applied against terms.
re_collection = pyessv.create_collection(
    cmip6,
    "test-regex-collection",
    "Ensemble member",
    term_name_regex=r'^[a-z\-]*$'
)


# In[ ]:

# Create a valid term.
term = pyessv.create_term(re_collection, "abc-def", "valid-regex-term")
assert pyessv.is_valid(term) == True


# In[ ]:

# Create an invalid term - raises ValidationError.
try:
    pyessv.create_term(re_collection, "ABC-DEF", "invalid-regex-term")
except pyessv.ValidationError:
    pass


# ## Template parsing

# In[ ]:

# Template.
template = 'ciclad/cmip6/{}/{}/{}/{}/afilename.nc1'

# Template collections.
collections = (
    pyessv.load('wcrp', 'cmip6', 'institution-id'),
    pyessv.load('wcrp', 'cmip6', 'activity-id'),
    pyessv.load('wcrp', 'cmip6', 'source-id'),
    pyessv.load('wcrp', 'cmip6', 'experiment-id')
    )

# Parser.
parser = pyessv.create_template_parser(template, collections)


# In[ ]:

# Parse a valid.
parser.parse('ciclad/cmip6/ipsl/dcpp/hadgem3-gc31-ll/dcppc-atl-spg/afilename.nc1')


# In[ ]:

# Parsing: invalid - raises TemplateParsingError. 
try:
    parser.parse('ciclad/cmip6/WWW/XXX/YYY/ZZZ/afilename.nc1')
except pyessv.TemplateParsingError:
    pass


