# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import re
# reading package version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__),'pyvalidate', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'",re.S).match(v_file.read()).group(1)


readme = """
pyvalidate
==========


.. Python method's parameter validation library, as a pythonic decorator


Validates input parameters of a callable using this arguments::
  
   param: arg_types:            list of types, Required argument's types  & counts in order
   param: deny_match            list of string ,regex pattern, if any argument matches with the pattern, exception raises
   param: requires:             list of fields to check for mandatory
   param: deny:                 string ,regex pattern, if any parameter matches with the pattern, exception raises
   param: deny_except:          string ,regex pattern for excluding fields from deny
   param: types:                dict of key:name and value:type to check for types, if mismatch it will be raises exception
   param: values:               dict of key:name and value:regex pattern to check the values, & fire exception if mismatch
   param: ignore:               string ,regex pattern of parameters to filter
   param: defaults:             dict of key:name and value:default_value


Exceptions::
    
   raise: MandatoryException:           if any param in requires does not provided
   raise: ArgumentException:            if arguments are invalid , short or mismatch type.
   raise: DenialException:              if found param in deny list
   raise: ParameterTypeException:       if parameter types invalid
   raise: ParameterValueException:      if values are not in correct format


Example::

   from pyvalidate import validate, ValidationException
   
   @validate(arg_types=[int, str, str],
             deny_match=['xxx', 'tiktik'],
             requires=['phone'],
             deny='query',
             deny_except='query2',
             types={'phone':str, 'address':str, 'age':int},
             values={'phone':'^\d*$'},
             ignore='age',
             defaults={'address':'nothing'})
   def add_person(serial, firstname, lastname, phone=None, address=None, age=None, **kw):
       print 'adding person "%s:%s %s:%s" with serial: %s:%s phone: %s:%s address: %s:%s age:%s:%s' \
               % (firstname, type(firstname),
                  lastname, type(lastname),
                  serial, type(serial),
                  phone,
                  type(phone),
                  address,
                  type(address),
                  age,
                  type(age))
       
   def test(*args, **kwargs):
       try:
           add_person(*args, **kwargs)
       except ValidationException as ex:
           print ex.message
   
   def main():
       test(12, "Vahid", "Mardani", phone="09122451075", address="Tehran")
       test("12", "Vahid", "Mardani", phone='+9122451075', address="Tehran")
       test("12", "Vahid", "Mardani", phone='1')
       test("12", "Vahid", "Mardani", phone='tiktik')
       test("12", "xxx", "Mardani", phone='')
       test("12", "", "Mardani",)
       test("12", "", "Mardani", phone='1', query='123')
       test("12", "", "Mardani", phone='1', query2='123')
       test("12", "", "Mardani", phone='1', age='123')
       
   if __name__ == '__main__':
       main()

"""

setup(
    name="pyvalidate",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    url="http://packages.python.org/pyvalidate",
    description="Python method's parameter validation library, as a pythonic decorator",
    maintainer="Vahid Mardani",
    maintainer_email="vahid.mardani@gmail.com",
    packages=["pyvalidate"],
    platforms=["any"],
    long_description=readme,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Freeware",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
        ],
    )
