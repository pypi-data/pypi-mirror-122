#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Tue Oct  5 14:06:37 2021 by generateDS.py version 2.40.3.
# Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)]
#
# Command line options:
#   ('-o', 'models.py')
#   ('-s', 'models_stub.py')
#
# Command line arguments:
#   ya_fattura_elettronica_generator\package_data\Schema_del_file_xml_FatturaPA_versione_1.2.xsd
#
# Command line:
#   .\venv\Scripts\generateDS.py -o "models.py" -s "models_stub.py" ya_fattura_elettronica_generator\package_data\Schema_del_file_xml_FatturaPA_versione_1.2.xsd
#
# Current working directory (os.getcwd()):
#   pythonProject
#

import sys
from typing import List

try:
    ModulenotfoundExp_ = ModuleNotFoundError
except NameError:
    ModulenotfoundExp_ = ImportError
from six.moves import zip_longest
import os
import re as re_
import base64
import datetime as datetime_
import decimal as decimal_
from lxml import etree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the _exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ModulenotfoundExp_ :
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
except ModulenotfoundExp_ :
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ModulenotfoundExp_ :

    class GdsCollector_(object):

        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print("Warning: {}".format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write("Warning: {}\n".format(msg))


#
# The super-class for enum types
#

try:
    from enum import Enum
except ModulenotfoundExp_ :
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ModulenotfoundExp_ as exp:
    try:
        from generatedssupersuper import GeneratedsSuperSuper
    except ModulenotfoundExp_ as exp:
        class GeneratedsSuperSuper(object):
            pass
    
    class GeneratedsSuper(GeneratedsSuperSuper):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')
        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name
            def utcoffset(self, dt):
                return self.__offset
            def tzname(self, dt):
                return self.__name
            def dst(self, dt):
                return None
        def __str__(self):
            settings = {
                'str_pretty_print': True,
                'str_indent_level': 0,
                'str_namespaceprefix': '',
                'str_name': None,
                'str_namespacedefs': '',
            }
            for n in settings:
                if hasattr(self, n):
                    setattr(settings[n], self[n])
            from io import StringIO
            output = StringIO()
            self.export(
                output,
                settings['str_indent_level'],
                pretty_print=settings['str_pretty_print'],
                namespaceprefix_=settings['str_namespaceprefix'],
                name_=settings['str_name'],
                namespacedef_=settings['str_namespacedefs']
            )
            strval = output.getvalue()
            output.close()
            return strval
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data
        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data).decode('ascii')
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % int(input_data)
        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival
        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value
        def gds_format_integer_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_integer_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer values')
            return values
        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % float(input_data)).rstrip('0')
        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_
        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value
        def gds_format_float_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_float_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values
        def gds_format_decimal(self, input_data, input_name=''):
            return_value = '%s' % input_data
            if '.' in return_value:
                return_value = return_value.rstrip('0')
                if return_value.endswith('.'):
                    return_value = return_value.rstrip('.')
            return return_value
        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value
        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value
        def gds_format_decimal_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return ' '.join([self.gds_format_decimal(item) for item in input_data])
        def gds_validate_decimal_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values
        def gds_format_double(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_
        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value
        def gds_format_double_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_double_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, 'Requires sequence of double or float values')
            return values
        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()
        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval
        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (True, 1, False, 0, ):
                raise_parse_error(
                    node,
                    'Requires boolean value '
                    '(one of True, 1, False, 0)')
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_boolean_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                value = self.gds_parse_boolean(value, node, input_name)
                if value not in (True, 1, False, 0, ):
                    raise_parse_error(
                        node,
                        'Requires sequence of boolean values '
                        '(one of True, 1, False, 0)')
            return values
        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0], "{}".format(micro_seconds).rjust(6, "0"), )
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt
        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(
                                hours, minutes)
            except AttributeError:
                pass
            return _svalue
        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()
        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            if not isinstance(target, str):
                target = str(target)

            found1 = True
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1
        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()
        def gds_check_cardinality_(
                self, value, input_name,
                min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None :
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()))
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        min_occurs, length))
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        max_occurs, length))
        def gds_validate_builtin_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_validate_defined_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1
        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ""
            content = etree_.tostring(node, encoding="unicode")
            return content
        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))
        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring
        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result
        def __eq__(self, other):
            def excl_select_objs_(obj):
                return (obj[0] != 'parent_object_' and
                        obj[0] != 'gds_collector_')
            if type(self) != type(other):
                return False
            return all(x == y for x, y in zip_longest(
                filter(excl_select_objs_, self.__dict__.items()),
                filter(excl_select_objs_, other.__dict__.items())))
        def __ne__(self, other):
            return not self.__eq__(other)
        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass
        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass
        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None
        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass
        def gds_get_node_lineno_(self):
            if (hasattr(self, "gds_elementtree_node_") and
                    self.gds_elementtree_node_ is not None):
                return ' near line {}'.format(
                    self.gds_elementtree_node_.sourceline)
            else:
                return ""
    
    
    def getSubclassFromModule_(module, class_):
        '''Get the subclass of a class from a specific module.'''
        name = class_.__name__ + 'Sub'
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = ''
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        if prefix == 'xml':
            namespace = 'http://www.w3.org/XML/1998/namespace'
        else:
            namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace,
               pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name,
                pretty_print=pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (
                self.name,
                base64.b64encode(self.value),
                self.name))
    def to_etree(self, element, mapping_=None, reverse_mapping_=None, nsmap_=None):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(
                element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:    # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)
    def to_etree_simple(self, mapping_=None, reverse_mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (self.content_type == MixedContainer.TypeInteger or
                self.content_type == MixedContainer.TypeBoolean):
            text = '%d' % self.value
        elif (self.content_type == MixedContainer.TypeFloat or
                self.content_type == MixedContainer.TypeDecimal):
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n' % (
                    self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0,
            optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container
    def set_child_attrs(self, child_attrs): self.child_attrs = child_attrs
    def get_child_attrs(self): return self.child_attrs
    def set_choice(self, choice): self.choice = choice
    def get_choice(self): return self.choice
    def set_optional(self, optional): self.optional = optional
    def get_optional(self): return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


class Art73Type(str, Enum):
    SI='SI' # SI = Documento emesso secondo modalità e termini stabiliti con DM ai sensi dell'art. 73 DPR 633/72


class BolloVirtualeType(str, Enum):
    SI='SI'


class CausalePagamentoType(str, Enum):
    A='A'
    B='B'
    C='C'
    D='D'
    E='E'
    G='G'
    H='H'
    I='I'
    L='L'
    M='M'
    N='N'
    O='O'
    P='P'
    Q='Q'
    R='R'
    S='S'
    T='T'
    U='U'
    V='V'
    W='W'
    X='X'
    Y='Y'
    Z='Z'
    L_1='L1'
    M_1='M1'
    O_1='O1'
    V_1='V1'


class CondizioniPagamentoType(str, Enum):
    TP_01='TP01' # pagamento a rate
    TP_02='TP02' # pagamento completo
    TP_03='TP03' # anticipo


class EsigibilitaIVAType(str, Enum):
    D='D' # esigibilità differita
    I='I' # esigibilità immediata
    S='S' # scissione dei pagamenti


class FormatoTrasmissioneType(str, Enum):
    FPA_12='FPA12' # Fattura verso PA
    FPR_12='FPR12' # Fattura verso privati


class ModalitaPagamentoType(str, Enum):
    MP_01='MP01' # contanti
    MP_02='MP02' # assegno
    MP_03='MP03' # assegno circolare
    MP_04='MP04' # contanti presso Tesoreria
    MP_05='MP05' # bonifico
    MP_06='MP06' # vaglia cambiario
    MP_07='MP07' # bollettino bancario
    MP_08='MP08' # carta di pagamento
    MP_09='MP09' # RID
    MP_10='MP10' # RID utenze
    MP_11='MP11' # RID veloce
    MP_12='MP12' # RIBA
    MP_13='MP13' # MAV
    MP_14='MP14' # quietanza erario
    MP_15='MP15' # giroconto su conti di contabilità speciale
    MP_16='MP16' # domiciliazione bancaria
    MP_17='MP17' # domiciliazione postale
    MP_18='MP18' # bollettino di c/c postale
    MP_19='MP19' # SEPA Direct Debit
    MP_20='MP20' # SEPA Direct Debit CORE
    MP_21='MP21' # SEPA Direct Debit B2B
    MP_22='MP22' # Trattenuta su somme già riscosse


class NaturaType(str, Enum):
    N_1='N1' # Escluse ex. art. 15
    N_2='N2' # Non soggette
    N_2_2 = 'N2'  # Non soggette (altri casi)
    N_3='N3' # Non Imponibili
    N_4='N4' # Esenti
    N_5='N5' # Regime del margine
    N_6='N6' # Inversione contabile (reverse charge)
    N_7='N7' # IVA assolta in altro stato UE (vendite a distanza ex art. 40 commi 3 e 4 e art. 41 comma 1 lett. b, DL 331/93; prestazione di servizi di telecomunicazioni, tele-radiodiffusione ed elettronici ex art. 7-sexies lett. f, g, DPR 633/72 e art. 74-sexies, DPR 633/72)

    def get_description(self) -> str:
        cls = type(self)
        if self == cls.N_1:
            return "Escluse ex. art. 15"
        elif self == cls.N_2:
            return "Non soggette"
        elif self == cls.N_2_2:
            return "Non soggette (altri casi)"
        elif self == cls.N_3:
            return "Non Imponibili"
        elif self == cls.N_4:
            return "Esenti"
        elif self == cls.N_5:
            return "Regime del margine"
        elif self == cls.N_6:
            return "Inversione contabile (reverse charge)"
        elif self == cls.N_7:
            return "IVA assolta in altro stato UE (vendite a distanza ex art. 40 commi 3 e 4 e art. 41 comma 1 lett. b, DL 331/93; prestazione di servizi di telecomunicazioni, tele-radiodiffusione ed elettronici ex art. 7-sexies lett. f, g, DPR 633/72 e art. 74-sexies, DPR 633/72)"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class RegimeFiscaleType(str, Enum):
    RF_01='RF01' # Regime ordinario
    RF_02='RF02' # Regime dei contribuenti minimi (art. 1,c.96-117, L. 244/2007)
    RF_03='RF03' # Regime delle nuove iniziative produttive (art. 13, L. 388/2000)
    RF_04='RF04' # Agricoltura e attività connesse e pesca (artt. 34 e 34-bis, D.P.R. 633/1972)
    RF_05='RF05' # Vendita sali e tabacchi (art. 74, c.1, D.P.R. 633/1972)
    RF_06='RF06' # Commercio dei fiammiferi (art. 74, c.1, D.P.R. 633/1972)
    RF_07='RF07' # Editoria (art. 74, c.1, D.P.R. 633/1972)
    RF_08='RF08' # Gestione di servizi di telefonia pubblica (art. 74, c.1, D.P.R. 633/1972)
    RF_09='RF09' # Rivendita di documenti di trasporto pubblico e di sosta (art. 74, c.1, D.P.R. 633/1972)
    RF_10='RF10' # Intrattenimenti, giochi e altre attività di cui alla tariffa allegata al D.P.R. 640/72 (art. 74, c.6, D.P.R. 633/1972)
    RF_11='RF11' # Agenzie di viaggi e turismo (art. 74-ter, D.P.R. 633/1972)
    RF_12='RF12' # Agriturismo (art. 5, c.2, L. 413/1991)
    RF_13='RF13' # Vendite a domicilio (art. 25-bis, c.6, D.P.R. 600/1973)
    RF_14='RF14' # Rivendita di beni usati, di oggetti d’arte, d’antiquariato o da collezione (art. 36, D.L. 41/1995)
    RF_15='RF15' # Agenzie di vendite all’asta di oggetti d’arte, antiquariato o da collezione (art. 40-bis, D.L. 41/1995)
    RF_16='RF16' # IVA per cassa P.A. (art. 6, c.5, D.P.R. 633/1972)
    RF_17='RF17' # IVA per cassa (art. 32-bis, D.L. 83/2012)
    RF_19='RF19' # Regime forfettario
    RF_18='RF18' # Altro
    
    def get_description(self) -> str:
        cls = type(self)
        if self == cls.RF_01:
            return "Regime ordinario"
        elif self == cls.RF_02:
            return "Regime dei contribuenti minimi (art. 1,c.96-117, L. 244/2007)"
        elif self == cls.RF_03:
            return "Regime delle nuove iniziative produttive (art. 13, L. 388/2000)"
        elif self == cls.RF_04:
            return "Agricoltura e attività connesse e pesca (artt. 34 e 34-bis, D.P.R. 633/1972)"
        elif self == cls.RF_05:
            return "Vendita sali e tabacchi (art. 74, c.1, D.P.R. 633/1972)"
        elif self == cls.RF_06:
            return "Commercio dei fiammiferi (art. 74, c.1, D.P.R. 633/1972)"
        elif self == cls.RF_07:
            return "Editoria (art. 74, c.1, D.P.R. 633/1972)"
        elif self == cls.RF_08:
            return "Gestione di servizi di telefonia pubblica (art. 74, c.1, D.P.R. 633/1972)"
        elif self == cls.RF_09:
            return "Rivendita di documenti di trasporto pubblico e di sosta (art. 74, c.1, D.P.R. 633/1972)"
        elif self == cls.RF_10:
            return "Intrattenimenti, giochi e altre attività di cui alla tariffa allegata al D.P.R. 640/72 (art. 74, c.6, D.P.R. 633/1972)"
        elif self == cls.RF_11:
            return "Agenzie di viaggi e turismo (art. 74-ter, D.P.R. 633/1972)"
        elif self == cls.RF_12:
            return "Agriturismo (art. 5, c.2, L. 413/1991)"
        elif self == cls.RF_13:
            return "Vendite a domicilio (art. 25-bis, c.6, D.P.R. 600/1973)"
        elif self == cls.RF_14:
            return "Rivendita di beni usati, di oggetti d’arte, d’antiquariato o da collezione (art. 36, D.L. 41/1995)"
        elif self == cls.RF_15:
            return "Agenzie di vendite all’asta di oggetti d’arte, antiquariato o da collezione (art. 40-bis, D.L. 41/1995)"
        elif self == cls.RF_16:
            return "IVA per cassa P.A. (art. 6, c.5, D.P.R. 633/1972)"
        elif self == cls.RF_17:
            return "IVA per cassa (art. 32-bis, D.L. 83/2012)"
        elif self == cls.RF_18:
            return "Regime forfettario"
        elif self == cls.RF_19:
            return "Altro"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class RitenutaType(str, Enum):
    SI='SI' # SI = Cessione / Prestazione soggetta a ritenuta
    
    def get_description(self) -> str:
        cls = type(self)
        if self == cls.SI:
            return "Si"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class SocioUnicoType(str, Enum):
    SU='SU' # socio unico
    SM='SM' # più soci
    
    def get_description(self) -> str:
        cls = type(self)
        if self == cls.SU:
            return "Socio unico"
        elif self == cls.SM:
            return "più soci"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class SoggettoEmittenteType(str, Enum):
    CC='CC' # Cessionario / Committente
    TZ='TZ' # Terzo
    
    def get_description(self) -> str:
        cls = type(self)
        if self == cls.CC:
            return "Cessionario / Committente"
        elif self == cls.TZ:
            return "Terzo"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class StatoLiquidazioneType(str, Enum):
    LS='LS' # in liquidazione
    LN='LN' # non in liquidazione
    
    def get_description(self) -> str:
        cls = type(self)
        if self == cls.LS:
            return "in liquidazione"
        elif self == cls.LN:
            return "non in liquidazione"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class TipoCassaType(str, Enum):
    TC_01='TC01' # Cassa nazionale previdenza e assistenza avvocati e procuratori legali
    TC_02='TC02' # Cassa previdenza dottori commercialisti
    TC_03='TC03' # Cassa previdenza e assistenza geometri
    TC_04='TC04' # Cassa nazionale previdenza e assistenza ingegneri e architetti liberi professionisti
    TC_05='TC05' # Cassa nazionale del notariato
    TC_06='TC06' # Cassa nazionale previdenza e assistenza ragionieri e periti commerciali
    TC_07='TC07' # Ente nazionale assistenza agenti e rappresentanti di commercio (ENASARCO)
    TC_08='TC08' # Ente nazionale previdenza e assistenza consulenti del lavoro (ENPACL)
    TC_09='TC09' # Ente nazionale previdenza e assistenza medici (ENPAM)
    TC_10='TC10' # Ente nazionale previdenza e assistenza farmacisti (ENPAF)
    TC_11='TC11' # Ente nazionale previdenza e assistenza veterinari (ENPAV)
    TC_12='TC12' # Ente nazionale previdenza e assistenza impiegati dell'agricoltura (ENPAIA)
    TC_13='TC13' # Fondo previdenza impiegati imprese di spedizione e agenzie marittime
    TC_14='TC14' # Istituto nazionale previdenza giornalisti italiani (INPGI)
    TC_15='TC15' # Opera nazionale assistenza orfani sanitari italiani (ONAOSI)
    TC_16='TC16' # Cassa autonoma assistenza integrativa giornalisti italiani (CASAGIT)
    TC_17='TC17' # Ente previdenza periti industriali e periti industriali laureati (EPPI)
    TC_18='TC18' # Ente previdenza e assistenza pluricategoriale (EPAP)
    TC_19='TC19' # Ente nazionale previdenza e assistenza biologi (ENPAB)
    TC_20='TC20' # Ente nazionale previdenza e assistenza professione infermieristica (ENPAPI)
    TC_21='TC21' # Ente nazionale previdenza e assistenza psicologi (ENPAP)
    TC_22='TC22' # INPS


class TipoCessionePrestazioneType(str, Enum):
    SC='SC' # Sconto
    PR='PR' # Premio
    AB='AB' # Abbuono
    AC='AC' # Spesa accessoria

    def get_description(self) -> str:
        cls = type(self)
        if self == cls.SC:
            return "Sconto"
        elif self == cls.PR:
            return "Premio"
        elif self == cls.AB:
            return "Abbuono"
        elif self == cls.AC:
            return "Spesa accessoria"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class TipoDocumentoType(str, Enum):
    TD_01='TD01' # Fattura
    TD_02='TD02' # Acconto / anticipo su fattura
    TD_03='TD03' # Acconto / anticipo su parcella
    TD_04='TD04' # Nota di credito
    TD_05='TD05' # Nota di debito
    TD_06='TD06' # Parcella

    def get_description(self) -> str:
        cls = type(self)
        if self == cls.TD_01:
            return "Fattura"
        elif self == cls.TD_02:
            return "Acconto / anticipo su fattura"
        elif self == cls.TD_03:
            return "Acconto / anticipo su parcella"
        elif self == cls.TD_04:
            return "Nota di credito"
        elif self == cls.TD_05:
            return "Nota di debito"
        elif self == cls.TD_06:
            return "Parcella"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")



class TipoRitenutaType(str, Enum):
    RT_01='RT01' # Ritenuta di acconto persone fisiche
    RT_02='RT02' # Ritenuta di acconto persone giuridiche

    def get_description(self) -> str:
        cls = type(self)
        if self == cls.RT_01:
            return "Ritenuta di acconto persone fisiche"
        elif self == cls.RT_02:
            return "Acconto / anticipo su fattura"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class TipoScontoMaggiorazioneType(str, Enum):
    SC='SC' # SC = Sconto
    MG='MG' # MG = Maggiorazione

    def get_description(self) -> str:
        cls = type(self)
        if self == cls.SC:
            return "Sconto"
        elif self == cls.MG:
            return "Maggiorazione"
        else:
            raise ValueError(f"invalid enum of type {cls.__name__}!")


class FatturaElettronicaType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, versione=None, FatturaElettronicaHeader=None, FatturaElettronicaBody=None, Signature=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.versione = _cast(None, versione)
        self.versione_nsprefix_ = None
        self.FatturaElettronicaHeader = FatturaElettronicaHeader
        self.FatturaElettronicaHeader_nsprefix_ = None
        if FatturaElettronicaBody is None:
            self.FatturaElettronicaBody = []
        else:
            self.FatturaElettronicaBody = FatturaElettronicaBody
        self.FatturaElettronicaBody_nsprefix_ = None
        self.Signature = Signature
        self.Signature_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FatturaElettronicaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FatturaElettronicaType.subclass:
            return FatturaElettronicaType.subclass(*args_, **kwargs_)
        else:
            return FatturaElettronicaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FatturaElettronicaHeader(self) -> "FatturaElettronicaHeaderType":
        return self.FatturaElettronicaHeader
    def set_FatturaElettronicaHeader(self, FatturaElettronicaHeader):
        self.FatturaElettronicaHeader = FatturaElettronicaHeader
    def get_FatturaElettronicaBody(self) -> "List[FatturaElettronicaBodyType]":
        return self.FatturaElettronicaBody
    def set_FatturaElettronicaBody(self, FatturaElettronicaBody):
        self.FatturaElettronicaBody = FatturaElettronicaBody
    def add_FatturaElettronicaBody(self, value):
        self.FatturaElettronicaBody.append(value)
    def insert_FatturaElettronicaBody_at(self, index, value):
        self.FatturaElettronicaBody.insert(index, value)
    def replace_FatturaElettronicaBody_at(self, index, value):
        self.FatturaElettronicaBody[index] = value
    def get_Signature(self) -> "SignatureType":
        return self.Signature
    def set_Signature(self, Signature):
        self.Signature = Signature
    def get_versione(self):
        return self.versione
    def set_versione(self, versione):
        self.versione = versione
    def validate_FormatoTrasmissioneType(self, value):
        # Validate type FormatoTrasmissioneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FPA12', 'FPR12']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on FormatoTrasmissioneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on FormatoTrasmissioneType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
    def _hasContent(self):
        if (
            self.FatturaElettronicaHeader is not None or
            self.FatturaElettronicaBody or
            self.Signature is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema"  xmlns:ds="http://www.w3.org/2000/09/xmldsig#" ', name_='FatturaElettronicaType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FatturaElettronicaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FatturaElettronicaType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FatturaElettronicaType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FatturaElettronicaType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FatturaElettronicaType'):
        if self.versione is not None and 'versione' not in already_processed:
            already_processed.add('versione')
            outfile.write(' versione=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.versione), input_name='versione')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema"  xmlns:ds="http://www.w3.org/2000/09/xmldsig#" ', name_='FatturaElettronicaType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FatturaElettronicaHeader is not None:
            namespaceprefix_ = self.FatturaElettronicaHeader_nsprefix_ + ':' if (UseCapturedNS_ and self.FatturaElettronicaHeader_nsprefix_) else ''
            self.FatturaElettronicaHeader.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FatturaElettronicaHeader', pretty_print=pretty_print)
        for FatturaElettronicaBody_ in self.FatturaElettronicaBody:
            namespaceprefix_ = self.FatturaElettronicaBody_nsprefix_ + ':' if (UseCapturedNS_ and self.FatturaElettronicaBody_nsprefix_) else ''
            FatturaElettronicaBody_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FatturaElettronicaBody', pretty_print=pretty_print)
        if self.Signature is not None:
            namespaceprefix_ = self.Signature_nsprefix_ + ':' if (UseCapturedNS_ and self.Signature_nsprefix_) else ''
            self.Signature.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='Signature', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('versione', node)
        if value is not None and 'versione' not in already_processed:
            already_processed.add('versione')
            self.versione = value
            self.validate_FormatoTrasmissioneType(self.versione)    # validate type FormatoTrasmissioneType
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'FatturaElettronicaHeader':
            obj_ = FatturaElettronicaHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FatturaElettronicaHeader = obj_
            obj_.original_tagname_ = 'FatturaElettronicaHeader'
        elif nodeName_ == 'FatturaElettronicaBody':
            obj_ = FatturaElettronicaBodyType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FatturaElettronicaBody.append(obj_)
            obj_.original_tagname_ = 'FatturaElettronicaBody'
        elif nodeName_ == 'Signature':
            obj_ = SignatureType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Signature = obj_
            obj_.original_tagname_ = 'Signature'
# end class FatturaElettronicaType


class FatturaElettronicaHeaderType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DatiTrasmissione=None, CedentePrestatore=None, RappresentanteFiscale=None, CessionarioCommittente=None, TerzoIntermediarioOSoggettoEmittente=None, SoggettoEmittente=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiTrasmissione: "DatiTrasmissioneType" = DatiTrasmissione
        self.DatiTrasmissione_nsprefix_ = None
        self.CedentePrestatore: "CedentePrestatoreType" = CedentePrestatore
        self.CedentePrestatore_nsprefix_ = None
        self.RappresentanteFiscale = RappresentanteFiscale
        self.RappresentanteFiscale_nsprefix_ = None
        self.CessionarioCommittente = CessionarioCommittente
        self.CessionarioCommittente_nsprefix_ = None
        self.TerzoIntermediarioOSoggettoEmittente = TerzoIntermediarioOSoggettoEmittente
        self.TerzoIntermediarioOSoggettoEmittente_nsprefix_ = None
        self.SoggettoEmittente = SoggettoEmittente
        self.validate_SoggettoEmittenteType(self.SoggettoEmittente)
        self.SoggettoEmittente_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FatturaElettronicaHeaderType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FatturaElettronicaHeaderType.subclass:
            return FatturaElettronicaHeaderType.subclass(*args_, **kwargs_)
        else:
            return FatturaElettronicaHeaderType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiTrasmissione(self):
        return self.DatiTrasmissione
    def set_DatiTrasmissione(self, DatiTrasmissione):
        self.DatiTrasmissione = DatiTrasmissione
    def get_CedentePrestatore(self):
        return self.CedentePrestatore
    def set_CedentePrestatore(self, CedentePrestatore):
        self.CedentePrestatore = CedentePrestatore
    def get_RappresentanteFiscale(self):
        return self.RappresentanteFiscale
    def set_RappresentanteFiscale(self, RappresentanteFiscale):
        self.RappresentanteFiscale = RappresentanteFiscale
    def get_CessionarioCommittente(self):
        return self.CessionarioCommittente
    def set_CessionarioCommittente(self, CessionarioCommittente):
        self.CessionarioCommittente = CessionarioCommittente
    def get_TerzoIntermediarioOSoggettoEmittente(self):
        return self.TerzoIntermediarioOSoggettoEmittente
    def set_TerzoIntermediarioOSoggettoEmittente(self, TerzoIntermediarioOSoggettoEmittente):
        self.TerzoIntermediarioOSoggettoEmittente = TerzoIntermediarioOSoggettoEmittente
    def get_SoggettoEmittente(self):
        return self.SoggettoEmittente
    def set_SoggettoEmittente(self, SoggettoEmittente):
        self.SoggettoEmittente = SoggettoEmittente
    def validate_SoggettoEmittenteType(self, value):
        result = True
        # Validate type SoggettoEmittenteType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CC', 'TZ']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SoggettoEmittenteType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on SoggettoEmittenteType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.DatiTrasmissione is not None or
            self.CedentePrestatore is not None or
            self.RappresentanteFiscale is not None or
            self.CessionarioCommittente is not None or
            self.TerzoIntermediarioOSoggettoEmittente is not None or
            self.SoggettoEmittente is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='FatturaElettronicaHeaderType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FatturaElettronicaHeaderType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FatturaElettronicaHeaderType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FatturaElettronicaHeaderType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FatturaElettronicaHeaderType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FatturaElettronicaHeaderType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='FatturaElettronicaHeaderType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiTrasmissione is not None:
            namespaceprefix_ = self.DatiTrasmissione_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiTrasmissione_nsprefix_) else ''
            self.DatiTrasmissione.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiTrasmissione', pretty_print=pretty_print)
        if self.CedentePrestatore is not None:
            namespaceprefix_ = self.CedentePrestatore_nsprefix_ + ':' if (UseCapturedNS_ and self.CedentePrestatore_nsprefix_) else ''
            self.CedentePrestatore.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CedentePrestatore', pretty_print=pretty_print)
        if self.RappresentanteFiscale is not None:
            namespaceprefix_ = self.RappresentanteFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.RappresentanteFiscale_nsprefix_) else ''
            self.RappresentanteFiscale.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RappresentanteFiscale', pretty_print=pretty_print)
        if self.CessionarioCommittente is not None:
            namespaceprefix_ = self.CessionarioCommittente_nsprefix_ + ':' if (UseCapturedNS_ and self.CessionarioCommittente_nsprefix_) else ''
            self.CessionarioCommittente.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CessionarioCommittente', pretty_print=pretty_print)
        if self.TerzoIntermediarioOSoggettoEmittente is not None:
            namespaceprefix_ = self.TerzoIntermediarioOSoggettoEmittente_nsprefix_ + ':' if (UseCapturedNS_ and self.TerzoIntermediarioOSoggettoEmittente_nsprefix_) else ''
            self.TerzoIntermediarioOSoggettoEmittente.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TerzoIntermediarioOSoggettoEmittente', pretty_print=pretty_print)
        if self.SoggettoEmittente is not None:
            namespaceprefix_ = self.SoggettoEmittente_nsprefix_ + ':' if (UseCapturedNS_ and self.SoggettoEmittente_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSoggettoEmittente>%s</%sSoggettoEmittente>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SoggettoEmittente), input_name='SoggettoEmittente')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiTrasmissione':
            obj_ = DatiTrasmissioneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiTrasmissione = obj_
            obj_.original_tagname_ = 'DatiTrasmissione'
        elif nodeName_ == 'CedentePrestatore':
            obj_ = CedentePrestatoreType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CedentePrestatore = obj_
            obj_.original_tagname_ = 'CedentePrestatore'
        elif nodeName_ == 'RappresentanteFiscale':
            obj_ = RappresentanteFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RappresentanteFiscale = obj_
            obj_.original_tagname_ = 'RappresentanteFiscale'
        elif nodeName_ == 'CessionarioCommittente':
            obj_ = CessionarioCommittenteType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CessionarioCommittente = obj_
            obj_.original_tagname_ = 'CessionarioCommittente'
        elif nodeName_ == 'TerzoIntermediarioOSoggettoEmittente':
            obj_ = TerzoIntermediarioSoggettoEmittenteType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TerzoIntermediarioOSoggettoEmittente = obj_
            obj_.original_tagname_ = 'TerzoIntermediarioOSoggettoEmittente'
        elif nodeName_ == 'SoggettoEmittente':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SoggettoEmittente')
            value_ = self.gds_validate_string(value_, node, 'SoggettoEmittente')
            self.SoggettoEmittente = value_
            self.SoggettoEmittente_nsprefix_ = child_.prefix
            # validate type SoggettoEmittenteType
            self.validate_SoggettoEmittenteType(self.SoggettoEmittente)
# end class FatturaElettronicaHeaderType


class FatturaElettronicaBodyType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def compute_total_from_dati_generali(self) -> float:
        return float(self.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento) \
               - float(self.DatiGenerali.DatiGeneraliDocumento.Arrotondamento)

    def compute_total_from_dati_riepilogo(self) -> float:
        result = 0.0
        for x in self.DatiBeniServizi.DatiRiepilogo:
            result += float(x.ImponibileImporto)
        return result

    def compute_total_from_total_in_lines(self) -> float:
        result = 0.0
        for x in self.DatiBeniServizi.DettaglioLinee:
            result += float(x.PrezzoTotale)
        return result

    def compute_total_from_raw_data_lines(self) -> float:
        result = 0.0
        for x in self.DatiBeniServizi.DettaglioLinee:
            result += float(x.Quantita) * float(x.PrezzoUnitario)
        return result



    def __init__(self, DatiGenerali=None, DatiBeniServizi=None, DatiVeicoli=None, DatiPagamento=None, Allegati=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiGenerali: "DatiGeneraliType" = DatiGenerali
        self.DatiGenerali_nsprefix_ = None
        self.DatiBeniServizi: "DatiBeniServiziType" = DatiBeniServizi
        self.DatiBeniServizi_nsprefix_ = None
        self.DatiVeicoli: "DatiVeicoliType" = DatiVeicoli
        self.DatiVeicoli_nsprefix_ = None
        if DatiPagamento is None:
            self.DatiPagamento = []
        else:
            self.DatiPagamento = DatiPagamento
        self.DatiPagamento_nsprefix_ = None
        if Allegati is None:
            self.Allegati = []
        else:
            self.Allegati = Allegati
        self.Allegati_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FatturaElettronicaBodyType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FatturaElettronicaBodyType.subclass:
            return FatturaElettronicaBodyType.subclass(*args_, **kwargs_)
        else:
            return FatturaElettronicaBodyType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiGenerali(self):
        return self.DatiGenerali
    def set_DatiGenerali(self, DatiGenerali):
        self.DatiGenerali = DatiGenerali
    def get_DatiBeniServizi(self):
        return self.DatiBeniServizi
    def set_DatiBeniServizi(self, DatiBeniServizi):
        self.DatiBeniServizi = DatiBeniServizi
    def get_DatiVeicoli(self):
        return self.DatiVeicoli
    def set_DatiVeicoli(self, DatiVeicoli):
        self.DatiVeicoli = DatiVeicoli
    def get_DatiPagamento(self):
        return self.DatiPagamento
    def set_DatiPagamento(self, DatiPagamento):
        self.DatiPagamento = DatiPagamento
    def add_DatiPagamento(self, value):
        self.DatiPagamento.append(value)
    def insert_DatiPagamento_at(self, index, value):
        self.DatiPagamento.insert(index, value)
    def replace_DatiPagamento_at(self, index, value):
        self.DatiPagamento[index] = value
    def get_Allegati(self):
        return self.Allegati
    def set_Allegati(self, Allegati):
        self.Allegati = Allegati
    def add_Allegati(self, value):
        self.Allegati.append(value)
    def insert_Allegati_at(self, index, value):
        self.Allegati.insert(index, value)
    def replace_Allegati_at(self, index, value):
        self.Allegati[index] = value
    def _hasContent(self):
        if (
            self.DatiGenerali is not None or
            self.DatiBeniServizi is not None or
            self.DatiVeicoli is not None or
            self.DatiPagamento or
            self.Allegati
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='FatturaElettronicaBodyType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FatturaElettronicaBodyType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FatturaElettronicaBodyType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FatturaElettronicaBodyType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FatturaElettronicaBodyType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FatturaElettronicaBodyType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='FatturaElettronicaBodyType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiGenerali is not None:
            namespaceprefix_ = self.DatiGenerali_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiGenerali_nsprefix_) else ''
            self.DatiGenerali.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiGenerali', pretty_print=pretty_print)
        if self.DatiBeniServizi is not None:
            namespaceprefix_ = self.DatiBeniServizi_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiBeniServizi_nsprefix_) else ''
            self.DatiBeniServizi.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiBeniServizi', pretty_print=pretty_print)
        if self.DatiVeicoli is not None:
            namespaceprefix_ = self.DatiVeicoli_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiVeicoli_nsprefix_) else ''
            self.DatiVeicoli.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiVeicoli', pretty_print=pretty_print)
        for DatiPagamento_ in self.DatiPagamento:
            namespaceprefix_ = self.DatiPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiPagamento_nsprefix_) else ''
            DatiPagamento_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiPagamento', pretty_print=pretty_print)
        for Allegati_ in self.Allegati:
            namespaceprefix_ = self.Allegati_nsprefix_ + ':' if (UseCapturedNS_ and self.Allegati_nsprefix_) else ''
            Allegati_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Allegati', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiGenerali':
            obj_ = DatiGeneraliType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiGenerali = obj_
            obj_.original_tagname_ = 'DatiGenerali'
        elif nodeName_ == 'DatiBeniServizi':
            obj_ = DatiBeniServiziType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiBeniServizi = obj_
            obj_.original_tagname_ = 'DatiBeniServizi'
        elif nodeName_ == 'DatiVeicoli':
            obj_ = DatiVeicoliType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiVeicoli = obj_
            obj_.original_tagname_ = 'DatiVeicoli'
        elif nodeName_ == 'DatiPagamento':
            obj_ = DatiPagamentoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiPagamento.append(obj_)
            obj_.original_tagname_ = 'DatiPagamento'
        elif nodeName_ == 'Allegati':
            obj_ = AllegatiType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Allegati.append(obj_)
            obj_.original_tagname_ = 'Allegati'
# end class FatturaElettronicaBodyType


class DatiTrasmissioneType(GeneratedsSuper):
    """DatiTrasmissioneType -- Blocco relativo ai dati di trasmissione della Fattura Elettronica
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdTrasmittente=None, ProgressivoInvio=None, FormatoTrasmissione=None, CodiceDestinatario=None, ContattiTrasmittente=None, PECDestinatario=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdTrasmittente = IdTrasmittente
        self.IdTrasmittente_nsprefix_ = None
        self.ProgressivoInvio = ProgressivoInvio
        self.validate_String10Type(self.ProgressivoInvio)
        self.ProgressivoInvio_nsprefix_ = None
        self.FormatoTrasmissione = FormatoTrasmissione
        self.validate_FormatoTrasmissioneType(self.FormatoTrasmissione)
        self.FormatoTrasmissione_nsprefix_ = None
        self.CodiceDestinatario = CodiceDestinatario
        self.validate_CodiceDestinatarioType(self.CodiceDestinatario)
        self.CodiceDestinatario_nsprefix_ = None
        self.ContattiTrasmittente = ContattiTrasmittente
        self.ContattiTrasmittente_nsprefix_ = None
        self.PECDestinatario = PECDestinatario
        self.validate_EmailType(self.PECDestinatario)
        self.PECDestinatario_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiTrasmissioneType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiTrasmissioneType.subclass:
            return DatiTrasmissioneType.subclass(*args_, **kwargs_)
        else:
            return DatiTrasmissioneType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdTrasmittente(self):
        return self.IdTrasmittente
    def set_IdTrasmittente(self, IdTrasmittente):
        self.IdTrasmittente = IdTrasmittente
    def get_ProgressivoInvio(self):
        return self.ProgressivoInvio
    def set_ProgressivoInvio(self, ProgressivoInvio):
        self.ProgressivoInvio = ProgressivoInvio
    def get_FormatoTrasmissione(self):
        return self.FormatoTrasmissione
    def set_FormatoTrasmissione(self, FormatoTrasmissione):
        self.FormatoTrasmissione = FormatoTrasmissione
    def get_CodiceDestinatario(self):
        return self.CodiceDestinatario
    def set_CodiceDestinatario(self, CodiceDestinatario):
        self.CodiceDestinatario = CodiceDestinatario
    def get_ContattiTrasmittente(self):
        return self.ContattiTrasmittente
    def set_ContattiTrasmittente(self, ContattiTrasmittente):
        self.ContattiTrasmittente = ContattiTrasmittente
    def get_PECDestinatario(self):
        return self.PECDestinatario
    def set_PECDestinatario(self, PECDestinatario):
        self.PECDestinatario = PECDestinatario
    def validate_String10Type(self, value):
        result = True
        # Validate type String10Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String10Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String10Type_patterns_, ))
                result = False
        return result
    validate_String10Type_patterns_ = [['^(([\x00-\x7f]{1,10}))$']]
    def validate_FormatoTrasmissioneType(self, value):
        result = True
        # Validate type FormatoTrasmissioneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FPA12', 'FPR12']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on FormatoTrasmissioneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on FormatoTrasmissioneType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CodiceDestinatarioType(self, value):
        result = True
        # Validate type CodiceDestinatarioType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CodiceDestinatarioType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CodiceDestinatarioType_patterns_, ))
                result = False
        return result
    validate_CodiceDestinatarioType_patterns_ = [['^([A-Z0-9]{6,7})$']]
    def validate_EmailType(self, value):
        result = True
        # Validate type EmailType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on EmailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailType_patterns_, ))
                result = False
        return result
    validate_EmailType_patterns_ = [['^(.+@.+[.]+.+)$']]
    def _hasContent(self):
        if (
            self.IdTrasmittente is not None or
            self.ProgressivoInvio is not None or
            self.FormatoTrasmissione is not None or
            self.CodiceDestinatario is not None or
            self.ContattiTrasmittente is not None or
            self.PECDestinatario is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiTrasmissioneType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiTrasmissioneType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiTrasmissioneType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiTrasmissioneType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiTrasmissioneType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiTrasmissioneType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiTrasmissioneType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdTrasmittente is not None:
            namespaceprefix_ = self.IdTrasmittente_nsprefix_ + ':' if (UseCapturedNS_ and self.IdTrasmittente_nsprefix_) else ''
            self.IdTrasmittente.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdTrasmittente', pretty_print=pretty_print)
        if self.ProgressivoInvio is not None:
            namespaceprefix_ = self.ProgressivoInvio_nsprefix_ + ':' if (UseCapturedNS_ and self.ProgressivoInvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProgressivoInvio>%s</%sProgressivoInvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProgressivoInvio), input_name='ProgressivoInvio')), namespaceprefix_ , eol_))
        if self.FormatoTrasmissione is not None:
            namespaceprefix_ = self.FormatoTrasmissione_nsprefix_ + ':' if (UseCapturedNS_ and self.FormatoTrasmissione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFormatoTrasmissione>%s</%sFormatoTrasmissione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FormatoTrasmissione), input_name='FormatoTrasmissione')), namespaceprefix_ , eol_))
        if self.CodiceDestinatario is not None:
            namespaceprefix_ = self.CodiceDestinatario_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceDestinatario_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceDestinatario>%s</%sCodiceDestinatario>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceDestinatario), input_name='CodiceDestinatario')), namespaceprefix_ , eol_))
        if self.ContattiTrasmittente is not None:
            namespaceprefix_ = self.ContattiTrasmittente_nsprefix_ + ':' if (UseCapturedNS_ and self.ContattiTrasmittente_nsprefix_) else ''
            self.ContattiTrasmittente.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ContattiTrasmittente', pretty_print=pretty_print)
        if self.PECDestinatario is not None:
            namespaceprefix_ = self.PECDestinatario_nsprefix_ + ':' if (UseCapturedNS_ and self.PECDestinatario_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPECDestinatario>%s</%sPECDestinatario>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PECDestinatario), input_name='PECDestinatario')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdTrasmittente':
            obj_ = IdFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdTrasmittente = obj_
            obj_.original_tagname_ = 'IdTrasmittente'
        elif nodeName_ == 'ProgressivoInvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProgressivoInvio')
            value_ = self.gds_validate_string(value_, node, 'ProgressivoInvio')
            self.ProgressivoInvio = value_
            self.ProgressivoInvio_nsprefix_ = child_.prefix
            # validate type String10Type
            self.validate_String10Type(self.ProgressivoInvio)
        elif nodeName_ == 'FormatoTrasmissione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FormatoTrasmissione')
            value_ = self.gds_validate_string(value_, node, 'FormatoTrasmissione')
            self.FormatoTrasmissione = value_
            self.FormatoTrasmissione_nsprefix_ = child_.prefix
            # validate type FormatoTrasmissioneType
            self.validate_FormatoTrasmissioneType(self.FormatoTrasmissione)
        elif nodeName_ == 'CodiceDestinatario':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceDestinatario')
            value_ = self.gds_validate_string(value_, node, 'CodiceDestinatario')
            self.CodiceDestinatario = value_
            self.CodiceDestinatario_nsprefix_ = child_.prefix
            # validate type CodiceDestinatarioType
            self.validate_CodiceDestinatarioType(self.CodiceDestinatario)
        elif nodeName_ == 'ContattiTrasmittente':
            obj_ = ContattiTrasmittenteType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ContattiTrasmittente = obj_
            obj_.original_tagname_ = 'ContattiTrasmittente'
        elif nodeName_ == 'PECDestinatario':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PECDestinatario')
            value_ = self.gds_validate_string(value_, node, 'PECDestinatario')
            self.PECDestinatario = value_
            self.PECDestinatario_nsprefix_ = child_.prefix
            # validate type EmailType
            self.validate_EmailType(self.PECDestinatario)
# end class DatiTrasmissioneType


class IdFiscaleType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdPaese=None, IdCodice=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdPaese = IdPaese
        self.validate_NazioneType(self.IdPaese)
        self.IdPaese_nsprefix_ = None
        self.IdCodice = IdCodice
        self.validate_CodiceType(self.IdCodice)
        self.IdCodice_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IdFiscaleType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IdFiscaleType.subclass:
            return IdFiscaleType.subclass(*args_, **kwargs_)
        else:
            return IdFiscaleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdPaese(self):
        return self.IdPaese
    def set_IdPaese(self, IdPaese):
        self.IdPaese = IdPaese
    def get_IdCodice(self):
        return self.IdCodice
    def set_IdCodice(self, IdCodice):
        self.IdCodice = IdCodice
    def validate_NazioneType(self, value):
        result = True
        # Validate type NazioneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_NazioneType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_NazioneType_patterns_, ))
                result = False
        return result
    validate_NazioneType_patterns_ = [['^([A-Z]{2})$']]
    def validate_CodiceType(self, value):
        result = True
        # Validate type CodiceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 28:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CodiceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CodiceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.IdPaese is not None or
            self.IdCodice is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='IdFiscaleType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IdFiscaleType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IdFiscaleType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IdFiscaleType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IdFiscaleType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IdFiscaleType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='IdFiscaleType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdPaese is not None:
            namespaceprefix_ = self.IdPaese_nsprefix_ + ':' if (UseCapturedNS_ and self.IdPaese_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdPaese>%s</%sIdPaese>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdPaese), input_name='IdPaese')), namespaceprefix_ , eol_))
        if self.IdCodice is not None:
            namespaceprefix_ = self.IdCodice_nsprefix_ + ':' if (UseCapturedNS_ and self.IdCodice_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdCodice>%s</%sIdCodice>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdCodice), input_name='IdCodice')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdPaese':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdPaese')
            value_ = self.gds_validate_string(value_, node, 'IdPaese')
            self.IdPaese = value_
            self.IdPaese_nsprefix_ = child_.prefix
            # validate type NazioneType
            self.validate_NazioneType(self.IdPaese)
        elif nodeName_ == 'IdCodice':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdCodice')
            value_ = self.gds_validate_string(value_, node, 'IdCodice')
            self.IdCodice = value_
            self.IdCodice_nsprefix_ = child_.prefix
            # validate type CodiceType
            self.validate_CodiceType(self.IdCodice)
# end class IdFiscaleType


class ContattiTrasmittenteType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Telefono=None, Email=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Telefono = Telefono
        self.validate_TelFaxType(self.Telefono)
        self.Telefono_nsprefix_ = None
        self.Email = Email
        self.validate_EmailType(self.Email)
        self.Email_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ContattiTrasmittenteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ContattiTrasmittenteType.subclass:
            return ContattiTrasmittenteType.subclass(*args_, **kwargs_)
        else:
            return ContattiTrasmittenteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Telefono(self):
        return self.Telefono
    def set_Telefono(self, Telefono):
        self.Telefono = Telefono
    def get_Email(self):
        return self.Email
    def set_Email(self, Email):
        self.Email = Email
    def validate_TelFaxType(self, value):
        result = True
        # Validate type TelFaxType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_TelFaxType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_TelFaxType_patterns_, ))
                result = False
        return result
    validate_TelFaxType_patterns_ = [['^(([\x00-\x7f]{5,12}))$']]
    def validate_EmailType(self, value):
        result = True
        # Validate type EmailType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on EmailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailType_patterns_, ))
                result = False
        return result
    validate_EmailType_patterns_ = [['^(.+@.+[.]+.+)$']]
    def _hasContent(self):
        if (
            self.Telefono is not None or
            self.Email is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ContattiTrasmittenteType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ContattiTrasmittenteType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ContattiTrasmittenteType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ContattiTrasmittenteType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ContattiTrasmittenteType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ContattiTrasmittenteType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ContattiTrasmittenteType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Telefono is not None:
            namespaceprefix_ = self.Telefono_nsprefix_ + ':' if (UseCapturedNS_ and self.Telefono_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTelefono>%s</%sTelefono>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Telefono), input_name='Telefono')), namespaceprefix_ , eol_))
        if self.Email is not None:
            namespaceprefix_ = self.Email_nsprefix_ + ':' if (UseCapturedNS_ and self.Email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmail>%s</%sEmail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Email), input_name='Email')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Telefono':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Telefono')
            value_ = self.gds_validate_string(value_, node, 'Telefono')
            self.Telefono = value_
            self.Telefono_nsprefix_ = child_.prefix
            # validate type TelFaxType
            self.validate_TelFaxType(self.Telefono)
        elif nodeName_ == 'Email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Email')
            value_ = self.gds_validate_string(value_, node, 'Email')
            self.Email = value_
            self.Email_nsprefix_ = child_.prefix
            # validate type EmailType
            self.validate_EmailType(self.Email)
# end class ContattiTrasmittenteType


class DatiGeneraliType(GeneratedsSuper):
    """DatiGeneraliType --
    Blocco relativo ai Dati Generali della Fattura Elettronica
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DatiGeneraliDocumento=None, DatiOrdineAcquisto=None, DatiContratto=None, DatiConvenzione=None, DatiRicezione=None, DatiFattureCollegate=None, DatiSAL=None, DatiDDT=None, DatiTrasporto=None, FatturaPrincipale=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiGeneraliDocumento: "DatiGeneraliDocumentoType" = DatiGeneraliDocumento
        self.DatiGeneraliDocumento_nsprefix_ = None
        if DatiOrdineAcquisto is None:
            self.DatiOrdineAcquisto: List["DatiOrdineAcquistoType"] = []
        else:
            self.DatiOrdineAcquisto: List["DatiOrdineAcquistoType"] = DatiOrdineAcquisto
        self.DatiOrdineAcquisto_nsprefix_ = None
        if DatiContratto is None:
            self.DatiContratto: List["DatiContrattoType"] = []
        else:
            self.DatiContratto: List["DatiContrattoType"] = DatiContratto
        self.DatiContratto_nsprefix_ = None
        if DatiConvenzione is None:
            self.DatiConvenzione: List["DatiConvenzioneType"] = []
        else:
            self.DatiConvenzione: List["DatiConvenzioneType"] = DatiConvenzione
        self.DatiConvenzione_nsprefix_ = None
        if DatiRicezione is None:
            self.DatiRicezione: List["DatiRicezioneType"] = []
        else:
            self.DatiRicezione: List["DatiRicezioneType"] = DatiRicezione
        self.DatiRicezione_nsprefix_ = None
        if DatiFattureCollegate is None:
            self.DatiFattureCollegate: List["DatiFattureCollegateType"] = []
        else:
            self.DatiFattureCollegate: List["DatiFattureCollegateType"] = DatiFattureCollegate
        self.DatiFattureCollegate_nsprefix_ = None
        if DatiSAL is None:
            self.DatiSAL: List["DatiSALType"] = []
        else:
            self.DatiSAL: List["DatiSALType"] = DatiSAL
        self.DatiSAL_nsprefix_ = None
        if DatiDDT is None:
            self.DatiDDT: List["DatiDDTType"] = []
        else:
            self.DatiDDT: List["DatiDDTType"] = DatiDDT
        self.DatiDDT_nsprefix_ = None
        self.DatiTrasporto: "DatiTrasporto" = DatiTrasporto
        self.DatiTrasporto_nsprefix_ = None
        self.FatturaPrincipale: "FatturaPrincipale" = FatturaPrincipale
        self.FatturaPrincipale_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiGeneraliType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiGeneraliType.subclass:
            return DatiGeneraliType.subclass(*args_, **kwargs_)
        else:
            return DatiGeneraliType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiGeneraliDocumento(self):
        return self.DatiGeneraliDocumento
    def set_DatiGeneraliDocumento(self, DatiGeneraliDocumento):
        self.DatiGeneraliDocumento = DatiGeneraliDocumento
    def get_DatiOrdineAcquisto(self):
        return self.DatiOrdineAcquisto
    def set_DatiOrdineAcquisto(self, DatiOrdineAcquisto):
        self.DatiOrdineAcquisto = DatiOrdineAcquisto
    def add_DatiOrdineAcquisto(self, value):
        self.DatiOrdineAcquisto.append(value)
    def insert_DatiOrdineAcquisto_at(self, index, value):
        self.DatiOrdineAcquisto.insert(index, value)
    def replace_DatiOrdineAcquisto_at(self, index, value):
        self.DatiOrdineAcquisto[index] = value
    def get_DatiContratto(self):
        return self.DatiContratto
    def set_DatiContratto(self, DatiContratto):
        self.DatiContratto = DatiContratto
    def add_DatiContratto(self, value):
        self.DatiContratto.append(value)
    def insert_DatiContratto_at(self, index, value):
        self.DatiContratto.insert(index, value)
    def replace_DatiContratto_at(self, index, value):
        self.DatiContratto[index] = value
    def get_DatiConvenzione(self):
        return self.DatiConvenzione
    def set_DatiConvenzione(self, DatiConvenzione):
        self.DatiConvenzione = DatiConvenzione
    def add_DatiConvenzione(self, value):
        self.DatiConvenzione.append(value)
    def insert_DatiConvenzione_at(self, index, value):
        self.DatiConvenzione.insert(index, value)
    def replace_DatiConvenzione_at(self, index, value):
        self.DatiConvenzione[index] = value
    def get_DatiRicezione(self):
        return self.DatiRicezione
    def set_DatiRicezione(self, DatiRicezione):
        self.DatiRicezione = DatiRicezione
    def add_DatiRicezione(self, value):
        self.DatiRicezione.append(value)
    def insert_DatiRicezione_at(self, index, value):
        self.DatiRicezione.insert(index, value)
    def replace_DatiRicezione_at(self, index, value):
        self.DatiRicezione[index] = value
    def get_DatiFattureCollegate(self):
        return self.DatiFattureCollegate
    def set_DatiFattureCollegate(self, DatiFattureCollegate):
        self.DatiFattureCollegate = DatiFattureCollegate
    def add_DatiFattureCollegate(self, value):
        self.DatiFattureCollegate.append(value)
    def insert_DatiFattureCollegate_at(self, index, value):
        self.DatiFattureCollegate.insert(index, value)
    def replace_DatiFattureCollegate_at(self, index, value):
        self.DatiFattureCollegate[index] = value
    def get_DatiSAL(self):
        return self.DatiSAL
    def set_DatiSAL(self, DatiSAL):
        self.DatiSAL = DatiSAL
    def add_DatiSAL(self, value):
        self.DatiSAL.append(value)
    def insert_DatiSAL_at(self, index, value):
        self.DatiSAL.insert(index, value)
    def replace_DatiSAL_at(self, index, value):
        self.DatiSAL[index] = value
    def get_DatiDDT(self):
        return self.DatiDDT
    def set_DatiDDT(self, DatiDDT):
        self.DatiDDT = DatiDDT
    def add_DatiDDT(self, value):
        self.DatiDDT.append(value)
    def insert_DatiDDT_at(self, index, value):
        self.DatiDDT.insert(index, value)
    def replace_DatiDDT_at(self, index, value):
        self.DatiDDT[index] = value
    def get_DatiTrasporto(self):
        return self.DatiTrasporto
    def set_DatiTrasporto(self, DatiTrasporto):
        self.DatiTrasporto = DatiTrasporto
    def get_FatturaPrincipale(self):
        return self.FatturaPrincipale
    def set_FatturaPrincipale(self, FatturaPrincipale):
        self.FatturaPrincipale = FatturaPrincipale
    def _hasContent(self):
        if (
            self.DatiGeneraliDocumento is not None or
            self.DatiOrdineAcquisto or
            self.DatiContratto or
            self.DatiConvenzione or
            self.DatiRicezione or
            self.DatiFattureCollegate or
            self.DatiSAL or
            self.DatiDDT or
            self.DatiTrasporto is not None or
            self.FatturaPrincipale is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiGeneraliType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiGeneraliType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiGeneraliType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiGeneraliType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiGeneraliType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiGeneraliType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiGeneraliType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiGeneraliDocumento is not None:
            namespaceprefix_ = self.DatiGeneraliDocumento_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiGeneraliDocumento_nsprefix_) else ''
            self.DatiGeneraliDocumento.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiGeneraliDocumento', pretty_print=pretty_print)
        for DatiOrdineAcquisto_ in self.DatiOrdineAcquisto:
            namespaceprefix_ = self.DatiOrdineAcquisto_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiOrdineAcquisto_nsprefix_) else ''
            DatiOrdineAcquisto_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiOrdineAcquisto', pretty_print=pretty_print)
        for DatiContratto_ in self.DatiContratto:
            namespaceprefix_ = self.DatiContratto_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiContratto_nsprefix_) else ''
            DatiContratto_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiContratto', pretty_print=pretty_print)
        for DatiConvenzione_ in self.DatiConvenzione:
            namespaceprefix_ = self.DatiConvenzione_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiConvenzione_nsprefix_) else ''
            DatiConvenzione_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiConvenzione', pretty_print=pretty_print)
        for DatiRicezione_ in self.DatiRicezione:
            namespaceprefix_ = self.DatiRicezione_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiRicezione_nsprefix_) else ''
            DatiRicezione_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiRicezione', pretty_print=pretty_print)
        for DatiFattureCollegate_ in self.DatiFattureCollegate:
            namespaceprefix_ = self.DatiFattureCollegate_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiFattureCollegate_nsprefix_) else ''
            DatiFattureCollegate_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiFattureCollegate', pretty_print=pretty_print)
        for DatiSAL_ in self.DatiSAL:
            namespaceprefix_ = self.DatiSAL_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiSAL_nsprefix_) else ''
            DatiSAL_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiSAL', pretty_print=pretty_print)
        for DatiDDT_ in self.DatiDDT:
            namespaceprefix_ = self.DatiDDT_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiDDT_nsprefix_) else ''
            DatiDDT_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiDDT', pretty_print=pretty_print)
        if self.DatiTrasporto is not None:
            namespaceprefix_ = self.DatiTrasporto_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiTrasporto_nsprefix_) else ''
            self.DatiTrasporto.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiTrasporto', pretty_print=pretty_print)
        if self.FatturaPrincipale is not None:
            namespaceprefix_ = self.FatturaPrincipale_nsprefix_ + ':' if (UseCapturedNS_ and self.FatturaPrincipale_nsprefix_) else ''
            self.FatturaPrincipale.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FatturaPrincipale', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiGeneraliDocumento':
            obj_ = DatiGeneraliDocumentoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiGeneraliDocumento = obj_
            obj_.original_tagname_ = 'DatiGeneraliDocumento'
        elif nodeName_ == 'DatiOrdineAcquisto':
            obj_ = DatiDocumentiCorrelatiType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiOrdineAcquisto.append(obj_)
            obj_.original_tagname_ = 'DatiOrdineAcquisto'
        elif nodeName_ == 'DatiContratto':
            obj_ = DatiDocumentiCorrelatiType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiContratto.append(obj_)
            obj_.original_tagname_ = 'DatiContratto'
        elif nodeName_ == 'DatiConvenzione':
            obj_ = DatiDocumentiCorrelatiType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiConvenzione.append(obj_)
            obj_.original_tagname_ = 'DatiConvenzione'
        elif nodeName_ == 'DatiRicezione':
            obj_ = DatiDocumentiCorrelatiType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiRicezione.append(obj_)
            obj_.original_tagname_ = 'DatiRicezione'
        elif nodeName_ == 'DatiFattureCollegate':
            obj_ = DatiDocumentiCorrelatiType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiFattureCollegate.append(obj_)
            obj_.original_tagname_ = 'DatiFattureCollegate'
        elif nodeName_ == 'DatiSAL':
            obj_ = DatiSALType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiSAL.append(obj_)
            obj_.original_tagname_ = 'DatiSAL'
        elif nodeName_ == 'DatiDDT':
            obj_ = DatiDDTType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiDDT.append(obj_)
            obj_.original_tagname_ = 'DatiDDT'
        elif nodeName_ == 'DatiTrasporto':
            obj_ = DatiTrasportoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiTrasporto = obj_
            obj_.original_tagname_ = 'DatiTrasporto'
        elif nodeName_ == 'FatturaPrincipale':
            obj_ = FatturaPrincipaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FatturaPrincipale = obj_
            obj_.original_tagname_ = 'FatturaPrincipale'
# end class DatiGeneraliType


class DatiGeneraliDocumentoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TipoDocumento=None, Divisa=None, Data=None, Numero=None, DatiRitenuta=None, DatiBollo=None, DatiCassaPrevidenziale=None, ScontoMaggiorazione=None, ImportoTotaleDocumento=None, Arrotondamento=None, Causale=None, Art73=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TipoDocumento: "TipoDocumentoType" = TipoDocumento
        self.validate_TipoDocumentoType(self.TipoDocumento)
        self.TipoDocumento_nsprefix_ = None
        self.Divisa: str = Divisa
        self.validate_DivisaType(self.Divisa)
        self.Divisa_nsprefix_ = None
        if isinstance(Data, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Data, '%Y-%m-%d').date()
        else:
            initvalue_ = Data
        self.Data = initvalue_
        self.Data_nsprefix_ = None
        self.Numero: int = Numero
        self.validate_String20Type(self.Numero)
        self.Numero_nsprefix_ = None
        self.DatiRitenuta: "DatiRitenutaType" = DatiRitenuta
        self.DatiRitenuta_nsprefix_ = None
        self.DatiBollo: "DatiBolloType" = DatiBollo
        self.DatiBollo_nsprefix_ = None
        if DatiCassaPrevidenziale is None:
            self.DatiCassaPrevidenziale = []
        else:
            self.DatiCassaPrevidenziale = DatiCassaPrevidenziale
        self.DatiCassaPrevidenziale_nsprefix_ = None
        if ScontoMaggiorazione is None:
            self.ScontoMaggiorazione = []
        else:
            self.ScontoMaggiorazione = ScontoMaggiorazione
        self.ScontoMaggiorazione_nsprefix_ = None
        self.ImportoTotaleDocumento = ImportoTotaleDocumento
        self.validate_Amount2DecimalType(self.ImportoTotaleDocumento)
        self.ImportoTotaleDocumento_nsprefix_ = None
        self.Arrotondamento = Arrotondamento
        self.validate_Amount2DecimalType(self.Arrotondamento)
        self.Arrotondamento_nsprefix_ = None
        if Causale is None:
            self.Causale = []
        else:
            self.Causale = Causale
        self.Causale_nsprefix_ = None
        self.Art73 = Art73
        self.validate_Art73Type(self.Art73)
        self.Art73_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiGeneraliDocumentoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiGeneraliDocumentoType.subclass:
            return DatiGeneraliDocumentoType.subclass(*args_, **kwargs_)
        else:
            return DatiGeneraliDocumentoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TipoDocumento(self):
        return self.TipoDocumento
    def set_TipoDocumento(self, TipoDocumento):
        self.TipoDocumento = TipoDocumento
    def get_Divisa(self):
        return self.Divisa
    def set_Divisa(self, Divisa):
        self.Divisa = Divisa
    def get_Data(self):
        return self.Data
    def set_Data(self, Data):
        self.Data = Data
    def get_Numero(self):
        return self.Numero
    def set_Numero(self, Numero):
        self.Numero = Numero
    def get_DatiRitenuta(self):
        return self.DatiRitenuta
    def set_DatiRitenuta(self, DatiRitenuta):
        self.DatiRitenuta = DatiRitenuta
    def get_DatiBollo(self):
        return self.DatiBollo
    def set_DatiBollo(self, DatiBollo):
        self.DatiBollo = DatiBollo
    def get_DatiCassaPrevidenziale(self):
        return self.DatiCassaPrevidenziale
    def set_DatiCassaPrevidenziale(self, DatiCassaPrevidenziale):
        self.DatiCassaPrevidenziale = DatiCassaPrevidenziale
    def add_DatiCassaPrevidenziale(self, value):
        self.DatiCassaPrevidenziale.append(value)
    def insert_DatiCassaPrevidenziale_at(self, index, value):
        self.DatiCassaPrevidenziale.insert(index, value)
    def replace_DatiCassaPrevidenziale_at(self, index, value):
        self.DatiCassaPrevidenziale[index] = value
    def get_ScontoMaggiorazione(self):
        return self.ScontoMaggiorazione
    def set_ScontoMaggiorazione(self, ScontoMaggiorazione):
        self.ScontoMaggiorazione = ScontoMaggiorazione
    def add_ScontoMaggiorazione(self, value):
        self.ScontoMaggiorazione.append(value)
    def insert_ScontoMaggiorazione_at(self, index, value):
        self.ScontoMaggiorazione.insert(index, value)
    def replace_ScontoMaggiorazione_at(self, index, value):
        self.ScontoMaggiorazione[index] = value
    def get_ImportoTotaleDocumento(self):
        return self.ImportoTotaleDocumento
    def set_ImportoTotaleDocumento(self, ImportoTotaleDocumento):
        self.ImportoTotaleDocumento = ImportoTotaleDocumento
    def get_Arrotondamento(self):
        return self.Arrotondamento
    def set_Arrotondamento(self, Arrotondamento):
        self.Arrotondamento = Arrotondamento
    def get_Causale(self):
        return self.Causale
    def set_Causale(self, Causale):
        self.Causale = Causale
    def add_Causale(self, value):
        self.Causale.append(value)
    def insert_Causale_at(self, index, value):
        self.Causale.insert(index, value)
    def replace_Causale_at(self, index, value):
        self.Causale[index] = value
    def get_Art73(self):
        return self.Art73
    def set_Art73(self, Art73):
        self.Art73 = Art73
    def validate_TipoDocumentoType(self, value):
        result = True
        # Validate type TipoDocumentoType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['TD01', 'TD02', 'TD03', 'TD04', 'TD05', 'TD06']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TipoDocumentoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on TipoDocumentoType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DivisaType(self, value):
        result = True
        # Validate type DivisaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_DivisaType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_DivisaType_patterns_, ))
                result = False
        return result
    validate_DivisaType_patterns_ = [['^([A-Z]{3})$']]
    def validate_DataFatturaType(self, value):
        result = True
        # Validate type DataFatturaType, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            if value < self.gds_parse_date('1970-01-01'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on DataFatturaType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def validate_String200LatinType(self, value):
        result = True
        # Validate type String200LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String200LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String200LatinType_patterns_, ))
                result = False
        return result
    validate_String200LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,200})$']]
    def validate_Art73Type(self, value):
        result = True
        # Validate type Art73Type, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SI']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on Art73Type' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on Art73Type' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.TipoDocumento is not None or
            self.Divisa is not None or
            self.Data is not None or
            self.Numero is not None or
            self.DatiRitenuta is not None or
            self.DatiBollo is not None or
            self.DatiCassaPrevidenziale or
            self.ScontoMaggiorazione or
            self.ImportoTotaleDocumento is not None or
            self.Arrotondamento is not None or
            self.Causale or
            self.Art73 is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiGeneraliDocumentoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiGeneraliDocumentoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiGeneraliDocumentoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiGeneraliDocumentoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiGeneraliDocumentoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiGeneraliDocumentoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiGeneraliDocumentoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TipoDocumento is not None:
            namespaceprefix_ = self.TipoDocumento_nsprefix_ + ':' if (UseCapturedNS_ and self.TipoDocumento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTipoDocumento>%s</%sTipoDocumento>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TipoDocumento), input_name='TipoDocumento')), namespaceprefix_ , eol_))
        if self.Divisa is not None:
            namespaceprefix_ = self.Divisa_nsprefix_ + ':' if (UseCapturedNS_ and self.Divisa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDivisa>%s</%sDivisa>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Divisa), input_name='Divisa')), namespaceprefix_ , eol_))
        if self.Data is not None:
            namespaceprefix_ = self.Data_nsprefix_ + ':' if (UseCapturedNS_ and self.Data_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sData>%s</%sData>%s' % (namespaceprefix_ , self.gds_format_date(self.Data, input_name='Data'), namespaceprefix_ , eol_))
        if self.Numero is not None:
            namespaceprefix_ = self.Numero_nsprefix_ + ':' if (UseCapturedNS_ and self.Numero_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumero>%s</%sNumero>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Numero), input_name='Numero')), namespaceprefix_ , eol_))
        if self.DatiRitenuta is not None:
            namespaceprefix_ = self.DatiRitenuta_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiRitenuta_nsprefix_) else ''
            self.DatiRitenuta.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiRitenuta', pretty_print=pretty_print)
        if self.DatiBollo is not None:
            namespaceprefix_ = self.DatiBollo_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiBollo_nsprefix_) else ''
            self.DatiBollo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiBollo', pretty_print=pretty_print)
        for DatiCassaPrevidenziale_ in self.DatiCassaPrevidenziale:
            namespaceprefix_ = self.DatiCassaPrevidenziale_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiCassaPrevidenziale_nsprefix_) else ''
            DatiCassaPrevidenziale_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiCassaPrevidenziale', pretty_print=pretty_print)
        for ScontoMaggiorazione_ in self.ScontoMaggiorazione:
            namespaceprefix_ = self.ScontoMaggiorazione_nsprefix_ + ':' if (UseCapturedNS_ and self.ScontoMaggiorazione_nsprefix_) else ''
            ScontoMaggiorazione_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ScontoMaggiorazione', pretty_print=pretty_print)
        if self.ImportoTotaleDocumento is not None:
            namespaceprefix_ = self.ImportoTotaleDocumento_nsprefix_ + ':' if (UseCapturedNS_ and self.ImportoTotaleDocumento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImportoTotaleDocumento>%s</%sImportoTotaleDocumento>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ImportoTotaleDocumento, input_name='ImportoTotaleDocumento'), namespaceprefix_ , eol_))
        if self.Arrotondamento is not None:
            namespaceprefix_ = self.Arrotondamento_nsprefix_ + ':' if (UseCapturedNS_ and self.Arrotondamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sArrotondamento>%s</%sArrotondamento>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Arrotondamento, input_name='Arrotondamento'), namespaceprefix_ , eol_))
        for Causale_ in self.Causale:
            namespaceprefix_ = self.Causale_nsprefix_ + ':' if (UseCapturedNS_ and self.Causale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCausale>%s</%sCausale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Causale_), input_name='Causale')), namespaceprefix_ , eol_))
        if self.Art73 is not None:
            namespaceprefix_ = self.Art73_nsprefix_ + ':' if (UseCapturedNS_ and self.Art73_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sArt73>%s</%sArt73>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Art73), input_name='Art73')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TipoDocumento':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TipoDocumento')
            value_ = self.gds_validate_string(value_, node, 'TipoDocumento')
            self.TipoDocumento = value_
            self.TipoDocumento_nsprefix_ = child_.prefix
            # validate type TipoDocumentoType
            self.validate_TipoDocumentoType(self.TipoDocumento)
        elif nodeName_ == 'Divisa':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Divisa')
            value_ = self.gds_validate_string(value_, node, 'Divisa')
            self.Divisa = value_
            self.Divisa_nsprefix_ = child_.prefix
            # validate type DivisaType
            self.validate_DivisaType(self.Divisa)
        elif nodeName_ == 'Data':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Data = dval_
            self.Data_nsprefix_ = child_.prefix
            # validate type DataFatturaType
            self.validate_DataFatturaType(self.Data)
        elif nodeName_ == 'Numero':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Numero')
            value_ = self.gds_validate_string(value_, node, 'Numero')
            self.Numero = value_
            self.Numero_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.Numero)
        elif nodeName_ == 'DatiRitenuta':
            obj_ = DatiRitenutaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiRitenuta = obj_
            obj_.original_tagname_ = 'DatiRitenuta'
        elif nodeName_ == 'DatiBollo':
            obj_ = DatiBolloType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiBollo = obj_
            obj_.original_tagname_ = 'DatiBollo'
        elif nodeName_ == 'DatiCassaPrevidenziale':
            obj_ = DatiCassaPrevidenzialeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiCassaPrevidenziale.append(obj_)
            obj_.original_tagname_ = 'DatiCassaPrevidenziale'
        elif nodeName_ == 'ScontoMaggiorazione':
            obj_ = ScontoMaggiorazioneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ScontoMaggiorazione.append(obj_)
            obj_.original_tagname_ = 'ScontoMaggiorazione'
        elif nodeName_ == 'ImportoTotaleDocumento' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ImportoTotaleDocumento')
            fval_ = self.gds_validate_decimal(fval_, node, 'ImportoTotaleDocumento')
            self.ImportoTotaleDocumento = fval_
            self.ImportoTotaleDocumento_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ImportoTotaleDocumento)
        elif nodeName_ == 'Arrotondamento' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Arrotondamento')
            fval_ = self.gds_validate_decimal(fval_, node, 'Arrotondamento')
            self.Arrotondamento = fval_
            self.Arrotondamento_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.Arrotondamento)
        elif nodeName_ == 'Causale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Causale')
            value_ = self.gds_validate_string(value_, node, 'Causale')
            self.Causale.append(value_)
            self.Causale_nsprefix_ = child_.prefix
            # validate type String200LatinType
            self.validate_String200LatinType(self.Causale[-1])
        elif nodeName_ == 'Art73':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Art73')
            value_ = self.gds_validate_string(value_, node, 'Art73')
            self.Art73 = value_
            self.Art73_nsprefix_ = child_.prefix
            # validate type Art73Type
            self.validate_Art73Type(self.Art73)
# end class DatiGeneraliDocumentoType


class DatiRitenutaType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TipoRitenuta=None, ImportoRitenuta=None, AliquotaRitenuta=None, CausalePagamento=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TipoRitenuta = TipoRitenuta
        self.validate_TipoRitenutaType(self.TipoRitenuta)
        self.TipoRitenuta_nsprefix_ = None
        self.ImportoRitenuta = ImportoRitenuta
        self.validate_Amount2DecimalType(self.ImportoRitenuta)
        self.ImportoRitenuta_nsprefix_ = None
        self.AliquotaRitenuta = AliquotaRitenuta
        self.validate_RateType(self.AliquotaRitenuta)
        self.AliquotaRitenuta_nsprefix_ = None
        self.CausalePagamento = CausalePagamento
        self.validate_CausalePagamentoType(self.CausalePagamento)
        self.CausalePagamento_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiRitenutaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiRitenutaType.subclass:
            return DatiRitenutaType.subclass(*args_, **kwargs_)
        else:
            return DatiRitenutaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TipoRitenuta(self):
        return self.TipoRitenuta
    def set_TipoRitenuta(self, TipoRitenuta):
        self.TipoRitenuta = TipoRitenuta
    def get_ImportoRitenuta(self):
        return self.ImportoRitenuta
    def set_ImportoRitenuta(self, ImportoRitenuta):
        self.ImportoRitenuta = ImportoRitenuta
    def get_AliquotaRitenuta(self):
        return self.AliquotaRitenuta
    def set_AliquotaRitenuta(self, AliquotaRitenuta):
        self.AliquotaRitenuta = AliquotaRitenuta
    def get_CausalePagamento(self):
        return self.CausalePagamento
    def set_CausalePagamento(self, CausalePagamento):
        self.CausalePagamento = CausalePagamento
    def validate_TipoRitenutaType(self, value):
        result = True
        # Validate type TipoRitenutaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['RT01', 'RT02']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TipoRitenutaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on TipoRitenutaType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def validate_RateType(self, value):
        result = True
        # Validate type RateType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 100.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RateType' % {"value": value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_RateType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RateType_patterns_, ))
                result = False
        return result
    validate_RateType_patterns_ = [['^([0-9]{1,3}\\.[0-9]{2})$']]
    def validate_CausalePagamentoType(self, value):
        result = True
        # Validate type CausalePagamentoType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'L1', 'M1', 'O1', 'V1']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CausalePagamentoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.TipoRitenuta is not None or
            self.ImportoRitenuta is not None or
            self.AliquotaRitenuta is not None or
            self.CausalePagamento is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiRitenutaType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiRitenutaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiRitenutaType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiRitenutaType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiRitenutaType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiRitenutaType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiRitenutaType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TipoRitenuta is not None:
            namespaceprefix_ = self.TipoRitenuta_nsprefix_ + ':' if (UseCapturedNS_ and self.TipoRitenuta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTipoRitenuta>%s</%sTipoRitenuta>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TipoRitenuta), input_name='TipoRitenuta')), namespaceprefix_ , eol_))
        if self.ImportoRitenuta is not None:
            namespaceprefix_ = self.ImportoRitenuta_nsprefix_ + ':' if (UseCapturedNS_ and self.ImportoRitenuta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImportoRitenuta>%s</%sImportoRitenuta>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ImportoRitenuta, input_name='ImportoRitenuta'), namespaceprefix_ , eol_))
        if self.AliquotaRitenuta is not None:
            namespaceprefix_ = self.AliquotaRitenuta_nsprefix_ + ':' if (UseCapturedNS_ and self.AliquotaRitenuta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAliquotaRitenuta>%s</%sAliquotaRitenuta>%s' % (namespaceprefix_ , self.gds_format_decimal(self.AliquotaRitenuta, input_name='AliquotaRitenuta'), namespaceprefix_ , eol_))
        if self.CausalePagamento is not None:
            namespaceprefix_ = self.CausalePagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.CausalePagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCausalePagamento>%s</%sCausalePagamento>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CausalePagamento), input_name='CausalePagamento')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TipoRitenuta':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TipoRitenuta')
            value_ = self.gds_validate_string(value_, node, 'TipoRitenuta')
            self.TipoRitenuta = value_
            self.TipoRitenuta_nsprefix_ = child_.prefix
            # validate type TipoRitenutaType
            self.validate_TipoRitenutaType(self.TipoRitenuta)
        elif nodeName_ == 'ImportoRitenuta' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ImportoRitenuta')
            fval_ = self.gds_validate_decimal(fval_, node, 'ImportoRitenuta')
            self.ImportoRitenuta = fval_
            self.ImportoRitenuta_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ImportoRitenuta)
        elif nodeName_ == 'AliquotaRitenuta' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'AliquotaRitenuta')
            fval_ = self.gds_validate_decimal(fval_, node, 'AliquotaRitenuta')
            self.AliquotaRitenuta = fval_
            self.AliquotaRitenuta_nsprefix_ = child_.prefix
            # validate type RateType
            self.validate_RateType(self.AliquotaRitenuta)
        elif nodeName_ == 'CausalePagamento':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CausalePagamento')
            value_ = self.gds_validate_string(value_, node, 'CausalePagamento')
            self.CausalePagamento = value_
            self.CausalePagamento_nsprefix_ = child_.prefix
            # validate type CausalePagamentoType
            self.validate_CausalePagamentoType(self.CausalePagamento)
# end class DatiRitenutaType


class DatiBolloType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, BolloVirtuale=None, ImportoBollo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.BolloVirtuale = BolloVirtuale
        self.validate_BolloVirtualeType(self.BolloVirtuale)
        self.BolloVirtuale_nsprefix_ = None
        self.ImportoBollo = ImportoBollo
        self.validate_Amount2DecimalType(self.ImportoBollo)
        self.ImportoBollo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiBolloType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiBolloType.subclass:
            return DatiBolloType.subclass(*args_, **kwargs_)
        else:
            return DatiBolloType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_BolloVirtuale(self):
        return self.BolloVirtuale
    def set_BolloVirtuale(self, BolloVirtuale):
        self.BolloVirtuale = BolloVirtuale
    def get_ImportoBollo(self):
        return self.ImportoBollo
    def set_ImportoBollo(self, ImportoBollo):
        self.ImportoBollo = ImportoBollo
    def validate_BolloVirtualeType(self, value):
        result = True
        # Validate type BolloVirtualeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SI']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on BolloVirtualeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def _hasContent(self):
        if (
            self.BolloVirtuale is not None or
            self.ImportoBollo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiBolloType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiBolloType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiBolloType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiBolloType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiBolloType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiBolloType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiBolloType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.BolloVirtuale is not None:
            namespaceprefix_ = self.BolloVirtuale_nsprefix_ + ':' if (UseCapturedNS_ and self.BolloVirtuale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBolloVirtuale>%s</%sBolloVirtuale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BolloVirtuale), input_name='BolloVirtuale')), namespaceprefix_ , eol_))
        if self.ImportoBollo is not None:
            namespaceprefix_ = self.ImportoBollo_nsprefix_ + ':' if (UseCapturedNS_ and self.ImportoBollo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImportoBollo>%s</%sImportoBollo>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ImportoBollo, input_name='ImportoBollo'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'BolloVirtuale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BolloVirtuale')
            value_ = self.gds_validate_string(value_, node, 'BolloVirtuale')
            self.BolloVirtuale = value_
            self.BolloVirtuale_nsprefix_ = child_.prefix
            # validate type BolloVirtualeType
            self.validate_BolloVirtualeType(self.BolloVirtuale)
        elif nodeName_ == 'ImportoBollo' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ImportoBollo')
            fval_ = self.gds_validate_decimal(fval_, node, 'ImportoBollo')
            self.ImportoBollo = fval_
            self.ImportoBollo_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ImportoBollo)
# end class DatiBolloType


class DatiCassaPrevidenzialeType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TipoCassa=None, AlCassa=None, ImportoContributoCassa=None, ImponibileCassa=None, AliquotaIVA=None, Ritenuta=None, Natura=None, RiferimentoAmministrazione=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TipoCassa = TipoCassa
        self.validate_TipoCassaType(self.TipoCassa)
        self.TipoCassa_nsprefix_ = None
        self.AlCassa = AlCassa
        self.validate_RateType(self.AlCassa)
        self.AlCassa_nsprefix_ = None
        self.ImportoContributoCassa = ImportoContributoCassa
        self.validate_Amount2DecimalType(self.ImportoContributoCassa)
        self.ImportoContributoCassa_nsprefix_ = None
        self.ImponibileCassa = ImponibileCassa
        self.validate_Amount2DecimalType(self.ImponibileCassa)
        self.ImponibileCassa_nsprefix_ = None
        self.AliquotaIVA = AliquotaIVA
        self.validate_RateType(self.AliquotaIVA)
        self.AliquotaIVA_nsprefix_ = None
        self.Ritenuta = Ritenuta
        self.validate_RitenutaType(self.Ritenuta)
        self.Ritenuta_nsprefix_ = None
        self.Natura = Natura
        self.validate_NaturaType(self.Natura)
        self.Natura_nsprefix_ = None
        self.RiferimentoAmministrazione = RiferimentoAmministrazione
        self.validate_String20Type(self.RiferimentoAmministrazione)
        self.RiferimentoAmministrazione_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiCassaPrevidenzialeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiCassaPrevidenzialeType.subclass:
            return DatiCassaPrevidenzialeType.subclass(*args_, **kwargs_)
        else:
            return DatiCassaPrevidenzialeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TipoCassa(self):
        return self.TipoCassa
    def set_TipoCassa(self, TipoCassa):
        self.TipoCassa = TipoCassa
    def get_AlCassa(self):
        return self.AlCassa
    def set_AlCassa(self, AlCassa):
        self.AlCassa = AlCassa
    def get_ImportoContributoCassa(self):
        return self.ImportoContributoCassa
    def set_ImportoContributoCassa(self, ImportoContributoCassa):
        self.ImportoContributoCassa = ImportoContributoCassa
    def get_ImponibileCassa(self):
        return self.ImponibileCassa
    def set_ImponibileCassa(self, ImponibileCassa):
        self.ImponibileCassa = ImponibileCassa
    def get_AliquotaIVA(self):
        return self.AliquotaIVA
    def set_AliquotaIVA(self, AliquotaIVA):
        self.AliquotaIVA = AliquotaIVA
    def get_Ritenuta(self):
        return self.Ritenuta
    def set_Ritenuta(self, Ritenuta):
        self.Ritenuta = Ritenuta
    def get_Natura(self):
        return self.Natura
    def set_Natura(self, Natura):
        self.Natura = Natura
    def get_RiferimentoAmministrazione(self):
        return self.RiferimentoAmministrazione
    def set_RiferimentoAmministrazione(self, RiferimentoAmministrazione):
        self.RiferimentoAmministrazione = RiferimentoAmministrazione
    def validate_TipoCassaType(self, value):
        result = True
        # Validate type TipoCassaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['TC01', 'TC02', 'TC03', 'TC04', 'TC05', 'TC06', 'TC07', 'TC08', 'TC09', 'TC10', 'TC11', 'TC12', 'TC13', 'TC14', 'TC15', 'TC16', 'TC17', 'TC18', 'TC19', 'TC20', 'TC21', 'TC22']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TipoCassaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on TipoCassaType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_RateType(self, value):
        result = True
        # Validate type RateType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 100.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RateType' % {"value": value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_RateType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RateType_patterns_, ))
                result = False
        return result
    validate_RateType_patterns_ = [['^([0-9]{1,3}\\.[0-9]{2})$']]
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def validate_RitenutaType(self, value):
        result = True
        # Validate type RitenutaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SI']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on RitenutaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on RitenutaType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_NaturaType(self, value):
        result = True
        # Validate type NaturaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NaturaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def _hasContent(self):
        if (
            self.TipoCassa is not None or
            self.AlCassa is not None or
            self.ImportoContributoCassa is not None or
            self.ImponibileCassa is not None or
            self.AliquotaIVA is not None or
            self.Ritenuta is not None or
            self.Natura is not None or
            self.RiferimentoAmministrazione is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiCassaPrevidenzialeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiCassaPrevidenzialeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiCassaPrevidenzialeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiCassaPrevidenzialeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiCassaPrevidenzialeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiCassaPrevidenzialeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiCassaPrevidenzialeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TipoCassa is not None:
            namespaceprefix_ = self.TipoCassa_nsprefix_ + ':' if (UseCapturedNS_ and self.TipoCassa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTipoCassa>%s</%sTipoCassa>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TipoCassa), input_name='TipoCassa')), namespaceprefix_ , eol_))
        if self.AlCassa is not None:
            namespaceprefix_ = self.AlCassa_nsprefix_ + ':' if (UseCapturedNS_ and self.AlCassa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAlCassa>%s</%sAlCassa>%s' % (namespaceprefix_ , self.gds_format_decimal(self.AlCassa, input_name='AlCassa'), namespaceprefix_ , eol_))
        if self.ImportoContributoCassa is not None:
            namespaceprefix_ = self.ImportoContributoCassa_nsprefix_ + ':' if (UseCapturedNS_ and self.ImportoContributoCassa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImportoContributoCassa>%s</%sImportoContributoCassa>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ImportoContributoCassa, input_name='ImportoContributoCassa'), namespaceprefix_ , eol_))
        if self.ImponibileCassa is not None:
            namespaceprefix_ = self.ImponibileCassa_nsprefix_ + ':' if (UseCapturedNS_ and self.ImponibileCassa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImponibileCassa>%s</%sImponibileCassa>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ImponibileCassa, input_name='ImponibileCassa'), namespaceprefix_ , eol_))
        if self.AliquotaIVA is not None:
            namespaceprefix_ = self.AliquotaIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.AliquotaIVA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAliquotaIVA>%s</%sAliquotaIVA>%s' % (namespaceprefix_ , self.gds_format_decimal(self.AliquotaIVA, input_name='AliquotaIVA'), namespaceprefix_ , eol_))
        if self.Ritenuta is not None:
            namespaceprefix_ = self.Ritenuta_nsprefix_ + ':' if (UseCapturedNS_ and self.Ritenuta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRitenuta>%s</%sRitenuta>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Ritenuta), input_name='Ritenuta')), namespaceprefix_ , eol_))
        if self.Natura is not None:
            namespaceprefix_ = self.Natura_nsprefix_ + ':' if (UseCapturedNS_ and self.Natura_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNatura>%s</%sNatura>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Natura), input_name='Natura')), namespaceprefix_ , eol_))
        if self.RiferimentoAmministrazione is not None:
            namespaceprefix_ = self.RiferimentoAmministrazione_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoAmministrazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoAmministrazione>%s</%sRiferimentoAmministrazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RiferimentoAmministrazione), input_name='RiferimentoAmministrazione')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TipoCassa':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TipoCassa')
            value_ = self.gds_validate_string(value_, node, 'TipoCassa')
            self.TipoCassa = value_
            self.TipoCassa_nsprefix_ = child_.prefix
            # validate type TipoCassaType
            self.validate_TipoCassaType(self.TipoCassa)
        elif nodeName_ == 'AlCassa' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'AlCassa')
            fval_ = self.gds_validate_decimal(fval_, node, 'AlCassa')
            self.AlCassa = fval_
            self.AlCassa_nsprefix_ = child_.prefix
            # validate type RateType
            self.validate_RateType(self.AlCassa)
        elif nodeName_ == 'ImportoContributoCassa' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ImportoContributoCassa')
            fval_ = self.gds_validate_decimal(fval_, node, 'ImportoContributoCassa')
            self.ImportoContributoCassa = fval_
            self.ImportoContributoCassa_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ImportoContributoCassa)
        elif nodeName_ == 'ImponibileCassa' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ImponibileCassa')
            fval_ = self.gds_validate_decimal(fval_, node, 'ImponibileCassa')
            self.ImponibileCassa = fval_
            self.ImponibileCassa_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ImponibileCassa)
        elif nodeName_ == 'AliquotaIVA' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'AliquotaIVA')
            fval_ = self.gds_validate_decimal(fval_, node, 'AliquotaIVA')
            self.AliquotaIVA = fval_
            self.AliquotaIVA_nsprefix_ = child_.prefix
            # validate type RateType
            self.validate_RateType(self.AliquotaIVA)
        elif nodeName_ == 'Ritenuta':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Ritenuta')
            value_ = self.gds_validate_string(value_, node, 'Ritenuta')
            self.Ritenuta = value_
            self.Ritenuta_nsprefix_ = child_.prefix
            # validate type RitenutaType
            self.validate_RitenutaType(self.Ritenuta)
        elif nodeName_ == 'Natura':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Natura')
            value_ = self.gds_validate_string(value_, node, 'Natura')
            self.Natura = value_
            self.Natura_nsprefix_ = child_.prefix
            # validate type NaturaType
            self.validate_NaturaType(self.Natura)
        elif nodeName_ == 'RiferimentoAmministrazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RiferimentoAmministrazione')
            value_ = self.gds_validate_string(value_, node, 'RiferimentoAmministrazione')
            self.RiferimentoAmministrazione = value_
            self.RiferimentoAmministrazione_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.RiferimentoAmministrazione)
# end class DatiCassaPrevidenzialeType


class ScontoMaggiorazioneType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Tipo=None, Percentuale=None, Importo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Tipo = Tipo
        self.validate_TipoScontoMaggiorazioneType(self.Tipo)
        self.Tipo_nsprefix_ = None
        self.Percentuale = Percentuale
        self.validate_RateType(self.Percentuale)
        self.Percentuale_nsprefix_ = None
        self.Importo = Importo
        self.validate_Amount2DecimalType(self.Importo)
        self.Importo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ScontoMaggiorazioneType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ScontoMaggiorazioneType.subclass:
            return ScontoMaggiorazioneType.subclass(*args_, **kwargs_)
        else:
            return ScontoMaggiorazioneType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Tipo(self):
        return self.Tipo
    def set_Tipo(self, Tipo):
        self.Tipo = Tipo
    def get_Percentuale(self):
        return self.Percentuale
    def set_Percentuale(self, Percentuale):
        self.Percentuale = Percentuale
    def get_Importo(self):
        return self.Importo
    def set_Importo(self, Importo):
        self.Importo = Importo
    def validate_TipoScontoMaggiorazioneType(self, value):
        result = True
        # Validate type TipoScontoMaggiorazioneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SC', 'MG']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TipoScontoMaggiorazioneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on TipoScontoMaggiorazioneType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_RateType(self, value):
        result = True
        # Validate type RateType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 100.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RateType' % {"value": value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_RateType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RateType_patterns_, ))
                result = False
        return result
    validate_RateType_patterns_ = [['^([0-9]{1,3}\\.[0-9]{2})$']]
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def _hasContent(self):
        if (
            self.Tipo is not None or
            self.Percentuale is not None or
            self.Importo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ScontoMaggiorazioneType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ScontoMaggiorazioneType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ScontoMaggiorazioneType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ScontoMaggiorazioneType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ScontoMaggiorazioneType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ScontoMaggiorazioneType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ScontoMaggiorazioneType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Tipo is not None:
            namespaceprefix_ = self.Tipo_nsprefix_ + ':' if (UseCapturedNS_ and self.Tipo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTipo>%s</%sTipo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Tipo), input_name='Tipo')), namespaceprefix_ , eol_))
        if self.Percentuale is not None:
            namespaceprefix_ = self.Percentuale_nsprefix_ + ':' if (UseCapturedNS_ and self.Percentuale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPercentuale>%s</%sPercentuale>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Percentuale, input_name='Percentuale'), namespaceprefix_ , eol_))
        if self.Importo is not None:
            namespaceprefix_ = self.Importo_nsprefix_ + ':' if (UseCapturedNS_ and self.Importo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImporto>%s</%sImporto>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Importo, input_name='Importo'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Tipo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Tipo')
            value_ = self.gds_validate_string(value_, node, 'Tipo')
            self.Tipo = value_
            self.Tipo_nsprefix_ = child_.prefix
            # validate type TipoScontoMaggiorazioneType
            self.validate_TipoScontoMaggiorazioneType(self.Tipo)
        elif nodeName_ == 'Percentuale' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Percentuale')
            fval_ = self.gds_validate_decimal(fval_, node, 'Percentuale')
            self.Percentuale = fval_
            self.Percentuale_nsprefix_ = child_.prefix
            # validate type RateType
            self.validate_RateType(self.Percentuale)
        elif nodeName_ == 'Importo' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Importo')
            fval_ = self.gds_validate_decimal(fval_, node, 'Importo')
            self.Importo = fval_
            self.Importo_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.Importo)
# end class ScontoMaggiorazioneType


class DatiSALType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RiferimentoFase=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.RiferimentoFase = RiferimentoFase
        self.validate_RiferimentoFaseType(self.RiferimentoFase)
        self.RiferimentoFase_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiSALType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiSALType.subclass:
            return DatiSALType.subclass(*args_, **kwargs_)
        else:
            return DatiSALType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RiferimentoFase(self):
        return self.RiferimentoFase
    def set_RiferimentoFase(self, RiferimentoFase):
        self.RiferimentoFase = RiferimentoFase
    def validate_RiferimentoFaseType(self, value):
        result = True
        # Validate type RiferimentoFaseType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on RiferimentoFaseType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RiferimentoFaseType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.RiferimentoFase is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiSALType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiSALType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiSALType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiSALType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiSALType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiSALType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiSALType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.RiferimentoFase is not None:
            namespaceprefix_ = self.RiferimentoFase_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoFase_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoFase>%s</%sRiferimentoFase>%s' % (namespaceprefix_ , self.gds_format_integer(self.RiferimentoFase, input_name='RiferimentoFase'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'RiferimentoFase' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'RiferimentoFase')
            ival_ = self.gds_validate_integer(ival_, node, 'RiferimentoFase')
            self.RiferimentoFase = ival_
            self.RiferimentoFase_nsprefix_ = child_.prefix
            # validate type RiferimentoFaseType
            self.validate_RiferimentoFaseType(self.RiferimentoFase)
# end class DatiSALType


class DatiDocumentiCorrelatiType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RiferimentoNumeroLinea=None, IdDocumento=None, Data=None, NumItem=None, CodiceCommessaConvenzione=None, CodiceCUP=None, CodiceCIG=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if RiferimentoNumeroLinea is None:
            self.RiferimentoNumeroLinea = []
        else:
            self.RiferimentoNumeroLinea = RiferimentoNumeroLinea
        self.RiferimentoNumeroLinea_nsprefix_ = None
        self.IdDocumento = IdDocumento
        self.validate_String20Type(self.IdDocumento)
        self.IdDocumento_nsprefix_ = None
        if isinstance(Data, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Data, '%Y-%m-%d').date()
        else:
            initvalue_ = Data
        self.Data = initvalue_
        self.Data_nsprefix_ = None
        self.NumItem = NumItem
        self.validate_String20Type(self.NumItem)
        self.NumItem_nsprefix_ = None
        self.CodiceCommessaConvenzione = CodiceCommessaConvenzione
        self.validate_String100LatinType(self.CodiceCommessaConvenzione)
        self.CodiceCommessaConvenzione_nsprefix_ = None
        self.CodiceCUP = CodiceCUP
        self.validate_String15Type(self.CodiceCUP)
        self.CodiceCUP_nsprefix_ = None
        self.CodiceCIG = CodiceCIG
        self.validate_String15Type(self.CodiceCIG)
        self.CodiceCIG_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiDocumentiCorrelatiType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiDocumentiCorrelatiType.subclass:
            return DatiDocumentiCorrelatiType.subclass(*args_, **kwargs_)
        else:
            return DatiDocumentiCorrelatiType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RiferimentoNumeroLinea(self):
        return self.RiferimentoNumeroLinea
    def set_RiferimentoNumeroLinea(self, RiferimentoNumeroLinea):
        self.RiferimentoNumeroLinea = RiferimentoNumeroLinea
    def add_RiferimentoNumeroLinea(self, value):
        self.RiferimentoNumeroLinea.append(value)
    def insert_RiferimentoNumeroLinea_at(self, index, value):
        self.RiferimentoNumeroLinea.insert(index, value)
    def replace_RiferimentoNumeroLinea_at(self, index, value):
        self.RiferimentoNumeroLinea[index] = value
    def get_IdDocumento(self):
        return self.IdDocumento
    def set_IdDocumento(self, IdDocumento):
        self.IdDocumento = IdDocumento
    def get_Data(self):
        return self.Data
    def set_Data(self, Data):
        self.Data = Data
    def get_NumItem(self):
        return self.NumItem
    def set_NumItem(self, NumItem):
        self.NumItem = NumItem
    def get_CodiceCommessaConvenzione(self):
        return self.CodiceCommessaConvenzione
    def set_CodiceCommessaConvenzione(self, CodiceCommessaConvenzione):
        self.CodiceCommessaConvenzione = CodiceCommessaConvenzione
    def get_CodiceCUP(self):
        return self.CodiceCUP
    def set_CodiceCUP(self, CodiceCUP):
        self.CodiceCUP = CodiceCUP
    def get_CodiceCIG(self):
        return self.CodiceCIG
    def set_CodiceCIG(self, CodiceCIG):
        self.CodiceCIG = CodiceCIG
    def validate_RiferimentoNumeroLineaType(self, value):
        result = True
        # Validate type RiferimentoNumeroLineaType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on RiferimentoNumeroLineaType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RiferimentoNumeroLineaType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def validate_String100LatinType(self, value):
        result = True
        # Validate type String100LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String100LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String100LatinType_patterns_, ))
                result = False
        return result
    validate_String100LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,100})$']]
    def validate_String15Type(self, value):
        result = True
        # Validate type String15Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String15Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String15Type_patterns_, ))
                result = False
        return result
    validate_String15Type_patterns_ = [['^(([\x00-\x7f]{1,15}))$']]
    def _hasContent(self):
        if (
            self.RiferimentoNumeroLinea or
            self.IdDocumento is not None or
            self.Data is not None or
            self.NumItem is not None or
            self.CodiceCommessaConvenzione is not None or
            self.CodiceCUP is not None or
            self.CodiceCIG is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiDocumentiCorrelatiType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiDocumentiCorrelatiType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiDocumentiCorrelatiType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiDocumentiCorrelatiType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiDocumentiCorrelatiType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiDocumentiCorrelatiType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiDocumentiCorrelatiType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for RiferimentoNumeroLinea_ in self.RiferimentoNumeroLinea:
            namespaceprefix_ = self.RiferimentoNumeroLinea_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoNumeroLinea_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoNumeroLinea>%s</%sRiferimentoNumeroLinea>%s' % (namespaceprefix_ , self.gds_format_integer(RiferimentoNumeroLinea_, input_name='RiferimentoNumeroLinea'), namespaceprefix_ , eol_))
        if self.IdDocumento is not None:
            namespaceprefix_ = self.IdDocumento_nsprefix_ + ':' if (UseCapturedNS_ and self.IdDocumento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdDocumento>%s</%sIdDocumento>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdDocumento), input_name='IdDocumento')), namespaceprefix_ , eol_))
        if self.Data is not None:
            namespaceprefix_ = self.Data_nsprefix_ + ':' if (UseCapturedNS_ and self.Data_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sData>%s</%sData>%s' % (namespaceprefix_ , self.gds_format_date(self.Data, input_name='Data'), namespaceprefix_ , eol_))
        if self.NumItem is not None:
            namespaceprefix_ = self.NumItem_nsprefix_ + ':' if (UseCapturedNS_ and self.NumItem_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumItem>%s</%sNumItem>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumItem), input_name='NumItem')), namespaceprefix_ , eol_))
        if self.CodiceCommessaConvenzione is not None:
            namespaceprefix_ = self.CodiceCommessaConvenzione_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceCommessaConvenzione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceCommessaConvenzione>%s</%sCodiceCommessaConvenzione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceCommessaConvenzione), input_name='CodiceCommessaConvenzione')), namespaceprefix_ , eol_))
        if self.CodiceCUP is not None:
            namespaceprefix_ = self.CodiceCUP_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceCUP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceCUP>%s</%sCodiceCUP>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceCUP), input_name='CodiceCUP')), namespaceprefix_ , eol_))
        if self.CodiceCIG is not None:
            namespaceprefix_ = self.CodiceCIG_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceCIG_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceCIG>%s</%sCodiceCIG>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceCIG), input_name='CodiceCIG')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'RiferimentoNumeroLinea' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'RiferimentoNumeroLinea')
            ival_ = self.gds_validate_integer(ival_, node, 'RiferimentoNumeroLinea')
            self.RiferimentoNumeroLinea.append(ival_)
            self.RiferimentoNumeroLinea_nsprefix_ = child_.prefix
            # validate type RiferimentoNumeroLineaType
            self.validate_RiferimentoNumeroLineaType(self.RiferimentoNumeroLinea[-1])
        elif nodeName_ == 'IdDocumento':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdDocumento')
            value_ = self.gds_validate_string(value_, node, 'IdDocumento')
            self.IdDocumento = value_
            self.IdDocumento_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.IdDocumento)
        elif nodeName_ == 'Data':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Data = dval_
            self.Data_nsprefix_ = child_.prefix
        elif nodeName_ == 'NumItem':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumItem')
            value_ = self.gds_validate_string(value_, node, 'NumItem')
            self.NumItem = value_
            self.NumItem_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.NumItem)
        elif nodeName_ == 'CodiceCommessaConvenzione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceCommessaConvenzione')
            value_ = self.gds_validate_string(value_, node, 'CodiceCommessaConvenzione')
            self.CodiceCommessaConvenzione = value_
            self.CodiceCommessaConvenzione_nsprefix_ = child_.prefix
            # validate type String100LatinType
            self.validate_String100LatinType(self.CodiceCommessaConvenzione)
        elif nodeName_ == 'CodiceCUP':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceCUP')
            value_ = self.gds_validate_string(value_, node, 'CodiceCUP')
            self.CodiceCUP = value_
            self.CodiceCUP_nsprefix_ = child_.prefix
            # validate type String15Type
            self.validate_String15Type(self.CodiceCUP)
        elif nodeName_ == 'CodiceCIG':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceCIG')
            value_ = self.gds_validate_string(value_, node, 'CodiceCIG')
            self.CodiceCIG = value_
            self.CodiceCIG_nsprefix_ = child_.prefix
            # validate type String15Type
            self.validate_String15Type(self.CodiceCIG)
# end class DatiDocumentiCorrelatiType


class DatiDDTType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NumeroDDT=None, DataDDT=None, RiferimentoNumeroLinea=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NumeroDDT = NumeroDDT
        self.validate_String20Type(self.NumeroDDT)
        self.NumeroDDT_nsprefix_ = None
        if isinstance(DataDDT, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataDDT, '%Y-%m-%d').date()
        else:
            initvalue_ = DataDDT
        self.DataDDT = initvalue_
        self.DataDDT_nsprefix_ = None
        if RiferimentoNumeroLinea is None:
            self.RiferimentoNumeroLinea = []
        else:
            self.RiferimentoNumeroLinea = RiferimentoNumeroLinea
        self.RiferimentoNumeroLinea_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiDDTType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiDDTType.subclass:
            return DatiDDTType.subclass(*args_, **kwargs_)
        else:
            return DatiDDTType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NumeroDDT(self):
        return self.NumeroDDT
    def set_NumeroDDT(self, NumeroDDT):
        self.NumeroDDT = NumeroDDT
    def get_DataDDT(self):
        return self.DataDDT
    def set_DataDDT(self, DataDDT):
        self.DataDDT = DataDDT
    def get_RiferimentoNumeroLinea(self):
        return self.RiferimentoNumeroLinea
    def set_RiferimentoNumeroLinea(self, RiferimentoNumeroLinea):
        self.RiferimentoNumeroLinea = RiferimentoNumeroLinea
    def add_RiferimentoNumeroLinea(self, value):
        self.RiferimentoNumeroLinea.append(value)
    def insert_RiferimentoNumeroLinea_at(self, index, value):
        self.RiferimentoNumeroLinea.insert(index, value)
    def replace_RiferimentoNumeroLinea_at(self, index, value):
        self.RiferimentoNumeroLinea[index] = value
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def validate_RiferimentoNumeroLineaType(self, value):
        result = True
        # Validate type RiferimentoNumeroLineaType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on RiferimentoNumeroLineaType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RiferimentoNumeroLineaType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.NumeroDDT is not None or
            self.DataDDT is not None or
            self.RiferimentoNumeroLinea
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiDDTType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiDDTType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiDDTType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiDDTType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiDDTType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiDDTType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiDDTType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NumeroDDT is not None:
            namespaceprefix_ = self.NumeroDDT_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroDDT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroDDT>%s</%sNumeroDDT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumeroDDT), input_name='NumeroDDT')), namespaceprefix_ , eol_))
        if self.DataDDT is not None:
            namespaceprefix_ = self.DataDDT_nsprefix_ + ':' if (UseCapturedNS_ and self.DataDDT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataDDT>%s</%sDataDDT>%s' % (namespaceprefix_ , self.gds_format_date(self.DataDDT, input_name='DataDDT'), namespaceprefix_ , eol_))
        for RiferimentoNumeroLinea_ in self.RiferimentoNumeroLinea:
            namespaceprefix_ = self.RiferimentoNumeroLinea_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoNumeroLinea_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoNumeroLinea>%s</%sRiferimentoNumeroLinea>%s' % (namespaceprefix_ , self.gds_format_integer(RiferimentoNumeroLinea_, input_name='RiferimentoNumeroLinea'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'NumeroDDT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumeroDDT')
            value_ = self.gds_validate_string(value_, node, 'NumeroDDT')
            self.NumeroDDT = value_
            self.NumeroDDT_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.NumeroDDT)
        elif nodeName_ == 'DataDDT':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataDDT = dval_
            self.DataDDT_nsprefix_ = child_.prefix
        elif nodeName_ == 'RiferimentoNumeroLinea' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'RiferimentoNumeroLinea')
            ival_ = self.gds_validate_integer(ival_, node, 'RiferimentoNumeroLinea')
            self.RiferimentoNumeroLinea.append(ival_)
            self.RiferimentoNumeroLinea_nsprefix_ = child_.prefix
            # validate type RiferimentoNumeroLineaType
            self.validate_RiferimentoNumeroLineaType(self.RiferimentoNumeroLinea[-1])
# end class DatiDDTType


class DatiTrasportoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DatiAnagraficiVettore=None, MezzoTrasporto=None, CausaleTrasporto=None, NumeroColli=None, Descrizione=None, UnitaMisuraPeso=None, PesoLordo=None, PesoNetto=None, DataOraRitiro=None, DataInizioTrasporto=None, TipoResa=None, IndirizzoResa=None, DataOraConsegna=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiAnagraficiVettore = DatiAnagraficiVettore
        self.DatiAnagraficiVettore_nsprefix_ = None
        self.MezzoTrasporto = MezzoTrasporto
        self.validate_String80LatinType(self.MezzoTrasporto)
        self.MezzoTrasporto_nsprefix_ = None
        self.CausaleTrasporto = CausaleTrasporto
        self.validate_String100LatinType(self.CausaleTrasporto)
        self.CausaleTrasporto_nsprefix_ = None
        self.NumeroColli = NumeroColli
        self.validate_NumeroColliType(self.NumeroColli)
        self.NumeroColli_nsprefix_ = None
        self.Descrizione = Descrizione
        self.validate_String100LatinType(self.Descrizione)
        self.Descrizione_nsprefix_ = None
        self.UnitaMisuraPeso = UnitaMisuraPeso
        self.validate_String10Type(self.UnitaMisuraPeso)
        self.UnitaMisuraPeso_nsprefix_ = None
        self.PesoLordo = PesoLordo
        self.validate_PesoType(self.PesoLordo)
        self.PesoLordo_nsprefix_ = None
        self.PesoNetto = PesoNetto
        self.validate_PesoType(self.PesoNetto)
        self.PesoNetto_nsprefix_ = None
        if isinstance(DataOraRitiro, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataOraRitiro, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = DataOraRitiro
        self.DataOraRitiro = initvalue_
        self.DataOraRitiro_nsprefix_ = None
        if isinstance(DataInizioTrasporto, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataInizioTrasporto, '%Y-%m-%d').date()
        else:
            initvalue_ = DataInizioTrasporto
        self.DataInizioTrasporto = initvalue_
        self.DataInizioTrasporto_nsprefix_ = None
        self.TipoResa = TipoResa
        self.validate_TipoResaType(self.TipoResa)
        self.TipoResa_nsprefix_ = None
        self.IndirizzoResa = IndirizzoResa
        self.IndirizzoResa_nsprefix_ = None
        if isinstance(DataOraConsegna, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataOraConsegna, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = DataOraConsegna
        self.DataOraConsegna = initvalue_
        self.DataOraConsegna_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiTrasportoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiTrasportoType.subclass:
            return DatiTrasportoType.subclass(*args_, **kwargs_)
        else:
            return DatiTrasportoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiAnagraficiVettore(self):
        return self.DatiAnagraficiVettore
    def set_DatiAnagraficiVettore(self, DatiAnagraficiVettore):
        self.DatiAnagraficiVettore = DatiAnagraficiVettore
    def get_MezzoTrasporto(self):
        return self.MezzoTrasporto
    def set_MezzoTrasporto(self, MezzoTrasporto):
        self.MezzoTrasporto = MezzoTrasporto
    def get_CausaleTrasporto(self):
        return self.CausaleTrasporto
    def set_CausaleTrasporto(self, CausaleTrasporto):
        self.CausaleTrasporto = CausaleTrasporto
    def get_NumeroColli(self):
        return self.NumeroColli
    def set_NumeroColli(self, NumeroColli):
        self.NumeroColli = NumeroColli
    def get_Descrizione(self):
        return self.Descrizione
    def set_Descrizione(self, Descrizione):
        self.Descrizione = Descrizione
    def get_UnitaMisuraPeso(self):
        return self.UnitaMisuraPeso
    def set_UnitaMisuraPeso(self, UnitaMisuraPeso):
        self.UnitaMisuraPeso = UnitaMisuraPeso
    def get_PesoLordo(self):
        return self.PesoLordo
    def set_PesoLordo(self, PesoLordo):
        self.PesoLordo = PesoLordo
    def get_PesoNetto(self):
        return self.PesoNetto
    def set_PesoNetto(self, PesoNetto):
        self.PesoNetto = PesoNetto
    def get_DataOraRitiro(self):
        return self.DataOraRitiro
    def set_DataOraRitiro(self, DataOraRitiro):
        self.DataOraRitiro = DataOraRitiro
    def get_DataInizioTrasporto(self):
        return self.DataInizioTrasporto
    def set_DataInizioTrasporto(self, DataInizioTrasporto):
        self.DataInizioTrasporto = DataInizioTrasporto
    def get_TipoResa(self):
        return self.TipoResa
    def set_TipoResa(self, TipoResa):
        self.TipoResa = TipoResa
    def get_IndirizzoResa(self):
        return self.IndirizzoResa
    def set_IndirizzoResa(self, IndirizzoResa):
        self.IndirizzoResa = IndirizzoResa
    def get_DataOraConsegna(self):
        return self.DataOraConsegna
    def set_DataOraConsegna(self, DataOraConsegna):
        self.DataOraConsegna = DataOraConsegna
    def validate_String80LatinType(self, value):
        result = True
        # Validate type String80LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String80LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String80LatinType_patterns_, ))
                result = False
        return result
    validate_String80LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,80})$']]
    def validate_String100LatinType(self, value):
        result = True
        # Validate type String100LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String100LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String100LatinType_patterns_, ))
                result = False
        return result
    validate_String100LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,100})$']]
    def validate_NumeroColliType(self, value):
        result = True
        # Validate type NumeroColliType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on NumeroColliType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on NumeroColliType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_String10Type(self, value):
        result = True
        # Validate type String10Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String10Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String10Type_patterns_, ))
                result = False
        return result
    validate_String10Type_patterns_ = [['^(([\x00-\x7f]{1,10}))$']]
    def validate_PesoType(self, value):
        result = True
        # Validate type PesoType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_PesoType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_PesoType_patterns_, ))
                result = False
        return result
    validate_PesoType_patterns_ = [['^([0-9]{1,4}\\.[0-9]{1,2})$']]
    def validate_TipoResaType(self, value):
        result = True
        # Validate type TipoResaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_TipoResaType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_TipoResaType_patterns_, ))
                result = False
        return result
    validate_TipoResaType_patterns_ = [['^([A-Z]{3})$']]
    def _hasContent(self):
        if (
            self.DatiAnagraficiVettore is not None or
            self.MezzoTrasporto is not None or
            self.CausaleTrasporto is not None or
            self.NumeroColli is not None or
            self.Descrizione is not None or
            self.UnitaMisuraPeso is not None or
            self.PesoLordo is not None or
            self.PesoNetto is not None or
            self.DataOraRitiro is not None or
            self.DataInizioTrasporto is not None or
            self.TipoResa is not None or
            self.IndirizzoResa is not None or
            self.DataOraConsegna is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiTrasportoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiTrasportoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiTrasportoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiTrasportoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiTrasportoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiTrasportoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiTrasportoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiAnagraficiVettore is not None:
            namespaceprefix_ = self.DatiAnagraficiVettore_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiAnagraficiVettore_nsprefix_) else ''
            self.DatiAnagraficiVettore.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiAnagraficiVettore', pretty_print=pretty_print)
        if self.MezzoTrasporto is not None:
            namespaceprefix_ = self.MezzoTrasporto_nsprefix_ + ':' if (UseCapturedNS_ and self.MezzoTrasporto_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMezzoTrasporto>%s</%sMezzoTrasporto>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MezzoTrasporto), input_name='MezzoTrasporto')), namespaceprefix_ , eol_))
        if self.CausaleTrasporto is not None:
            namespaceprefix_ = self.CausaleTrasporto_nsprefix_ + ':' if (UseCapturedNS_ and self.CausaleTrasporto_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCausaleTrasporto>%s</%sCausaleTrasporto>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CausaleTrasporto), input_name='CausaleTrasporto')), namespaceprefix_ , eol_))
        if self.NumeroColli is not None:
            namespaceprefix_ = self.NumeroColli_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroColli_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroColli>%s</%sNumeroColli>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumeroColli, input_name='NumeroColli'), namespaceprefix_ , eol_))
        if self.Descrizione is not None:
            namespaceprefix_ = self.Descrizione_nsprefix_ + ':' if (UseCapturedNS_ and self.Descrizione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescrizione>%s</%sDescrizione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Descrizione), input_name='Descrizione')), namespaceprefix_ , eol_))
        if self.UnitaMisuraPeso is not None:
            namespaceprefix_ = self.UnitaMisuraPeso_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitaMisuraPeso_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnitaMisuraPeso>%s</%sUnitaMisuraPeso>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UnitaMisuraPeso), input_name='UnitaMisuraPeso')), namespaceprefix_ , eol_))
        if self.PesoLordo is not None:
            namespaceprefix_ = self.PesoLordo_nsprefix_ + ':' if (UseCapturedNS_ and self.PesoLordo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPesoLordo>%s</%sPesoLordo>%s' % (namespaceprefix_ , self.gds_format_decimal(self.PesoLordo, input_name='PesoLordo'), namespaceprefix_ , eol_))
        if self.PesoNetto is not None:
            namespaceprefix_ = self.PesoNetto_nsprefix_ + ':' if (UseCapturedNS_ and self.PesoNetto_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPesoNetto>%s</%sPesoNetto>%s' % (namespaceprefix_ , self.gds_format_decimal(self.PesoNetto, input_name='PesoNetto'), namespaceprefix_ , eol_))
        if self.DataOraRitiro is not None:
            namespaceprefix_ = self.DataOraRitiro_nsprefix_ + ':' if (UseCapturedNS_ and self.DataOraRitiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataOraRitiro>%s</%sDataOraRitiro>%s' % (namespaceprefix_ , self.gds_format_datetime(self.DataOraRitiro, input_name='DataOraRitiro'), namespaceprefix_ , eol_))
        if self.DataInizioTrasporto is not None:
            namespaceprefix_ = self.DataInizioTrasporto_nsprefix_ + ':' if (UseCapturedNS_ and self.DataInizioTrasporto_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataInizioTrasporto>%s</%sDataInizioTrasporto>%s' % (namespaceprefix_ , self.gds_format_date(self.DataInizioTrasporto, input_name='DataInizioTrasporto'), namespaceprefix_ , eol_))
        if self.TipoResa is not None:
            namespaceprefix_ = self.TipoResa_nsprefix_ + ':' if (UseCapturedNS_ and self.TipoResa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTipoResa>%s</%sTipoResa>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TipoResa), input_name='TipoResa')), namespaceprefix_ , eol_))
        if self.IndirizzoResa is not None:
            namespaceprefix_ = self.IndirizzoResa_nsprefix_ + ':' if (UseCapturedNS_ and self.IndirizzoResa_nsprefix_) else ''
            self.IndirizzoResa.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IndirizzoResa', pretty_print=pretty_print)
        if self.DataOraConsegna is not None:
            namespaceprefix_ = self.DataOraConsegna_nsprefix_ + ':' if (UseCapturedNS_ and self.DataOraConsegna_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataOraConsegna>%s</%sDataOraConsegna>%s' % (namespaceprefix_ , self.gds_format_datetime(self.DataOraConsegna, input_name='DataOraConsegna'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiAnagraficiVettore':
            obj_ = DatiAnagraficiVettoreType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiAnagraficiVettore = obj_
            obj_.original_tagname_ = 'DatiAnagraficiVettore'
        elif nodeName_ == 'MezzoTrasporto':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MezzoTrasporto')
            value_ = self.gds_validate_string(value_, node, 'MezzoTrasporto')
            self.MezzoTrasporto = value_
            self.MezzoTrasporto_nsprefix_ = child_.prefix
            # validate type String80LatinType
            self.validate_String80LatinType(self.MezzoTrasporto)
        elif nodeName_ == 'CausaleTrasporto':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CausaleTrasporto')
            value_ = self.gds_validate_string(value_, node, 'CausaleTrasporto')
            self.CausaleTrasporto = value_
            self.CausaleTrasporto_nsprefix_ = child_.prefix
            # validate type String100LatinType
            self.validate_String100LatinType(self.CausaleTrasporto)
        elif nodeName_ == 'NumeroColli' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumeroColli')
            ival_ = self.gds_validate_integer(ival_, node, 'NumeroColli')
            self.NumeroColli = ival_
            self.NumeroColli_nsprefix_ = child_.prefix
            # validate type NumeroColliType
            self.validate_NumeroColliType(self.NumeroColli)
        elif nodeName_ == 'Descrizione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Descrizione')
            value_ = self.gds_validate_string(value_, node, 'Descrizione')
            self.Descrizione = value_
            self.Descrizione_nsprefix_ = child_.prefix
            # validate type String100LatinType
            self.validate_String100LatinType(self.Descrizione)
        elif nodeName_ == 'UnitaMisuraPeso':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UnitaMisuraPeso')
            value_ = self.gds_validate_string(value_, node, 'UnitaMisuraPeso')
            self.UnitaMisuraPeso = value_
            self.UnitaMisuraPeso_nsprefix_ = child_.prefix
            # validate type String10Type
            self.validate_String10Type(self.UnitaMisuraPeso)
        elif nodeName_ == 'PesoLordo' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'PesoLordo')
            fval_ = self.gds_validate_decimal(fval_, node, 'PesoLordo')
            self.PesoLordo = fval_
            self.PesoLordo_nsprefix_ = child_.prefix
            # validate type PesoType
            self.validate_PesoType(self.PesoLordo)
        elif nodeName_ == 'PesoNetto' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'PesoNetto')
            fval_ = self.gds_validate_decimal(fval_, node, 'PesoNetto')
            self.PesoNetto = fval_
            self.PesoNetto_nsprefix_ = child_.prefix
            # validate type PesoType
            self.validate_PesoType(self.PesoNetto)
        elif nodeName_ == 'DataOraRitiro':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.DataOraRitiro = dval_
            self.DataOraRitiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'DataInizioTrasporto':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataInizioTrasporto = dval_
            self.DataInizioTrasporto_nsprefix_ = child_.prefix
        elif nodeName_ == 'TipoResa':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TipoResa')
            value_ = self.gds_validate_string(value_, node, 'TipoResa')
            self.TipoResa = value_
            self.TipoResa_nsprefix_ = child_.prefix
            # validate type TipoResaType
            self.validate_TipoResaType(self.TipoResa)
        elif nodeName_ == 'IndirizzoResa':
            obj_ = IndirizzoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IndirizzoResa = obj_
            obj_.original_tagname_ = 'IndirizzoResa'
        elif nodeName_ == 'DataOraConsegna':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.DataOraConsegna = dval_
            self.DataOraConsegna_nsprefix_ = child_.prefix
# end class DatiTrasportoType


class IndirizzoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Indirizzo=None, NumeroCivico=None, CAP=None, Comune=None, Provincia=None, Nazione='IT', gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Indirizzo = Indirizzo
        self.validate_String60LatinType(self.Indirizzo)
        self.Indirizzo_nsprefix_ = None
        self.NumeroCivico = NumeroCivico
        self.validate_NumeroCivicoType(self.NumeroCivico)
        self.NumeroCivico_nsprefix_ = None
        self.CAP = CAP
        self.validate_CAPType(self.CAP)
        self.CAP_nsprefix_ = None
        self.Comune = Comune
        self.validate_String60LatinType(self.Comune)
        self.Comune_nsprefix_ = None
        self.Provincia = Provincia
        self.validate_ProvinciaType(self.Provincia)
        self.Provincia_nsprefix_ = None
        self.Nazione = Nazione
        self.validate_NazioneType(self.Nazione)
        self.Nazione_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IndirizzoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IndirizzoType.subclass:
            return IndirizzoType.subclass(*args_, **kwargs_)
        else:
            return IndirizzoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Indirizzo(self):
        return self.Indirizzo
    def set_Indirizzo(self, Indirizzo):
        self.Indirizzo = Indirizzo
    def get_NumeroCivico(self):
        return self.NumeroCivico
    def set_NumeroCivico(self, NumeroCivico):
        self.NumeroCivico = NumeroCivico
    def get_CAP(self):
        return self.CAP
    def set_CAP(self, CAP):
        self.CAP = CAP
    def get_Comune(self):
        return self.Comune
    def set_Comune(self, Comune):
        self.Comune = Comune
    def get_Provincia(self):
        return self.Provincia
    def set_Provincia(self, Provincia):
        self.Provincia = Provincia
    def get_Nazione(self):
        return self.Nazione
    def set_Nazione(self, Nazione):
        self.Nazione = Nazione
    def validate_String60LatinType(self, value):
        result = True
        # Validate type String60LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60LatinType_patterns_, ))
                result = False
        return result
    validate_String60LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,60})$']]
    def validate_NumeroCivicoType(self, value):
        result = True
        # Validate type NumeroCivicoType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_NumeroCivicoType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_NumeroCivicoType_patterns_, ))
                result = False
        return result
    validate_NumeroCivicoType_patterns_ = [['^(([\x00-\x7f]{1,8}))$']]
    def validate_CAPType(self, value):
        result = True
        # Validate type CAPType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CAPType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CAPType_patterns_, ))
                result = False
        return result
    validate_CAPType_patterns_ = [['^([0-9][0-9][0-9][0-9][0-9])$']]
    def validate_ProvinciaType(self, value):
        result = True
        # Validate type ProvinciaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_ProvinciaType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ProvinciaType_patterns_, ))
                result = False
        return result
    validate_ProvinciaType_patterns_ = [['^([A-Z]{2})$']]
    def validate_NazioneType(self, value):
        result = True
        # Validate type NazioneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_NazioneType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_NazioneType_patterns_, ))
                result = False
        return result
    validate_NazioneType_patterns_ = [['^([A-Z]{2})$']]
    def _hasContent(self):
        if (
            self.Indirizzo is not None or
            self.NumeroCivico is not None or
            self.CAP is not None or
            self.Comune is not None or
            self.Provincia is not None or
            self.Nazione != "IT"
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='IndirizzoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IndirizzoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IndirizzoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IndirizzoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IndirizzoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IndirizzoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='IndirizzoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Indirizzo is not None:
            namespaceprefix_ = self.Indirizzo_nsprefix_ + ':' if (UseCapturedNS_ and self.Indirizzo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIndirizzo>%s</%sIndirizzo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Indirizzo), input_name='Indirizzo')), namespaceprefix_ , eol_))
        if self.NumeroCivico is not None:
            namespaceprefix_ = self.NumeroCivico_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroCivico_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroCivico>%s</%sNumeroCivico>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumeroCivico), input_name='NumeroCivico')), namespaceprefix_ , eol_))
        if self.CAP is not None:
            namespaceprefix_ = self.CAP_nsprefix_ + ':' if (UseCapturedNS_ and self.CAP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCAP>%s</%sCAP>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CAP), input_name='CAP')), namespaceprefix_ , eol_))
        if self.Comune is not None:
            namespaceprefix_ = self.Comune_nsprefix_ + ':' if (UseCapturedNS_ and self.Comune_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sComune>%s</%sComune>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Comune), input_name='Comune')), namespaceprefix_ , eol_))
        if self.Provincia is not None:
            namespaceprefix_ = self.Provincia_nsprefix_ + ':' if (UseCapturedNS_ and self.Provincia_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProvincia>%s</%sProvincia>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Provincia), input_name='Provincia')), namespaceprefix_ , eol_))
        if self.Nazione is not None:
            namespaceprefix_ = self.Nazione_nsprefix_ + ':' if (UseCapturedNS_ and self.Nazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNazione>%s</%sNazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Nazione), input_name='Nazione')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Indirizzo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Indirizzo')
            value_ = self.gds_validate_string(value_, node, 'Indirizzo')
            self.Indirizzo = value_
            self.Indirizzo_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.Indirizzo)
        elif nodeName_ == 'NumeroCivico':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumeroCivico')
            value_ = self.gds_validate_string(value_, node, 'NumeroCivico')
            self.NumeroCivico = value_
            self.NumeroCivico_nsprefix_ = child_.prefix
            # validate type NumeroCivicoType
            self.validate_NumeroCivicoType(self.NumeroCivico)
        elif nodeName_ == 'CAP':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CAP')
            value_ = self.gds_validate_string(value_, node, 'CAP')
            self.CAP = value_
            self.CAP_nsprefix_ = child_.prefix
            # validate type CAPType
            self.validate_CAPType(self.CAP)
        elif nodeName_ == 'Comune':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comune')
            value_ = self.gds_validate_string(value_, node, 'Comune')
            self.Comune = value_
            self.Comune_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.Comune)
        elif nodeName_ == 'Provincia':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Provincia')
            value_ = self.gds_validate_string(value_, node, 'Provincia')
            self.Provincia = value_
            self.Provincia_nsprefix_ = child_.prefix
            # validate type ProvinciaType
            self.validate_ProvinciaType(self.Provincia)
        elif nodeName_ == 'Nazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Nazione')
            value_ = self.gds_validate_string(value_, node, 'Nazione')
            self.Nazione = value_
            self.Nazione_nsprefix_ = child_.prefix
            # validate type NazioneType
            self.validate_NazioneType(self.Nazione)
# end class IndirizzoType


class FatturaPrincipaleType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NumeroFatturaPrincipale=None, DataFatturaPrincipale=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NumeroFatturaPrincipale = NumeroFatturaPrincipale
        self.validate_String20Type(self.NumeroFatturaPrincipale)
        self.NumeroFatturaPrincipale_nsprefix_ = None
        if isinstance(DataFatturaPrincipale, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataFatturaPrincipale, '%Y-%m-%d').date()
        else:
            initvalue_ = DataFatturaPrincipale
        self.DataFatturaPrincipale = initvalue_
        self.DataFatturaPrincipale_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FatturaPrincipaleType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FatturaPrincipaleType.subclass:
            return FatturaPrincipaleType.subclass(*args_, **kwargs_)
        else:
            return FatturaPrincipaleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NumeroFatturaPrincipale(self):
        return self.NumeroFatturaPrincipale
    def set_NumeroFatturaPrincipale(self, NumeroFatturaPrincipale):
        self.NumeroFatturaPrincipale = NumeroFatturaPrincipale
    def get_DataFatturaPrincipale(self):
        return self.DataFatturaPrincipale
    def set_DataFatturaPrincipale(self, DataFatturaPrincipale):
        self.DataFatturaPrincipale = DataFatturaPrincipale
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def _hasContent(self):
        if (
            self.NumeroFatturaPrincipale is not None or
            self.DataFatturaPrincipale is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='FatturaPrincipaleType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FatturaPrincipaleType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FatturaPrincipaleType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FatturaPrincipaleType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FatturaPrincipaleType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FatturaPrincipaleType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='FatturaPrincipaleType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NumeroFatturaPrincipale is not None:
            namespaceprefix_ = self.NumeroFatturaPrincipale_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroFatturaPrincipale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroFatturaPrincipale>%s</%sNumeroFatturaPrincipale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumeroFatturaPrincipale), input_name='NumeroFatturaPrincipale')), namespaceprefix_ , eol_))
        if self.DataFatturaPrincipale is not None:
            namespaceprefix_ = self.DataFatturaPrincipale_nsprefix_ + ':' if (UseCapturedNS_ and self.DataFatturaPrincipale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataFatturaPrincipale>%s</%sDataFatturaPrincipale>%s' % (namespaceprefix_ , self.gds_format_date(self.DataFatturaPrincipale, input_name='DataFatturaPrincipale'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'NumeroFatturaPrincipale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumeroFatturaPrincipale')
            value_ = self.gds_validate_string(value_, node, 'NumeroFatturaPrincipale')
            self.NumeroFatturaPrincipale = value_
            self.NumeroFatturaPrincipale_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.NumeroFatturaPrincipale)
        elif nodeName_ == 'DataFatturaPrincipale':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataFatturaPrincipale = dval_
            self.DataFatturaPrincipale_nsprefix_ = child_.prefix
# end class FatturaPrincipaleType


class CedentePrestatoreType(GeneratedsSuper):
    """CedentePrestatoreType --
    Blocco relativo ai dati del Cedente / Prestatore
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DatiAnagrafici=None, Sede=None, StabileOrganizzazione=None, IscrizioneREA=None, Contatti=None, RiferimentoAmministrazione=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiAnagrafici: "DatiAnagraficiCedenteType" = DatiAnagrafici
        self.DatiAnagrafici_nsprefix_ = None
        self.Sede = Sede
        self.Sede_nsprefix_ = None
        self.StabileOrganizzazione = StabileOrganizzazione
        self.StabileOrganizzazione_nsprefix_ = None
        self.IscrizioneREA = IscrizioneREA
        self.IscrizioneREA_nsprefix_ = None
        self.Contatti = Contatti
        self.Contatti_nsprefix_ = None
        self.RiferimentoAmministrazione = RiferimentoAmministrazione
        self.validate_String20Type(self.RiferimentoAmministrazione)
        self.RiferimentoAmministrazione_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CedentePrestatoreType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CedentePrestatoreType.subclass:
            return CedentePrestatoreType.subclass(*args_, **kwargs_)
        else:
            return CedentePrestatoreType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiAnagrafici(self):
        return self.DatiAnagrafici
    def set_DatiAnagrafici(self, DatiAnagrafici):
        self.DatiAnagrafici = DatiAnagrafici
    def get_Sede(self):
        return self.Sede
    def set_Sede(self, Sede):
        self.Sede = Sede
    def get_StabileOrganizzazione(self):
        return self.StabileOrganizzazione
    def set_StabileOrganizzazione(self, StabileOrganizzazione):
        self.StabileOrganizzazione = StabileOrganizzazione
    def get_IscrizioneREA(self):
        return self.IscrizioneREA
    def set_IscrizioneREA(self, IscrizioneREA):
        self.IscrizioneREA = IscrizioneREA
    def get_Contatti(self):
        return self.Contatti
    def set_Contatti(self, Contatti):
        self.Contatti = Contatti
    def get_RiferimentoAmministrazione(self):
        return self.RiferimentoAmministrazione
    def set_RiferimentoAmministrazione(self, RiferimentoAmministrazione):
        self.RiferimentoAmministrazione = RiferimentoAmministrazione
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def _hasContent(self):
        if (
            self.DatiAnagrafici is not None or
            self.Sede is not None or
            self.StabileOrganizzazione is not None or
            self.IscrizioneREA is not None or
            self.Contatti is not None or
            self.RiferimentoAmministrazione is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CedentePrestatoreType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CedentePrestatoreType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CedentePrestatoreType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CedentePrestatoreType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CedentePrestatoreType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CedentePrestatoreType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CedentePrestatoreType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiAnagrafici is not None:
            namespaceprefix_ = self.DatiAnagrafici_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiAnagrafici_nsprefix_) else ''
            self.DatiAnagrafici.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiAnagrafici', pretty_print=pretty_print)
        if self.Sede is not None:
            namespaceprefix_ = self.Sede_nsprefix_ + ':' if (UseCapturedNS_ and self.Sede_nsprefix_) else ''
            self.Sede.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Sede', pretty_print=pretty_print)
        if self.StabileOrganizzazione is not None:
            namespaceprefix_ = self.StabileOrganizzazione_nsprefix_ + ':' if (UseCapturedNS_ and self.StabileOrganizzazione_nsprefix_) else ''
            self.StabileOrganizzazione.export(outfile, level, namespaceprefix_, namespacedef_='', name_='StabileOrganizzazione', pretty_print=pretty_print)
        if self.IscrizioneREA is not None:
            namespaceprefix_ = self.IscrizioneREA_nsprefix_ + ':' if (UseCapturedNS_ and self.IscrizioneREA_nsprefix_) else ''
            self.IscrizioneREA.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IscrizioneREA', pretty_print=pretty_print)
        if self.Contatti is not None:
            namespaceprefix_ = self.Contatti_nsprefix_ + ':' if (UseCapturedNS_ and self.Contatti_nsprefix_) else ''
            self.Contatti.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contatti', pretty_print=pretty_print)
        if self.RiferimentoAmministrazione is not None:
            namespaceprefix_ = self.RiferimentoAmministrazione_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoAmministrazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoAmministrazione>%s</%sRiferimentoAmministrazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RiferimentoAmministrazione), input_name='RiferimentoAmministrazione')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiAnagrafici':
            obj_ = DatiAnagraficiCedenteType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiAnagrafici = obj_
            obj_.original_tagname_ = 'DatiAnagrafici'
        elif nodeName_ == 'Sede':
            obj_ = IndirizzoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Sede = obj_
            obj_.original_tagname_ = 'Sede'
        elif nodeName_ == 'StabileOrganizzazione':
            obj_ = IndirizzoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.StabileOrganizzazione = obj_
            obj_.original_tagname_ = 'StabileOrganizzazione'
        elif nodeName_ == 'IscrizioneREA':
            obj_ = IscrizioneREAType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IscrizioneREA = obj_
            obj_.original_tagname_ = 'IscrizioneREA'
        elif nodeName_ == 'Contatti':
            obj_ = ContattiType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contatti = obj_
            obj_.original_tagname_ = 'Contatti'
        elif nodeName_ == 'RiferimentoAmministrazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RiferimentoAmministrazione')
            value_ = self.gds_validate_string(value_, node, 'RiferimentoAmministrazione')
            self.RiferimentoAmministrazione = value_
            self.RiferimentoAmministrazione_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.RiferimentoAmministrazione)
# end class CedentePrestatoreType


class DatiAnagraficiCedenteType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, AlboProfessionale=None, ProvinciaAlbo=None, NumeroIscrizioneAlbo=None, DataIscrizioneAlbo=None, RegimeFiscale=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdFiscaleIVA = IdFiscaleIVA
        self.IdFiscaleIVA_nsprefix_ = None
        self.CodiceFiscale = CodiceFiscale
        self.validate_CodiceFiscaleType(self.CodiceFiscale)
        self.CodiceFiscale_nsprefix_ = None
        self.Anagrafica = Anagrafica
        self.Anagrafica_nsprefix_ = None
        self.AlboProfessionale = AlboProfessionale
        self.validate_String60LatinType(self.AlboProfessionale)
        self.AlboProfessionale_nsprefix_ = None
        self.ProvinciaAlbo = ProvinciaAlbo
        self.validate_ProvinciaType(self.ProvinciaAlbo)
        self.ProvinciaAlbo_nsprefix_ = None
        self.NumeroIscrizioneAlbo = NumeroIscrizioneAlbo
        self.validate_String60Type(self.NumeroIscrizioneAlbo)
        self.NumeroIscrizioneAlbo_nsprefix_ = None
        if isinstance(DataIscrizioneAlbo, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataIscrizioneAlbo, '%Y-%m-%d').date()
        else:
            initvalue_ = DataIscrizioneAlbo
        self.DataIscrizioneAlbo = initvalue_
        self.DataIscrizioneAlbo_nsprefix_ = None
        self.RegimeFiscale = RegimeFiscale
        self.validate_RegimeFiscaleType(self.RegimeFiscale)
        self.RegimeFiscale_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiAnagraficiCedenteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiAnagraficiCedenteType.subclass:
            return DatiAnagraficiCedenteType.subclass(*args_, **kwargs_)
        else:
            return DatiAnagraficiCedenteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdFiscaleIVA(self):
        return self.IdFiscaleIVA
    def set_IdFiscaleIVA(self, IdFiscaleIVA):
        self.IdFiscaleIVA = IdFiscaleIVA
    def get_CodiceFiscale(self):
        return self.CodiceFiscale
    def set_CodiceFiscale(self, CodiceFiscale):
        self.CodiceFiscale = CodiceFiscale
    def get_Anagrafica(self):
        return self.Anagrafica
    def set_Anagrafica(self, Anagrafica):
        self.Anagrafica = Anagrafica
    def get_AlboProfessionale(self):
        return self.AlboProfessionale
    def set_AlboProfessionale(self, AlboProfessionale):
        self.AlboProfessionale = AlboProfessionale
    def get_ProvinciaAlbo(self):
        return self.ProvinciaAlbo
    def set_ProvinciaAlbo(self, ProvinciaAlbo):
        self.ProvinciaAlbo = ProvinciaAlbo
    def get_NumeroIscrizioneAlbo(self):
        return self.NumeroIscrizioneAlbo
    def set_NumeroIscrizioneAlbo(self, NumeroIscrizioneAlbo):
        self.NumeroIscrizioneAlbo = NumeroIscrizioneAlbo
    def get_DataIscrizioneAlbo(self):
        return self.DataIscrizioneAlbo
    def set_DataIscrizioneAlbo(self, DataIscrizioneAlbo):
        self.DataIscrizioneAlbo = DataIscrizioneAlbo
    def get_RegimeFiscale(self) -> "RegimeFiscaleType":
        return self.RegimeFiscale
    def set_RegimeFiscale(self, RegimeFiscale):
        self.RegimeFiscale = RegimeFiscale
    def validate_CodiceFiscaleType(self, value):
        result = True
        # Validate type CodiceFiscaleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CodiceFiscaleType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CodiceFiscaleType_patterns_, ))
                result = False
        return result
    validate_CodiceFiscaleType_patterns_ = [['^([A-Z0-9]{11,16})$']]
    def validate_String60LatinType(self, value):
        result = True
        # Validate type String60LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60LatinType_patterns_, ))
                result = False
        return result
    validate_String60LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,60})$']]
    def validate_ProvinciaType(self, value):
        result = True
        # Validate type ProvinciaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_ProvinciaType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ProvinciaType_patterns_, ))
                result = False
        return result
    validate_ProvinciaType_patterns_ = [['^([A-Z]{2})$']]
    def validate_String60Type(self, value):
        result = True
        # Validate type String60Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60Type_patterns_, ))
                result = False
        return result
    validate_String60Type_patterns_ = [['^(([\x00-\x7f]{1,60}))$']]
    def validate_RegimeFiscaleType(self, value):
        result = True
        # Validate type RegimeFiscaleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['RF01', 'RF02', 'RF03', 'RF04', 'RF05', 'RF06', 'RF07', 'RF08', 'RF09', 'RF10', 'RF11', 'RF12', 'RF13', 'RF14', 'RF15', 'RF16', 'RF17', 'RF19', 'RF18']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on RegimeFiscaleType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on RegimeFiscaleType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.IdFiscaleIVA is not None or
            self.CodiceFiscale is not None or
            self.Anagrafica is not None or
            self.AlboProfessionale is not None or
            self.ProvinciaAlbo is not None or
            self.NumeroIscrizioneAlbo is not None or
            self.DataIscrizioneAlbo is not None or
            self.RegimeFiscale is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiCedenteType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiAnagraficiCedenteType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiAnagraficiCedenteType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiAnagraficiCedenteType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiAnagraficiCedenteType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiAnagraficiCedenteType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiCedenteType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdFiscaleIVA is not None:
            namespaceprefix_ = self.IdFiscaleIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.IdFiscaleIVA_nsprefix_) else ''
            self.IdFiscaleIVA.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdFiscaleIVA', pretty_print=pretty_print)
        if self.CodiceFiscale is not None:
            namespaceprefix_ = self.CodiceFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceFiscale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceFiscale>%s</%sCodiceFiscale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceFiscale), input_name='CodiceFiscale')), namespaceprefix_ , eol_))
        if self.Anagrafica is not None:
            namespaceprefix_ = self.Anagrafica_nsprefix_ + ':' if (UseCapturedNS_ and self.Anagrafica_nsprefix_) else ''
            self.Anagrafica.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Anagrafica', pretty_print=pretty_print)
        if self.AlboProfessionale is not None:
            namespaceprefix_ = self.AlboProfessionale_nsprefix_ + ':' if (UseCapturedNS_ and self.AlboProfessionale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAlboProfessionale>%s</%sAlboProfessionale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AlboProfessionale), input_name='AlboProfessionale')), namespaceprefix_ , eol_))
        if self.ProvinciaAlbo is not None:
            namespaceprefix_ = self.ProvinciaAlbo_nsprefix_ + ':' if (UseCapturedNS_ and self.ProvinciaAlbo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProvinciaAlbo>%s</%sProvinciaAlbo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProvinciaAlbo), input_name='ProvinciaAlbo')), namespaceprefix_ , eol_))
        if self.NumeroIscrizioneAlbo is not None:
            namespaceprefix_ = self.NumeroIscrizioneAlbo_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroIscrizioneAlbo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroIscrizioneAlbo>%s</%sNumeroIscrizioneAlbo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumeroIscrizioneAlbo), input_name='NumeroIscrizioneAlbo')), namespaceprefix_ , eol_))
        if self.DataIscrizioneAlbo is not None:
            namespaceprefix_ = self.DataIscrizioneAlbo_nsprefix_ + ':' if (UseCapturedNS_ and self.DataIscrizioneAlbo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataIscrizioneAlbo>%s</%sDataIscrizioneAlbo>%s' % (namespaceprefix_ , self.gds_format_date(self.DataIscrizioneAlbo, input_name='DataIscrizioneAlbo'), namespaceprefix_ , eol_))
        if self.RegimeFiscale is not None:
            namespaceprefix_ = self.RegimeFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.RegimeFiscale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegimeFiscale>%s</%sRegimeFiscale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RegimeFiscale), input_name='RegimeFiscale')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdFiscaleIVA':
            obj_ = IdFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdFiscaleIVA = obj_
            obj_.original_tagname_ = 'IdFiscaleIVA'
        elif nodeName_ == 'CodiceFiscale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceFiscale')
            value_ = self.gds_validate_string(value_, node, 'CodiceFiscale')
            self.CodiceFiscale = value_
            self.CodiceFiscale_nsprefix_ = child_.prefix
            # validate type CodiceFiscaleType
            self.validate_CodiceFiscaleType(self.CodiceFiscale)
        elif nodeName_ == 'Anagrafica':
            obj_ = AnagraficaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Anagrafica = obj_
            obj_.original_tagname_ = 'Anagrafica'
        elif nodeName_ == 'AlboProfessionale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AlboProfessionale')
            value_ = self.gds_validate_string(value_, node, 'AlboProfessionale')
            self.AlboProfessionale = value_
            self.AlboProfessionale_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.AlboProfessionale)
        elif nodeName_ == 'ProvinciaAlbo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProvinciaAlbo')
            value_ = self.gds_validate_string(value_, node, 'ProvinciaAlbo')
            self.ProvinciaAlbo = value_
            self.ProvinciaAlbo_nsprefix_ = child_.prefix
            # validate type ProvinciaType
            self.validate_ProvinciaType(self.ProvinciaAlbo)
        elif nodeName_ == 'NumeroIscrizioneAlbo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumeroIscrizioneAlbo')
            value_ = self.gds_validate_string(value_, node, 'NumeroIscrizioneAlbo')
            self.NumeroIscrizioneAlbo = value_
            self.NumeroIscrizioneAlbo_nsprefix_ = child_.prefix
            # validate type String60Type
            self.validate_String60Type(self.NumeroIscrizioneAlbo)
        elif nodeName_ == 'DataIscrizioneAlbo':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataIscrizioneAlbo = dval_
            self.DataIscrizioneAlbo_nsprefix_ = child_.prefix
        elif nodeName_ == 'RegimeFiscale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RegimeFiscale')
            value_ = self.gds_validate_string(value_, node, 'RegimeFiscale')
            self.RegimeFiscale = value_
            self.RegimeFiscale_nsprefix_ = child_.prefix
            # validate type RegimeFiscaleType
            self.validate_RegimeFiscaleType(self.RegimeFiscale)
# end class DatiAnagraficiCedenteType


class AnagraficaType(GeneratedsSuper):
    """AnagraficaType --
    Il campo Denominazione
    è
    in alternativa ai campi Nome e Cognome
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Denominazione=None, Nome=None, Cognome=None, Titolo=None, CodEORI=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Denominazione = Denominazione
        self.validate_String80LatinType(self.Denominazione)
        self.Denominazione_nsprefix_ = None
        self.Nome = Nome
        self.validate_String60LatinType(self.Nome)
        self.Nome_nsprefix_ = None
        self.Cognome = Cognome
        self.validate_String60LatinType(self.Cognome)
        self.Cognome_nsprefix_ = None
        self.Titolo = Titolo
        self.validate_TitoloType(self.Titolo)
        self.Titolo_nsprefix_ = None
        self.CodEORI = CodEORI
        self.validate_CodEORIType(self.CodEORI)
        self.CodEORI_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AnagraficaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AnagraficaType.subclass:
            return AnagraficaType.subclass(*args_, **kwargs_)
        else:
            return AnagraficaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Denominazione(self):
        return self.Denominazione
    def set_Denominazione(self, Denominazione):
        self.Denominazione = Denominazione
    def get_Nome(self):
        return self.Nome
    def set_Nome(self, Nome):
        self.Nome = Nome
    def get_Cognome(self):
        return self.Cognome
    def set_Cognome(self, Cognome):
        self.Cognome = Cognome
    def get_Titolo(self):
        return self.Titolo
    def set_Titolo(self, Titolo):
        self.Titolo = Titolo
    def get_CodEORI(self):
        return self.CodEORI
    def set_CodEORI(self, CodEORI):
        self.CodEORI = CodEORI
    def validate_String80LatinType(self, value):
        result = True
        # Validate type String80LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String80LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String80LatinType_patterns_, ))
                result = False
        return result
    validate_String80LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,80})$']]
    def validate_String60LatinType(self, value):
        result = True
        # Validate type String60LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60LatinType_patterns_, ))
                result = False
        return result
    validate_String60LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,60})$']]
    def validate_TitoloType(self, value):
        result = True
        # Validate type TitoloType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_TitoloType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_TitoloType_patterns_, ))
                result = False
        return result
    validate_TitoloType_patterns_ = [['^(([\x00-\x7f]{2,10}))$']]
    def validate_CodEORIType(self, value):
        result = True
        # Validate type CodEORIType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 17:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CodEORIType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 13:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CodEORIType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.Denominazione is not None or
            self.Nome is not None or
            self.Cognome is not None or
            self.Titolo is not None or
            self.CodEORI is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='AnagraficaType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AnagraficaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AnagraficaType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AnagraficaType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AnagraficaType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AnagraficaType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='AnagraficaType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Denominazione is not None:
            namespaceprefix_ = self.Denominazione_nsprefix_ + ':' if (UseCapturedNS_ and self.Denominazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDenominazione>%s</%sDenominazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Denominazione), input_name='Denominazione')), namespaceprefix_ , eol_))
        if self.Nome is not None:
            namespaceprefix_ = self.Nome_nsprefix_ + ':' if (UseCapturedNS_ and self.Nome_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNome>%s</%sNome>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Nome), input_name='Nome')), namespaceprefix_ , eol_))
        if self.Cognome is not None:
            namespaceprefix_ = self.Cognome_nsprefix_ + ':' if (UseCapturedNS_ and self.Cognome_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCognome>%s</%sCognome>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Cognome), input_name='Cognome')), namespaceprefix_ , eol_))
        if self.Titolo is not None:
            namespaceprefix_ = self.Titolo_nsprefix_ + ':' if (UseCapturedNS_ and self.Titolo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTitolo>%s</%sTitolo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Titolo), input_name='Titolo')), namespaceprefix_ , eol_))
        if self.CodEORI is not None:
            namespaceprefix_ = self.CodEORI_nsprefix_ + ':' if (UseCapturedNS_ and self.CodEORI_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodEORI>%s</%sCodEORI>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodEORI), input_name='CodEORI')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Denominazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Denominazione')
            value_ = self.gds_validate_string(value_, node, 'Denominazione')
            self.Denominazione = value_
            self.Denominazione_nsprefix_ = child_.prefix
            # validate type String80LatinType
            self.validate_String80LatinType(self.Denominazione)
        elif nodeName_ == 'Nome':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Nome')
            value_ = self.gds_validate_string(value_, node, 'Nome')
            self.Nome = value_
            self.Nome_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.Nome)
        elif nodeName_ == 'Cognome':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Cognome')
            value_ = self.gds_validate_string(value_, node, 'Cognome')
            self.Cognome = value_
            self.Cognome_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.Cognome)
        elif nodeName_ == 'Titolo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Titolo')
            value_ = self.gds_validate_string(value_, node, 'Titolo')
            self.Titolo = value_
            self.Titolo_nsprefix_ = child_.prefix
            # validate type TitoloType
            self.validate_TitoloType(self.Titolo)
        elif nodeName_ == 'CodEORI':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodEORI')
            value_ = self.gds_validate_string(value_, node, 'CodEORI')
            self.CodEORI = value_
            self.CodEORI_nsprefix_ = child_.prefix
            # validate type CodEORIType
            self.validate_CodEORIType(self.CodEORI)
# end class AnagraficaType


class DatiAnagraficiVettoreType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, NumeroLicenzaGuida=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdFiscaleIVA = IdFiscaleIVA
        self.IdFiscaleIVA_nsprefix_ = None
        self.CodiceFiscale = CodiceFiscale
        self.validate_CodiceFiscaleType(self.CodiceFiscale)
        self.CodiceFiscale_nsprefix_ = None
        self.Anagrafica = Anagrafica
        self.Anagrafica_nsprefix_ = None
        self.NumeroLicenzaGuida = NumeroLicenzaGuida
        self.validate_String20Type(self.NumeroLicenzaGuida)
        self.NumeroLicenzaGuida_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiAnagraficiVettoreType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiAnagraficiVettoreType.subclass:
            return DatiAnagraficiVettoreType.subclass(*args_, **kwargs_)
        else:
            return DatiAnagraficiVettoreType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdFiscaleIVA(self):
        return self.IdFiscaleIVA
    def set_IdFiscaleIVA(self, IdFiscaleIVA):
        self.IdFiscaleIVA = IdFiscaleIVA
    def get_CodiceFiscale(self):
        return self.CodiceFiscale
    def set_CodiceFiscale(self, CodiceFiscale):
        self.CodiceFiscale = CodiceFiscale
    def get_Anagrafica(self):
        return self.Anagrafica
    def set_Anagrafica(self, Anagrafica):
        self.Anagrafica = Anagrafica
    def get_NumeroLicenzaGuida(self):
        return self.NumeroLicenzaGuida
    def set_NumeroLicenzaGuida(self, NumeroLicenzaGuida):
        self.NumeroLicenzaGuida = NumeroLicenzaGuida
    def validate_CodiceFiscaleType(self, value):
        result = True
        # Validate type CodiceFiscaleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CodiceFiscaleType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CodiceFiscaleType_patterns_, ))
                result = False
        return result
    validate_CodiceFiscaleType_patterns_ = [['^([A-Z0-9]{11,16})$']]
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def _hasContent(self):
        if (
            self.IdFiscaleIVA is not None or
            self.CodiceFiscale is not None or
            self.Anagrafica is not None or
            self.NumeroLicenzaGuida is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiVettoreType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiAnagraficiVettoreType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiAnagraficiVettoreType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiAnagraficiVettoreType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiAnagraficiVettoreType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiAnagraficiVettoreType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiVettoreType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdFiscaleIVA is not None:
            namespaceprefix_ = self.IdFiscaleIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.IdFiscaleIVA_nsprefix_) else ''
            self.IdFiscaleIVA.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdFiscaleIVA', pretty_print=pretty_print)
        if self.CodiceFiscale is not None:
            namespaceprefix_ = self.CodiceFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceFiscale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceFiscale>%s</%sCodiceFiscale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceFiscale), input_name='CodiceFiscale')), namespaceprefix_ , eol_))
        if self.Anagrafica is not None:
            namespaceprefix_ = self.Anagrafica_nsprefix_ + ':' if (UseCapturedNS_ and self.Anagrafica_nsprefix_) else ''
            self.Anagrafica.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Anagrafica', pretty_print=pretty_print)
        if self.NumeroLicenzaGuida is not None:
            namespaceprefix_ = self.NumeroLicenzaGuida_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroLicenzaGuida_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroLicenzaGuida>%s</%sNumeroLicenzaGuida>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumeroLicenzaGuida), input_name='NumeroLicenzaGuida')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdFiscaleIVA':
            obj_ = IdFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdFiscaleIVA = obj_
            obj_.original_tagname_ = 'IdFiscaleIVA'
        elif nodeName_ == 'CodiceFiscale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceFiscale')
            value_ = self.gds_validate_string(value_, node, 'CodiceFiscale')
            self.CodiceFiscale = value_
            self.CodiceFiscale_nsprefix_ = child_.prefix
            # validate type CodiceFiscaleType
            self.validate_CodiceFiscaleType(self.CodiceFiscale)
        elif nodeName_ == 'Anagrafica':
            obj_ = AnagraficaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Anagrafica = obj_
            obj_.original_tagname_ = 'Anagrafica'
        elif nodeName_ == 'NumeroLicenzaGuida':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumeroLicenzaGuida')
            value_ = self.gds_validate_string(value_, node, 'NumeroLicenzaGuida')
            self.NumeroLicenzaGuida = value_
            self.NumeroLicenzaGuida_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.NumeroLicenzaGuida)
# end class DatiAnagraficiVettoreType


class IscrizioneREAType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Ufficio=None, NumeroREA=None, CapitaleSociale=None, SocioUnico=None, StatoLiquidazione=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Ufficio = Ufficio
        self.validate_ProvinciaType(self.Ufficio)
        self.Ufficio_nsprefix_ = None
        self.NumeroREA = NumeroREA
        self.validate_String20Type(self.NumeroREA)
        self.NumeroREA_nsprefix_ = None
        self.CapitaleSociale = CapitaleSociale
        self.validate_Amount2DecimalType(self.CapitaleSociale)
        self.CapitaleSociale_nsprefix_ = None
        self.SocioUnico = SocioUnico
        self.validate_SocioUnicoType(self.SocioUnico)
        self.SocioUnico_nsprefix_ = None
        self.StatoLiquidazione = StatoLiquidazione
        self.validate_StatoLiquidazioneType(self.StatoLiquidazione)
        self.StatoLiquidazione_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IscrizioneREAType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IscrizioneREAType.subclass:
            return IscrizioneREAType.subclass(*args_, **kwargs_)
        else:
            return IscrizioneREAType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Ufficio(self):
        return self.Ufficio
    def set_Ufficio(self, Ufficio):
        self.Ufficio = Ufficio
    def get_NumeroREA(self):
        return self.NumeroREA
    def set_NumeroREA(self, NumeroREA):
        self.NumeroREA = NumeroREA
    def get_CapitaleSociale(self):
        return self.CapitaleSociale
    def set_CapitaleSociale(self, CapitaleSociale):
        self.CapitaleSociale = CapitaleSociale
    def get_SocioUnico(self):
        return self.SocioUnico
    def set_SocioUnico(self, SocioUnico):
        self.SocioUnico = SocioUnico
    def get_StatoLiquidazione(self):
        return self.StatoLiquidazione
    def set_StatoLiquidazione(self, StatoLiquidazione):
        self.StatoLiquidazione = StatoLiquidazione
    def validate_ProvinciaType(self, value):
        result = True
        # Validate type ProvinciaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_ProvinciaType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ProvinciaType_patterns_, ))
                result = False
        return result
    validate_ProvinciaType_patterns_ = [['^([A-Z]{2})$']]
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def validate_SocioUnicoType(self, value):
        result = True
        # Validate type SocioUnicoType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SU', 'SM']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SocioUnicoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_StatoLiquidazioneType(self, value):
        result = True
        # Validate type StatoLiquidazioneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['LS', 'LN']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StatoLiquidazioneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.Ufficio is not None or
            self.NumeroREA is not None or
            self.CapitaleSociale is not None or
            self.SocioUnico is not None or
            self.StatoLiquidazione is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='IscrizioneREAType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IscrizioneREAType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IscrizioneREAType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IscrizioneREAType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IscrizioneREAType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IscrizioneREAType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='IscrizioneREAType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Ufficio is not None:
            namespaceprefix_ = self.Ufficio_nsprefix_ + ':' if (UseCapturedNS_ and self.Ufficio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUfficio>%s</%sUfficio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Ufficio), input_name='Ufficio')), namespaceprefix_ , eol_))
        if self.NumeroREA is not None:
            namespaceprefix_ = self.NumeroREA_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroREA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroREA>%s</%sNumeroREA>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumeroREA), input_name='NumeroREA')), namespaceprefix_ , eol_))
        if self.CapitaleSociale is not None:
            namespaceprefix_ = self.CapitaleSociale_nsprefix_ + ':' if (UseCapturedNS_ and self.CapitaleSociale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCapitaleSociale>%s</%sCapitaleSociale>%s' % (namespaceprefix_ , self.gds_format_decimal(self.CapitaleSociale, input_name='CapitaleSociale'), namespaceprefix_ , eol_))
        if self.SocioUnico is not None:
            namespaceprefix_ = self.SocioUnico_nsprefix_ + ':' if (UseCapturedNS_ and self.SocioUnico_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSocioUnico>%s</%sSocioUnico>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SocioUnico), input_name='SocioUnico')), namespaceprefix_ , eol_))
        if self.StatoLiquidazione is not None:
            namespaceprefix_ = self.StatoLiquidazione_nsprefix_ + ':' if (UseCapturedNS_ and self.StatoLiquidazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatoLiquidazione>%s</%sStatoLiquidazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StatoLiquidazione), input_name='StatoLiquidazione')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ufficio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Ufficio')
            value_ = self.gds_validate_string(value_, node, 'Ufficio')
            self.Ufficio = value_
            self.Ufficio_nsprefix_ = child_.prefix
            # validate type ProvinciaType
            self.validate_ProvinciaType(self.Ufficio)
        elif nodeName_ == 'NumeroREA':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumeroREA')
            value_ = self.gds_validate_string(value_, node, 'NumeroREA')
            self.NumeroREA = value_
            self.NumeroREA_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.NumeroREA)
        elif nodeName_ == 'CapitaleSociale' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'CapitaleSociale')
            fval_ = self.gds_validate_decimal(fval_, node, 'CapitaleSociale')
            self.CapitaleSociale = fval_
            self.CapitaleSociale_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.CapitaleSociale)
        elif nodeName_ == 'SocioUnico':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SocioUnico')
            value_ = self.gds_validate_string(value_, node, 'SocioUnico')
            self.SocioUnico = value_
            self.SocioUnico_nsprefix_ = child_.prefix
            # validate type SocioUnicoType
            self.validate_SocioUnicoType(self.SocioUnico)
        elif nodeName_ == 'StatoLiquidazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StatoLiquidazione')
            value_ = self.gds_validate_string(value_, node, 'StatoLiquidazione')
            self.StatoLiquidazione = value_
            self.StatoLiquidazione_nsprefix_ = child_.prefix
            # validate type StatoLiquidazioneType
            self.validate_StatoLiquidazioneType(self.StatoLiquidazione)
# end class IscrizioneREAType


class ContattiType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Telefono=None, Fax=None, Email=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Telefono = Telefono
        self.validate_TelFaxType(self.Telefono)
        self.Telefono_nsprefix_ = None
        self.Fax = Fax
        self.validate_TelFaxType(self.Fax)
        self.Fax_nsprefix_ = None
        self.Email = Email
        self.validate_EmailType(self.Email)
        self.Email_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ContattiType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ContattiType.subclass:
            return ContattiType.subclass(*args_, **kwargs_)
        else:
            return ContattiType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Telefono(self):
        return self.Telefono
    def set_Telefono(self, Telefono):
        self.Telefono = Telefono
    def get_Fax(self):
        return self.Fax
    def set_Fax(self, Fax):
        self.Fax = Fax
    def get_Email(self):
        return self.Email
    def set_Email(self, Email):
        self.Email = Email
    def validate_TelFaxType(self, value):
        result = True
        # Validate type TelFaxType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_TelFaxType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_TelFaxType_patterns_, ))
                result = False
        return result
    validate_TelFaxType_patterns_ = [['^(([\x00-\x7f]{5,12}))$']]
    def validate_EmailType(self, value):
        result = True
        # Validate type EmailType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on EmailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailType_patterns_, ))
                result = False
        return result
    validate_EmailType_patterns_ = [['^(.+@.+[.]+.+)$']]
    def _hasContent(self):
        if (
            self.Telefono is not None or
            self.Fax is not None or
            self.Email is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ContattiType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ContattiType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ContattiType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ContattiType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ContattiType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ContattiType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ContattiType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Telefono is not None:
            namespaceprefix_ = self.Telefono_nsprefix_ + ':' if (UseCapturedNS_ and self.Telefono_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTelefono>%s</%sTelefono>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Telefono), input_name='Telefono')), namespaceprefix_ , eol_))
        if self.Fax is not None:
            namespaceprefix_ = self.Fax_nsprefix_ + ':' if (UseCapturedNS_ and self.Fax_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFax>%s</%sFax>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Fax), input_name='Fax')), namespaceprefix_ , eol_))
        if self.Email is not None:
            namespaceprefix_ = self.Email_nsprefix_ + ':' if (UseCapturedNS_ and self.Email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmail>%s</%sEmail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Email), input_name='Email')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Telefono':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Telefono')
            value_ = self.gds_validate_string(value_, node, 'Telefono')
            self.Telefono = value_
            self.Telefono_nsprefix_ = child_.prefix
            # validate type TelFaxType
            self.validate_TelFaxType(self.Telefono)
        elif nodeName_ == 'Fax':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Fax')
            value_ = self.gds_validate_string(value_, node, 'Fax')
            self.Fax = value_
            self.Fax_nsprefix_ = child_.prefix
            # validate type TelFaxType
            self.validate_TelFaxType(self.Fax)
        elif nodeName_ == 'Email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Email')
            value_ = self.gds_validate_string(value_, node, 'Email')
            self.Email = value_
            self.Email_nsprefix_ = child_.prefix
            # validate type EmailType
            self.validate_EmailType(self.Email)
# end class ContattiType


class RappresentanteFiscaleType(GeneratedsSuper):
    """RappresentanteFiscaleType --
    Blocco relativo ai dati del Rappresentante Fiscale
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DatiAnagrafici=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiAnagrafici = DatiAnagrafici
        self.DatiAnagrafici_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RappresentanteFiscaleType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RappresentanteFiscaleType.subclass:
            return RappresentanteFiscaleType.subclass(*args_, **kwargs_)
        else:
            return RappresentanteFiscaleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiAnagrafici(self):
        return self.DatiAnagrafici
    def set_DatiAnagrafici(self, DatiAnagrafici):
        self.DatiAnagrafici = DatiAnagrafici
    def _hasContent(self):
        if (
            self.DatiAnagrafici is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='RappresentanteFiscaleType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RappresentanteFiscaleType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RappresentanteFiscaleType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RappresentanteFiscaleType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RappresentanteFiscaleType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RappresentanteFiscaleType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='RappresentanteFiscaleType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiAnagrafici is not None:
            namespaceprefix_ = self.DatiAnagrafici_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiAnagrafici_nsprefix_) else ''
            self.DatiAnagrafici.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiAnagrafici', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiAnagrafici':
            obj_ = DatiAnagraficiRappresentanteType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiAnagrafici = obj_
            obj_.original_tagname_ = 'DatiAnagrafici'
# end class RappresentanteFiscaleType


class DatiAnagraficiRappresentanteType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdFiscaleIVA = IdFiscaleIVA
        self.IdFiscaleIVA_nsprefix_ = None
        self.CodiceFiscale = CodiceFiscale
        self.validate_CodiceFiscaleType(self.CodiceFiscale)
        self.CodiceFiscale_nsprefix_ = None
        self.Anagrafica = Anagrafica
        self.Anagrafica_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiAnagraficiRappresentanteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiAnagraficiRappresentanteType.subclass:
            return DatiAnagraficiRappresentanteType.subclass(*args_, **kwargs_)
        else:
            return DatiAnagraficiRappresentanteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdFiscaleIVA(self):
        return self.IdFiscaleIVA
    def set_IdFiscaleIVA(self, IdFiscaleIVA):
        self.IdFiscaleIVA = IdFiscaleIVA
    def get_CodiceFiscale(self):
        return self.CodiceFiscale
    def set_CodiceFiscale(self, CodiceFiscale):
        self.CodiceFiscale = CodiceFiscale
    def get_Anagrafica(self):
        return self.Anagrafica
    def set_Anagrafica(self, Anagrafica):
        self.Anagrafica = Anagrafica
    def validate_CodiceFiscaleType(self, value):
        result = True
        # Validate type CodiceFiscaleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CodiceFiscaleType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CodiceFiscaleType_patterns_, ))
                result = False
        return result
    validate_CodiceFiscaleType_patterns_ = [['^([A-Z0-9]{11,16})$']]
    def _hasContent(self):
        if (
            self.IdFiscaleIVA is not None or
            self.CodiceFiscale is not None or
            self.Anagrafica is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiRappresentanteType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiAnagraficiRappresentanteType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiAnagraficiRappresentanteType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiAnagraficiRappresentanteType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiAnagraficiRappresentanteType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiAnagraficiRappresentanteType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiRappresentanteType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdFiscaleIVA is not None:
            namespaceprefix_ = self.IdFiscaleIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.IdFiscaleIVA_nsprefix_) else ''
            self.IdFiscaleIVA.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdFiscaleIVA', pretty_print=pretty_print)
        if self.CodiceFiscale is not None:
            namespaceprefix_ = self.CodiceFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceFiscale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceFiscale>%s</%sCodiceFiscale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceFiscale), input_name='CodiceFiscale')), namespaceprefix_ , eol_))
        if self.Anagrafica is not None:
            namespaceprefix_ = self.Anagrafica_nsprefix_ + ':' if (UseCapturedNS_ and self.Anagrafica_nsprefix_) else ''
            self.Anagrafica.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Anagrafica', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdFiscaleIVA':
            obj_ = IdFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdFiscaleIVA = obj_
            obj_.original_tagname_ = 'IdFiscaleIVA'
        elif nodeName_ == 'CodiceFiscale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceFiscale')
            value_ = self.gds_validate_string(value_, node, 'CodiceFiscale')
            self.CodiceFiscale = value_
            self.CodiceFiscale_nsprefix_ = child_.prefix
            # validate type CodiceFiscaleType
            self.validate_CodiceFiscaleType(self.CodiceFiscale)
        elif nodeName_ == 'Anagrafica':
            obj_ = AnagraficaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Anagrafica = obj_
            obj_.original_tagname_ = 'Anagrafica'
# end class DatiAnagraficiRappresentanteType


class CessionarioCommittenteType(GeneratedsSuper):
    """CessionarioCommittenteType -- Blocco relativo ai dati del Cessionario / Committente
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DatiAnagrafici=None, Sede=None, StabileOrganizzazione=None, RappresentanteFiscale=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiAnagrafici = DatiAnagrafici
        self.DatiAnagrafici_nsprefix_ = None
        self.Sede = Sede
        self.Sede_nsprefix_ = None
        self.StabileOrganizzazione = StabileOrganizzazione
        self.StabileOrganizzazione_nsprefix_ = None
        self.RappresentanteFiscale = RappresentanteFiscale
        self.RappresentanteFiscale_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CessionarioCommittenteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CessionarioCommittenteType.subclass:
            return CessionarioCommittenteType.subclass(*args_, **kwargs_)
        else:
            return CessionarioCommittenteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiAnagrafici(self):
        return self.DatiAnagrafici
    def set_DatiAnagrafici(self, DatiAnagrafici):
        self.DatiAnagrafici = DatiAnagrafici
    def get_Sede(self):
        return self.Sede
    def set_Sede(self, Sede):
        self.Sede = Sede
    def get_StabileOrganizzazione(self):
        return self.StabileOrganizzazione
    def set_StabileOrganizzazione(self, StabileOrganizzazione):
        self.StabileOrganizzazione = StabileOrganizzazione
    def get_RappresentanteFiscale(self):
        return self.RappresentanteFiscale
    def set_RappresentanteFiscale(self, RappresentanteFiscale):
        self.RappresentanteFiscale = RappresentanteFiscale
    def _hasContent(self):
        if (
            self.DatiAnagrafici is not None or
            self.Sede is not None or
            self.StabileOrganizzazione is not None or
            self.RappresentanteFiscale is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CessionarioCommittenteType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CessionarioCommittenteType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CessionarioCommittenteType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CessionarioCommittenteType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CessionarioCommittenteType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CessionarioCommittenteType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CessionarioCommittenteType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiAnagrafici is not None:
            namespaceprefix_ = self.DatiAnagrafici_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiAnagrafici_nsprefix_) else ''
            self.DatiAnagrafici.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiAnagrafici', pretty_print=pretty_print)
        if self.Sede is not None:
            namespaceprefix_ = self.Sede_nsprefix_ + ':' if (UseCapturedNS_ and self.Sede_nsprefix_) else ''
            self.Sede.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Sede', pretty_print=pretty_print)
        if self.StabileOrganizzazione is not None:
            namespaceprefix_ = self.StabileOrganizzazione_nsprefix_ + ':' if (UseCapturedNS_ and self.StabileOrganizzazione_nsprefix_) else ''
            self.StabileOrganizzazione.export(outfile, level, namespaceprefix_, namespacedef_='', name_='StabileOrganizzazione', pretty_print=pretty_print)
        if self.RappresentanteFiscale is not None:
            namespaceprefix_ = self.RappresentanteFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.RappresentanteFiscale_nsprefix_) else ''
            self.RappresentanteFiscale.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RappresentanteFiscale', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiAnagrafici':
            obj_ = DatiAnagraficiCessionarioType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiAnagrafici = obj_
            obj_.original_tagname_ = 'DatiAnagrafici'
        elif nodeName_ == 'Sede':
            obj_ = IndirizzoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Sede = obj_
            obj_.original_tagname_ = 'Sede'
        elif nodeName_ == 'StabileOrganizzazione':
            obj_ = IndirizzoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.StabileOrganizzazione = obj_
            obj_.original_tagname_ = 'StabileOrganizzazione'
        elif nodeName_ == 'RappresentanteFiscale':
            obj_ = RappresentanteFiscaleCessionarioType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RappresentanteFiscale = obj_
            obj_.original_tagname_ = 'RappresentanteFiscale'
# end class CessionarioCommittenteType


class RappresentanteFiscaleCessionarioType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdFiscaleIVA=None, Denominazione=None, Nome=None, Cognome=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdFiscaleIVA = IdFiscaleIVA
        self.IdFiscaleIVA_nsprefix_ = None
        self.Denominazione = Denominazione
        self.validate_String80LatinType(self.Denominazione)
        self.Denominazione_nsprefix_ = None
        self.Nome = Nome
        self.validate_String60LatinType(self.Nome)
        self.Nome_nsprefix_ = None
        self.Cognome = Cognome
        self.validate_String60LatinType(self.Cognome)
        self.Cognome_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RappresentanteFiscaleCessionarioType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RappresentanteFiscaleCessionarioType.subclass:
            return RappresentanteFiscaleCessionarioType.subclass(*args_, **kwargs_)
        else:
            return RappresentanteFiscaleCessionarioType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdFiscaleIVA(self):
        return self.IdFiscaleIVA
    def set_IdFiscaleIVA(self, IdFiscaleIVA):
        self.IdFiscaleIVA = IdFiscaleIVA
    def get_Denominazione(self):
        return self.Denominazione
    def set_Denominazione(self, Denominazione):
        self.Denominazione = Denominazione
    def get_Nome(self):
        return self.Nome
    def set_Nome(self, Nome):
        self.Nome = Nome
    def get_Cognome(self):
        return self.Cognome
    def set_Cognome(self, Cognome):
        self.Cognome = Cognome
    def validate_String80LatinType(self, value):
        result = True
        # Validate type String80LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String80LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String80LatinType_patterns_, ))
                result = False
        return result
    validate_String80LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,80})$']]
    def validate_String60LatinType(self, value):
        result = True
        # Validate type String60LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60LatinType_patterns_, ))
                result = False
        return result
    validate_String60LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,60})$']]
    def _hasContent(self):
        if (
            self.IdFiscaleIVA is not None or
            self.Denominazione is not None or
            self.Nome is not None or
            self.Cognome is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='RappresentanteFiscaleCessionarioType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RappresentanteFiscaleCessionarioType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RappresentanteFiscaleCessionarioType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RappresentanteFiscaleCessionarioType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RappresentanteFiscaleCessionarioType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RappresentanteFiscaleCessionarioType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='RappresentanteFiscaleCessionarioType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdFiscaleIVA is not None:
            namespaceprefix_ = self.IdFiscaleIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.IdFiscaleIVA_nsprefix_) else ''
            self.IdFiscaleIVA.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdFiscaleIVA', pretty_print=pretty_print)
        if self.Denominazione is not None:
            namespaceprefix_ = self.Denominazione_nsprefix_ + ':' if (UseCapturedNS_ and self.Denominazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDenominazione>%s</%sDenominazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Denominazione), input_name='Denominazione')), namespaceprefix_ , eol_))
        if self.Nome is not None:
            namespaceprefix_ = self.Nome_nsprefix_ + ':' if (UseCapturedNS_ and self.Nome_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNome>%s</%sNome>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Nome), input_name='Nome')), namespaceprefix_ , eol_))
        if self.Cognome is not None:
            namespaceprefix_ = self.Cognome_nsprefix_ + ':' if (UseCapturedNS_ and self.Cognome_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCognome>%s</%sCognome>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Cognome), input_name='Cognome')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdFiscaleIVA':
            obj_ = IdFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdFiscaleIVA = obj_
            obj_.original_tagname_ = 'IdFiscaleIVA'
        elif nodeName_ == 'Denominazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Denominazione')
            value_ = self.gds_validate_string(value_, node, 'Denominazione')
            self.Denominazione = value_
            self.Denominazione_nsprefix_ = child_.prefix
            # validate type String80LatinType
            self.validate_String80LatinType(self.Denominazione)
        elif nodeName_ == 'Nome':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Nome')
            value_ = self.gds_validate_string(value_, node, 'Nome')
            self.Nome = value_
            self.Nome_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.Nome)
        elif nodeName_ == 'Cognome':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Cognome')
            value_ = self.gds_validate_string(value_, node, 'Cognome')
            self.Cognome = value_
            self.Cognome_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.Cognome)
# end class RappresentanteFiscaleCessionarioType


class DatiAnagraficiCessionarioType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdFiscaleIVA = IdFiscaleIVA
        self.IdFiscaleIVA_nsprefix_ = None
        self.CodiceFiscale = CodiceFiscale
        self.validate_CodiceFiscaleType(self.CodiceFiscale)
        self.CodiceFiscale_nsprefix_ = None
        self.Anagrafica = Anagrafica
        self.Anagrafica_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiAnagraficiCessionarioType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiAnagraficiCessionarioType.subclass:
            return DatiAnagraficiCessionarioType.subclass(*args_, **kwargs_)
        else:
            return DatiAnagraficiCessionarioType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdFiscaleIVA(self):
        return self.IdFiscaleIVA
    def set_IdFiscaleIVA(self, IdFiscaleIVA):
        self.IdFiscaleIVA = IdFiscaleIVA
    def get_CodiceFiscale(self):
        return self.CodiceFiscale
    def set_CodiceFiscale(self, CodiceFiscale):
        self.CodiceFiscale = CodiceFiscale
    def get_Anagrafica(self):
        return self.Anagrafica
    def set_Anagrafica(self, Anagrafica):
        self.Anagrafica = Anagrafica
    def validate_CodiceFiscaleType(self, value):
        result = True
        # Validate type CodiceFiscaleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CodiceFiscaleType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CodiceFiscaleType_patterns_, ))
                result = False
        return result
    validate_CodiceFiscaleType_patterns_ = [['^([A-Z0-9]{11,16})$']]
    def _hasContent(self):
        if (
            self.IdFiscaleIVA is not None or
            self.CodiceFiscale is not None or
            self.Anagrafica is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiCessionarioType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiAnagraficiCessionarioType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiAnagraficiCessionarioType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiAnagraficiCessionarioType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiAnagraficiCessionarioType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiAnagraficiCessionarioType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiCessionarioType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdFiscaleIVA is not None:
            namespaceprefix_ = self.IdFiscaleIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.IdFiscaleIVA_nsprefix_) else ''
            self.IdFiscaleIVA.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdFiscaleIVA', pretty_print=pretty_print)
        if self.CodiceFiscale is not None:
            namespaceprefix_ = self.CodiceFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceFiscale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceFiscale>%s</%sCodiceFiscale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceFiscale), input_name='CodiceFiscale')), namespaceprefix_ , eol_))
        if self.Anagrafica is not None:
            namespaceprefix_ = self.Anagrafica_nsprefix_ + ':' if (UseCapturedNS_ and self.Anagrafica_nsprefix_) else ''
            self.Anagrafica.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Anagrafica', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdFiscaleIVA':
            obj_ = IdFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdFiscaleIVA = obj_
            obj_.original_tagname_ = 'IdFiscaleIVA'
        elif nodeName_ == 'CodiceFiscale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceFiscale')
            value_ = self.gds_validate_string(value_, node, 'CodiceFiscale')
            self.CodiceFiscale = value_
            self.CodiceFiscale_nsprefix_ = child_.prefix
            # validate type CodiceFiscaleType
            self.validate_CodiceFiscaleType(self.CodiceFiscale)
        elif nodeName_ == 'Anagrafica':
            obj_ = AnagraficaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Anagrafica = obj_
            obj_.original_tagname_ = 'Anagrafica'
# end class DatiAnagraficiCessionarioType


class DatiBeniServiziType(GeneratedsSuper):
    """DatiBeniServiziType --
    Blocco relativo ai dati di Beni Servizi della Fattura	Elettronica
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DettaglioLinee=None, DatiRiepilogo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if DettaglioLinee is None:
            self.DettaglioLinee: List["DettaglioLineeType"] = []
        else:
            self.DettaglioLinee: List["DettaglioLineeType"] = DettaglioLinee
        self.DettaglioLinee_nsprefix_ = None
        if DatiRiepilogo is None:
            self.DatiRiepilogo: List["DatiRiepilogoType"] = []
        else:
            self.DatiRiepilogo: List["DatiRiepilogoType"] = DatiRiepilogo
        self.DatiRiepilogo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiBeniServiziType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiBeniServiziType.subclass:
            return DatiBeniServiziType.subclass(*args_, **kwargs_)
        else:
            return DatiBeniServiziType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DettaglioLinee(self):
        return self.DettaglioLinee
    def set_DettaglioLinee(self, DettaglioLinee):
        self.DettaglioLinee = DettaglioLinee
    def add_DettaglioLinee(self, value):
        self.DettaglioLinee.append(value)
    def insert_DettaglioLinee_at(self, index, value):
        self.DettaglioLinee.insert(index, value)
    def replace_DettaglioLinee_at(self, index, value):
        self.DettaglioLinee[index] = value
    def get_DatiRiepilogo(self):
        return self.DatiRiepilogo
    def set_DatiRiepilogo(self, DatiRiepilogo):
        self.DatiRiepilogo = DatiRiepilogo
    def add_DatiRiepilogo(self, value):
        self.DatiRiepilogo.append(value)
    def insert_DatiRiepilogo_at(self, index, value):
        self.DatiRiepilogo.insert(index, value)
    def replace_DatiRiepilogo_at(self, index, value):
        self.DatiRiepilogo[index] = value
    def _hasContent(self):
        if (
            self.DettaglioLinee or
            self.DatiRiepilogo
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiBeniServiziType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiBeniServiziType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiBeniServiziType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiBeniServiziType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiBeniServiziType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiBeniServiziType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiBeniServiziType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for DettaglioLinee_ in self.DettaglioLinee:
            namespaceprefix_ = self.DettaglioLinee_nsprefix_ + ':' if (UseCapturedNS_ and self.DettaglioLinee_nsprefix_) else ''
            DettaglioLinee_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DettaglioLinee', pretty_print=pretty_print)
        for DatiRiepilogo_ in self.DatiRiepilogo:
            namespaceprefix_ = self.DatiRiepilogo_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiRiepilogo_nsprefix_) else ''
            DatiRiepilogo_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiRiepilogo', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DettaglioLinee':
            obj_ = DettaglioLineeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DettaglioLinee.append(obj_)
            obj_.original_tagname_ = 'DettaglioLinee'
        elif nodeName_ == 'DatiRiepilogo':
            obj_ = DatiRiepilogoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiRiepilogo.append(obj_)
            obj_.original_tagname_ = 'DatiRiepilogo'
# end class DatiBeniServiziType


class DatiVeicoliType(GeneratedsSuper):
    """DatiVeicoliType --
    Blocco relativo ai dati dei Veicoli della Fattura
    Elettronica (da indicare nei casi di cessioni tra Paesi
    membri di mezzi di trasporto nuovi, in base all'art. 38,
    comma 4 del dl 331 del 1993)
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Data=None, TotalePercorso=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(Data, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Data, '%Y-%m-%d').date()
        else:
            initvalue_ = Data
        self.Data = initvalue_
        self.Data_nsprefix_ = None
        self.TotalePercorso = TotalePercorso
        self.validate_String15Type(self.TotalePercorso)
        self.TotalePercorso_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiVeicoliType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiVeicoliType.subclass:
            return DatiVeicoliType.subclass(*args_, **kwargs_)
        else:
            return DatiVeicoliType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Data(self):
        return self.Data
    def set_Data(self, Data):
        self.Data = Data
    def get_TotalePercorso(self):
        return self.TotalePercorso
    def set_TotalePercorso(self, TotalePercorso):
        self.TotalePercorso = TotalePercorso
    def validate_String15Type(self, value):
        result = True
        # Validate type String15Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String15Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String15Type_patterns_, ))
                result = False
        return result
    validate_String15Type_patterns_ = [['^(([\x00-\x7f]{1,15}))$']]
    def _hasContent(self):
        if (
            self.Data is not None or
            self.TotalePercorso is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiVeicoliType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiVeicoliType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiVeicoliType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiVeicoliType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiVeicoliType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiVeicoliType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiVeicoliType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Data is not None:
            namespaceprefix_ = self.Data_nsprefix_ + ':' if (UseCapturedNS_ and self.Data_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sData>%s</%sData>%s' % (namespaceprefix_ , self.gds_format_date(self.Data, input_name='Data'), namespaceprefix_ , eol_))
        if self.TotalePercorso is not None:
            namespaceprefix_ = self.TotalePercorso_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalePercorso_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalePercorso>%s</%sTotalePercorso>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TotalePercorso), input_name='TotalePercorso')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Data':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Data = dval_
            self.Data_nsprefix_ = child_.prefix
        elif nodeName_ == 'TotalePercorso':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TotalePercorso')
            value_ = self.gds_validate_string(value_, node, 'TotalePercorso')
            self.TotalePercorso = value_
            self.TotalePercorso_nsprefix_ = child_.prefix
            # validate type String15Type
            self.validate_String15Type(self.TotalePercorso)
# end class DatiVeicoliType


class DatiPagamentoType(GeneratedsSuper):
    """DatiPagamentoType --
    Blocco relativo ai dati di Pagamento della Fattura	Elettronica
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CondizioniPagamento=None, DettaglioPagamento=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CondizioniPagamento = CondizioniPagamento
        self.validate_CondizioniPagamentoType(self.CondizioniPagamento)
        self.CondizioniPagamento_nsprefix_ = None
        if DettaglioPagamento is None:
            self.DettaglioPagamento = []
        else:
            self.DettaglioPagamento = DettaglioPagamento
        self.DettaglioPagamento_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiPagamentoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiPagamentoType.subclass:
            return DatiPagamentoType.subclass(*args_, **kwargs_)
        else:
            return DatiPagamentoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CondizioniPagamento(self):
        return self.CondizioniPagamento
    def set_CondizioniPagamento(self, CondizioniPagamento):
        self.CondizioniPagamento = CondizioniPagamento
    def get_DettaglioPagamento(self):
        return self.DettaglioPagamento
    def set_DettaglioPagamento(self, DettaglioPagamento):
        self.DettaglioPagamento = DettaglioPagamento
    def add_DettaglioPagamento(self, value):
        self.DettaglioPagamento.append(value)
    def insert_DettaglioPagamento_at(self, index, value):
        self.DettaglioPagamento.insert(index, value)
    def replace_DettaglioPagamento_at(self, index, value):
        self.DettaglioPagamento[index] = value
    def validate_CondizioniPagamentoType(self, value):
        result = True
        # Validate type CondizioniPagamentoType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['TP01', 'TP02', 'TP03']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CondizioniPagamentoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CondizioniPagamentoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CondizioniPagamentoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.CondizioniPagamento is not None or
            self.DettaglioPagamento
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiPagamentoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiPagamentoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiPagamentoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiPagamentoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiPagamentoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiPagamentoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiPagamentoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CondizioniPagamento is not None:
            namespaceprefix_ = self.CondizioniPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.CondizioniPagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCondizioniPagamento>%s</%sCondizioniPagamento>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CondizioniPagamento), input_name='CondizioniPagamento')), namespaceprefix_ , eol_))
        for DettaglioPagamento_ in self.DettaglioPagamento:
            namespaceprefix_ = self.DettaglioPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.DettaglioPagamento_nsprefix_) else ''
            DettaglioPagamento_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DettaglioPagamento', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CondizioniPagamento':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CondizioniPagamento')
            value_ = self.gds_validate_string(value_, node, 'CondizioniPagamento')
            self.CondizioniPagamento = value_
            self.CondizioniPagamento_nsprefix_ = child_.prefix
            # validate type CondizioniPagamentoType
            self.validate_CondizioniPagamentoType(self.CondizioniPagamento)
        elif nodeName_ == 'DettaglioPagamento':
            obj_ = DettaglioPagamentoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DettaglioPagamento.append(obj_)
            obj_.original_tagname_ = 'DettaglioPagamento'
# end class DatiPagamentoType


class DettaglioPagamentoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Beneficiario=None, ModalitaPagamento=None, DataRiferimentoTerminiPagamento=None, GiorniTerminiPagamento=None, DataScadenzaPagamento=None, ImportoPagamento=None, CodUfficioPostale=None, CognomeQuietanzante=None, NomeQuietanzante=None, CFQuietanzante=None, TitoloQuietanzante=None, IstitutoFinanziario=None, IBAN=None, ABI=None, CAB=None, BIC=None, ScontoPagamentoAnticipato=None, DataLimitePagamentoAnticipato=None, PenalitaPagamentiRitardati=None, DataDecorrenzaPenale=None, CodicePagamento=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Beneficiario = Beneficiario
        self.validate_String200LatinType(self.Beneficiario)
        self.Beneficiario_nsprefix_ = None
        self.ModalitaPagamento = ModalitaPagamento
        self.validate_ModalitaPagamentoType(self.ModalitaPagamento)
        self.ModalitaPagamento_nsprefix_ = None
        if isinstance(DataRiferimentoTerminiPagamento, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataRiferimentoTerminiPagamento, '%Y-%m-%d').date()
        else:
            initvalue_ = DataRiferimentoTerminiPagamento
        self.DataRiferimentoTerminiPagamento = initvalue_
        self.DataRiferimentoTerminiPagamento_nsprefix_ = None
        self.GiorniTerminiPagamento = GiorniTerminiPagamento
        self.validate_GiorniTerminePagamentoType(self.GiorniTerminiPagamento)
        self.GiorniTerminiPagamento_nsprefix_ = None
        if isinstance(DataScadenzaPagamento, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataScadenzaPagamento, '%Y-%m-%d').date()
        else:
            initvalue_ = DataScadenzaPagamento
        self.DataScadenzaPagamento = initvalue_
        self.DataScadenzaPagamento_nsprefix_ = None
        self.ImportoPagamento = ImportoPagamento
        self.validate_Amount2DecimalType(self.ImportoPagamento)
        self.ImportoPagamento_nsprefix_ = None
        self.CodUfficioPostale = CodUfficioPostale
        self.validate_String20Type(self.CodUfficioPostale)
        self.CodUfficioPostale_nsprefix_ = None
        self.CognomeQuietanzante = CognomeQuietanzante
        self.validate_String60LatinType(self.CognomeQuietanzante)
        self.CognomeQuietanzante_nsprefix_ = None
        self.NomeQuietanzante = NomeQuietanzante
        self.validate_String60LatinType(self.NomeQuietanzante)
        self.NomeQuietanzante_nsprefix_ = None
        self.CFQuietanzante = CFQuietanzante
        self.validate_CodiceFiscalePFType(self.CFQuietanzante)
        self.CFQuietanzante_nsprefix_ = None
        self.TitoloQuietanzante = TitoloQuietanzante
        self.validate_TitoloType(self.TitoloQuietanzante)
        self.TitoloQuietanzante_nsprefix_ = None
        self.IstitutoFinanziario = IstitutoFinanziario
        self.validate_String80LatinType(self.IstitutoFinanziario)
        self.IstitutoFinanziario_nsprefix_ = None
        self.IBAN = IBAN
        self.validate_IBANType(self.IBAN)
        self.IBAN_nsprefix_ = None
        self.ABI = ABI
        self.validate_ABIType(self.ABI)
        self.ABI_nsprefix_ = None
        self.CAB = CAB
        self.validate_CABType(self.CAB)
        self.CAB_nsprefix_ = None
        self.BIC = BIC
        self.validate_BICType(self.BIC)
        self.BIC_nsprefix_ = None
        self.ScontoPagamentoAnticipato = ScontoPagamentoAnticipato
        self.validate_Amount2DecimalType(self.ScontoPagamentoAnticipato)
        self.ScontoPagamentoAnticipato_nsprefix_ = None
        if isinstance(DataLimitePagamentoAnticipato, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataLimitePagamentoAnticipato, '%Y-%m-%d').date()
        else:
            initvalue_ = DataLimitePagamentoAnticipato
        self.DataLimitePagamentoAnticipato = initvalue_
        self.DataLimitePagamentoAnticipato_nsprefix_ = None
        self.PenalitaPagamentiRitardati = PenalitaPagamentiRitardati
        self.validate_Amount2DecimalType(self.PenalitaPagamentiRitardati)
        self.PenalitaPagamentiRitardati_nsprefix_ = None
        if isinstance(DataDecorrenzaPenale, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataDecorrenzaPenale, '%Y-%m-%d').date()
        else:
            initvalue_ = DataDecorrenzaPenale
        self.DataDecorrenzaPenale = initvalue_
        self.DataDecorrenzaPenale_nsprefix_ = None
        self.CodicePagamento = CodicePagamento
        self.validate_String60Type(self.CodicePagamento)
        self.CodicePagamento_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DettaglioPagamentoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DettaglioPagamentoType.subclass:
            return DettaglioPagamentoType.subclass(*args_, **kwargs_)
        else:
            return DettaglioPagamentoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Beneficiario(self):
        return self.Beneficiario
    def set_Beneficiario(self, Beneficiario):
        self.Beneficiario = Beneficiario
    def get_ModalitaPagamento(self):
        return self.ModalitaPagamento
    def set_ModalitaPagamento(self, ModalitaPagamento):
        self.ModalitaPagamento = ModalitaPagamento
    def get_DataRiferimentoTerminiPagamento(self):
        return self.DataRiferimentoTerminiPagamento
    def set_DataRiferimentoTerminiPagamento(self, DataRiferimentoTerminiPagamento):
        self.DataRiferimentoTerminiPagamento = DataRiferimentoTerminiPagamento
    def get_GiorniTerminiPagamento(self):
        return self.GiorniTerminiPagamento
    def set_GiorniTerminiPagamento(self, GiorniTerminiPagamento):
        self.GiorniTerminiPagamento = GiorniTerminiPagamento
    def get_DataScadenzaPagamento(self):
        return self.DataScadenzaPagamento
    def set_DataScadenzaPagamento(self, DataScadenzaPagamento):
        self.DataScadenzaPagamento = DataScadenzaPagamento
    def get_ImportoPagamento(self):
        return self.ImportoPagamento
    def set_ImportoPagamento(self, ImportoPagamento):
        self.ImportoPagamento = ImportoPagamento
    def get_CodUfficioPostale(self):
        return self.CodUfficioPostale
    def set_CodUfficioPostale(self, CodUfficioPostale):
        self.CodUfficioPostale = CodUfficioPostale
    def get_CognomeQuietanzante(self):
        return self.CognomeQuietanzante
    def set_CognomeQuietanzante(self, CognomeQuietanzante):
        self.CognomeQuietanzante = CognomeQuietanzante
    def get_NomeQuietanzante(self):
        return self.NomeQuietanzante
    def set_NomeQuietanzante(self, NomeQuietanzante):
        self.NomeQuietanzante = NomeQuietanzante
    def get_CFQuietanzante(self):
        return self.CFQuietanzante
    def set_CFQuietanzante(self, CFQuietanzante):
        self.CFQuietanzante = CFQuietanzante
    def get_TitoloQuietanzante(self):
        return self.TitoloQuietanzante
    def set_TitoloQuietanzante(self, TitoloQuietanzante):
        self.TitoloQuietanzante = TitoloQuietanzante
    def get_IstitutoFinanziario(self):
        return self.IstitutoFinanziario
    def set_IstitutoFinanziario(self, IstitutoFinanziario):
        self.IstitutoFinanziario = IstitutoFinanziario
    def get_IBAN(self):
        return self.IBAN
    def set_IBAN(self, IBAN):
        self.IBAN = IBAN
    def get_ABI(self):
        return self.ABI
    def set_ABI(self, ABI):
        self.ABI = ABI
    def get_CAB(self):
        return self.CAB
    def set_CAB(self, CAB):
        self.CAB = CAB
    def get_BIC(self):
        return self.BIC
    def set_BIC(self, BIC):
        self.BIC = BIC
    def get_ScontoPagamentoAnticipato(self):
        return self.ScontoPagamentoAnticipato
    def set_ScontoPagamentoAnticipato(self, ScontoPagamentoAnticipato):
        self.ScontoPagamentoAnticipato = ScontoPagamentoAnticipato
    def get_DataLimitePagamentoAnticipato(self):
        return self.DataLimitePagamentoAnticipato
    def set_DataLimitePagamentoAnticipato(self, DataLimitePagamentoAnticipato):
        self.DataLimitePagamentoAnticipato = DataLimitePagamentoAnticipato
    def get_PenalitaPagamentiRitardati(self):
        return self.PenalitaPagamentiRitardati
    def set_PenalitaPagamentiRitardati(self, PenalitaPagamentiRitardati):
        self.PenalitaPagamentiRitardati = PenalitaPagamentiRitardati
    def get_DataDecorrenzaPenale(self):
        return self.DataDecorrenzaPenale
    def set_DataDecorrenzaPenale(self, DataDecorrenzaPenale):
        self.DataDecorrenzaPenale = DataDecorrenzaPenale
    def get_CodicePagamento(self):
        return self.CodicePagamento
    def set_CodicePagamento(self, CodicePagamento):
        self.CodicePagamento = CodicePagamento
    def validate_String200LatinType(self, value):
        result = True
        # Validate type String200LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String200LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String200LatinType_patterns_, ))
                result = False
        return result
    validate_String200LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,200})$']]
    def validate_ModalitaPagamentoType(self, value):
        result = True
        # Validate type ModalitaPagamentoType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['MP01', 'MP02', 'MP03', 'MP04', 'MP05', 'MP06', 'MP07', 'MP08', 'MP09', 'MP10', 'MP11', 'MP12', 'MP13', 'MP14', 'MP15', 'MP16', 'MP17', 'MP18', 'MP19', 'MP20', 'MP21', 'MP22']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ModalitaPagamentoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ModalitaPagamentoType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_GiorniTerminePagamentoType(self, value):
        result = True
        # Validate type GiorniTerminePagamentoType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on GiorniTerminePagamentoType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on GiorniTerminePagamentoType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def validate_String60LatinType(self, value):
        result = True
        # Validate type String60LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60LatinType_patterns_, ))
                result = False
        return result
    validate_String60LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,60})$']]
    def validate_CodiceFiscalePFType(self, value):
        result = True
        # Validate type CodiceFiscalePFType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CodiceFiscalePFType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CodiceFiscalePFType_patterns_, ))
                result = False
        return result
    validate_CodiceFiscalePFType_patterns_ = [['^([A-Z0-9]{16})$']]
    def validate_TitoloType(self, value):
        result = True
        # Validate type TitoloType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_TitoloType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_TitoloType_patterns_, ))
                result = False
        return result
    validate_TitoloType_patterns_ = [['^(([\x00-\x7f]{2,10}))$']]
    def validate_String80LatinType(self, value):
        result = True
        # Validate type String80LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String80LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String80LatinType_patterns_, ))
                result = False
        return result
    validate_String80LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,80})$']]
    def validate_IBANType(self, value):
        result = True
        # Validate type IBANType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_IBANType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_IBANType_patterns_, ))
                result = False
        return result
    validate_IBANType_patterns_ = [['^([a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{11,30})$']]
    def validate_ABIType(self, value):
        result = True
        # Validate type ABIType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_ABIType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ABIType_patterns_, ))
                result = False
        return result
    validate_ABIType_patterns_ = [['^([0-9][0-9][0-9][0-9][0-9])$']]
    def validate_CABType(self, value):
        result = True
        # Validate type CABType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CABType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CABType_patterns_, ))
                result = False
        return result
    validate_CABType_patterns_ = [['^([0-9][0-9][0-9][0-9][0-9])$']]
    def validate_BICType(self, value):
        result = True
        # Validate type BICType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_BICType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_BICType_patterns_, ))
                result = False
        return result
    validate_BICType_patterns_ = [['^([A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3}){0,1})$']]
    def validate_String60Type(self, value):
        result = True
        # Validate type String60Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60Type_patterns_, ))
                result = False
        return result
    validate_String60Type_patterns_ = [['^(([\x00-\x7f]{1,60}))$']]
    def _hasContent(self):
        if (
            self.Beneficiario is not None or
            self.ModalitaPagamento is not None or
            self.DataRiferimentoTerminiPagamento is not None or
            self.GiorniTerminiPagamento is not None or
            self.DataScadenzaPagamento is not None or
            self.ImportoPagamento is not None or
            self.CodUfficioPostale is not None or
            self.CognomeQuietanzante is not None or
            self.NomeQuietanzante is not None or
            self.CFQuietanzante is not None or
            self.TitoloQuietanzante is not None or
            self.IstitutoFinanziario is not None or
            self.IBAN is not None or
            self.ABI is not None or
            self.CAB is not None or
            self.BIC is not None or
            self.ScontoPagamentoAnticipato is not None or
            self.DataLimitePagamentoAnticipato is not None or
            self.PenalitaPagamentiRitardati is not None or
            self.DataDecorrenzaPenale is not None or
            self.CodicePagamento is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DettaglioPagamentoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DettaglioPagamentoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DettaglioPagamentoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DettaglioPagamentoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DettaglioPagamentoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DettaglioPagamentoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DettaglioPagamentoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Beneficiario is not None:
            namespaceprefix_ = self.Beneficiario_nsprefix_ + ':' if (UseCapturedNS_ and self.Beneficiario_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBeneficiario>%s</%sBeneficiario>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Beneficiario), input_name='Beneficiario')), namespaceprefix_ , eol_))
        if self.ModalitaPagamento is not None:
            namespaceprefix_ = self.ModalitaPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.ModalitaPagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sModalitaPagamento>%s</%sModalitaPagamento>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ModalitaPagamento), input_name='ModalitaPagamento')), namespaceprefix_ , eol_))
        if self.DataRiferimentoTerminiPagamento is not None:
            namespaceprefix_ = self.DataRiferimentoTerminiPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.DataRiferimentoTerminiPagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataRiferimentoTerminiPagamento>%s</%sDataRiferimentoTerminiPagamento>%s' % (namespaceprefix_ , self.gds_format_date(self.DataRiferimentoTerminiPagamento, input_name='DataRiferimentoTerminiPagamento'), namespaceprefix_ , eol_))
        if self.GiorniTerminiPagamento is not None:
            namespaceprefix_ = self.GiorniTerminiPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.GiorniTerminiPagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGiorniTerminiPagamento>%s</%sGiorniTerminiPagamento>%s' % (namespaceprefix_ , self.gds_format_integer(self.GiorniTerminiPagamento, input_name='GiorniTerminiPagamento'), namespaceprefix_ , eol_))
        if self.DataScadenzaPagamento is not None:
            namespaceprefix_ = self.DataScadenzaPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.DataScadenzaPagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataScadenzaPagamento>%s</%sDataScadenzaPagamento>%s' % (namespaceprefix_ , self.gds_format_date(self.DataScadenzaPagamento, input_name='DataScadenzaPagamento'), namespaceprefix_ , eol_))
        if self.ImportoPagamento is not None:
            namespaceprefix_ = self.ImportoPagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.ImportoPagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImportoPagamento>%s</%sImportoPagamento>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ImportoPagamento, input_name='ImportoPagamento'), namespaceprefix_ , eol_))
        if self.CodUfficioPostale is not None:
            namespaceprefix_ = self.CodUfficioPostale_nsprefix_ + ':' if (UseCapturedNS_ and self.CodUfficioPostale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodUfficioPostale>%s</%sCodUfficioPostale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodUfficioPostale), input_name='CodUfficioPostale')), namespaceprefix_ , eol_))
        if self.CognomeQuietanzante is not None:
            namespaceprefix_ = self.CognomeQuietanzante_nsprefix_ + ':' if (UseCapturedNS_ and self.CognomeQuietanzante_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCognomeQuietanzante>%s</%sCognomeQuietanzante>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CognomeQuietanzante), input_name='CognomeQuietanzante')), namespaceprefix_ , eol_))
        if self.NomeQuietanzante is not None:
            namespaceprefix_ = self.NomeQuietanzante_nsprefix_ + ':' if (UseCapturedNS_ and self.NomeQuietanzante_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNomeQuietanzante>%s</%sNomeQuietanzante>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NomeQuietanzante), input_name='NomeQuietanzante')), namespaceprefix_ , eol_))
        if self.CFQuietanzante is not None:
            namespaceprefix_ = self.CFQuietanzante_nsprefix_ + ':' if (UseCapturedNS_ and self.CFQuietanzante_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCFQuietanzante>%s</%sCFQuietanzante>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CFQuietanzante), input_name='CFQuietanzante')), namespaceprefix_ , eol_))
        if self.TitoloQuietanzante is not None:
            namespaceprefix_ = self.TitoloQuietanzante_nsprefix_ + ':' if (UseCapturedNS_ and self.TitoloQuietanzante_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTitoloQuietanzante>%s</%sTitoloQuietanzante>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TitoloQuietanzante), input_name='TitoloQuietanzante')), namespaceprefix_ , eol_))
        if self.IstitutoFinanziario is not None:
            namespaceprefix_ = self.IstitutoFinanziario_nsprefix_ + ':' if (UseCapturedNS_ and self.IstitutoFinanziario_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIstitutoFinanziario>%s</%sIstitutoFinanziario>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IstitutoFinanziario), input_name='IstitutoFinanziario')), namespaceprefix_ , eol_))
        if self.IBAN is not None:
            namespaceprefix_ = self.IBAN_nsprefix_ + ':' if (UseCapturedNS_ and self.IBAN_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIBAN>%s</%sIBAN>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IBAN), input_name='IBAN')), namespaceprefix_ , eol_))
        if self.ABI is not None:
            namespaceprefix_ = self.ABI_nsprefix_ + ':' if (UseCapturedNS_ and self.ABI_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sABI>%s</%sABI>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ABI), input_name='ABI')), namespaceprefix_ , eol_))
        if self.CAB is not None:
            namespaceprefix_ = self.CAB_nsprefix_ + ':' if (UseCapturedNS_ and self.CAB_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCAB>%s</%sCAB>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CAB), input_name='CAB')), namespaceprefix_ , eol_))
        if self.BIC is not None:
            namespaceprefix_ = self.BIC_nsprefix_ + ':' if (UseCapturedNS_ and self.BIC_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBIC>%s</%sBIC>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BIC), input_name='BIC')), namespaceprefix_ , eol_))
        if self.ScontoPagamentoAnticipato is not None:
            namespaceprefix_ = self.ScontoPagamentoAnticipato_nsprefix_ + ':' if (UseCapturedNS_ and self.ScontoPagamentoAnticipato_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sScontoPagamentoAnticipato>%s</%sScontoPagamentoAnticipato>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ScontoPagamentoAnticipato, input_name='ScontoPagamentoAnticipato'), namespaceprefix_ , eol_))
        if self.DataLimitePagamentoAnticipato is not None:
            namespaceprefix_ = self.DataLimitePagamentoAnticipato_nsprefix_ + ':' if (UseCapturedNS_ and self.DataLimitePagamentoAnticipato_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataLimitePagamentoAnticipato>%s</%sDataLimitePagamentoAnticipato>%s' % (namespaceprefix_ , self.gds_format_date(self.DataLimitePagamentoAnticipato, input_name='DataLimitePagamentoAnticipato'), namespaceprefix_ , eol_))
        if self.PenalitaPagamentiRitardati is not None:
            namespaceprefix_ = self.PenalitaPagamentiRitardati_nsprefix_ + ':' if (UseCapturedNS_ and self.PenalitaPagamentiRitardati_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPenalitaPagamentiRitardati>%s</%sPenalitaPagamentiRitardati>%s' % (namespaceprefix_ , self.gds_format_decimal(self.PenalitaPagamentiRitardati, input_name='PenalitaPagamentiRitardati'), namespaceprefix_ , eol_))
        if self.DataDecorrenzaPenale is not None:
            namespaceprefix_ = self.DataDecorrenzaPenale_nsprefix_ + ':' if (UseCapturedNS_ and self.DataDecorrenzaPenale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataDecorrenzaPenale>%s</%sDataDecorrenzaPenale>%s' % (namespaceprefix_ , self.gds_format_date(self.DataDecorrenzaPenale, input_name='DataDecorrenzaPenale'), namespaceprefix_ , eol_))
        if self.CodicePagamento is not None:
            namespaceprefix_ = self.CodicePagamento_nsprefix_ + ':' if (UseCapturedNS_ and self.CodicePagamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodicePagamento>%s</%sCodicePagamento>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodicePagamento), input_name='CodicePagamento')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Beneficiario':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Beneficiario')
            value_ = self.gds_validate_string(value_, node, 'Beneficiario')
            self.Beneficiario = value_
            self.Beneficiario_nsprefix_ = child_.prefix
            # validate type String200LatinType
            self.validate_String200LatinType(self.Beneficiario)
        elif nodeName_ == 'ModalitaPagamento':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ModalitaPagamento')
            value_ = self.gds_validate_string(value_, node, 'ModalitaPagamento')
            self.ModalitaPagamento = value_
            self.ModalitaPagamento_nsprefix_ = child_.prefix
            # validate type ModalitaPagamentoType
            self.validate_ModalitaPagamentoType(self.ModalitaPagamento)
        elif nodeName_ == 'DataRiferimentoTerminiPagamento':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataRiferimentoTerminiPagamento = dval_
            self.DataRiferimentoTerminiPagamento_nsprefix_ = child_.prefix
        elif nodeName_ == 'GiorniTerminiPagamento' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'GiorniTerminiPagamento')
            ival_ = self.gds_validate_integer(ival_, node, 'GiorniTerminiPagamento')
            self.GiorniTerminiPagamento = ival_
            self.GiorniTerminiPagamento_nsprefix_ = child_.prefix
            # validate type GiorniTerminePagamentoType
            self.validate_GiorniTerminePagamentoType(self.GiorniTerminiPagamento)
        elif nodeName_ == 'DataScadenzaPagamento':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataScadenzaPagamento = dval_
            self.DataScadenzaPagamento_nsprefix_ = child_.prefix
        elif nodeName_ == 'ImportoPagamento' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ImportoPagamento')
            fval_ = self.gds_validate_decimal(fval_, node, 'ImportoPagamento')
            self.ImportoPagamento = fval_
            self.ImportoPagamento_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ImportoPagamento)
        elif nodeName_ == 'CodUfficioPostale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodUfficioPostale')
            value_ = self.gds_validate_string(value_, node, 'CodUfficioPostale')
            self.CodUfficioPostale = value_
            self.CodUfficioPostale_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.CodUfficioPostale)
        elif nodeName_ == 'CognomeQuietanzante':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CognomeQuietanzante')
            value_ = self.gds_validate_string(value_, node, 'CognomeQuietanzante')
            self.CognomeQuietanzante = value_
            self.CognomeQuietanzante_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.CognomeQuietanzante)
        elif nodeName_ == 'NomeQuietanzante':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NomeQuietanzante')
            value_ = self.gds_validate_string(value_, node, 'NomeQuietanzante')
            self.NomeQuietanzante = value_
            self.NomeQuietanzante_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.NomeQuietanzante)
        elif nodeName_ == 'CFQuietanzante':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CFQuietanzante')
            value_ = self.gds_validate_string(value_, node, 'CFQuietanzante')
            self.CFQuietanzante = value_
            self.CFQuietanzante_nsprefix_ = child_.prefix
            # validate type CodiceFiscalePFType
            self.validate_CodiceFiscalePFType(self.CFQuietanzante)
        elif nodeName_ == 'TitoloQuietanzante':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TitoloQuietanzante')
            value_ = self.gds_validate_string(value_, node, 'TitoloQuietanzante')
            self.TitoloQuietanzante = value_
            self.TitoloQuietanzante_nsprefix_ = child_.prefix
            # validate type TitoloType
            self.validate_TitoloType(self.TitoloQuietanzante)
        elif nodeName_ == 'IstitutoFinanziario':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IstitutoFinanziario')
            value_ = self.gds_validate_string(value_, node, 'IstitutoFinanziario')
            self.IstitutoFinanziario = value_
            self.IstitutoFinanziario_nsprefix_ = child_.prefix
            # validate type String80LatinType
            self.validate_String80LatinType(self.IstitutoFinanziario)
        elif nodeName_ == 'IBAN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IBAN')
            value_ = self.gds_validate_string(value_, node, 'IBAN')
            self.IBAN = value_
            self.IBAN_nsprefix_ = child_.prefix
            # validate type IBANType
            self.validate_IBANType(self.IBAN)
        elif nodeName_ == 'ABI':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ABI')
            value_ = self.gds_validate_string(value_, node, 'ABI')
            self.ABI = value_
            self.ABI_nsprefix_ = child_.prefix
            # validate type ABIType
            self.validate_ABIType(self.ABI)
        elif nodeName_ == 'CAB':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CAB')
            value_ = self.gds_validate_string(value_, node, 'CAB')
            self.CAB = value_
            self.CAB_nsprefix_ = child_.prefix
            # validate type CABType
            self.validate_CABType(self.CAB)
        elif nodeName_ == 'BIC':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BIC')
            value_ = self.gds_validate_string(value_, node, 'BIC')
            self.BIC = value_
            self.BIC_nsprefix_ = child_.prefix
            # validate type BICType
            self.validate_BICType(self.BIC)
        elif nodeName_ == 'ScontoPagamentoAnticipato' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ScontoPagamentoAnticipato')
            fval_ = self.gds_validate_decimal(fval_, node, 'ScontoPagamentoAnticipato')
            self.ScontoPagamentoAnticipato = fval_
            self.ScontoPagamentoAnticipato_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ScontoPagamentoAnticipato)
        elif nodeName_ == 'DataLimitePagamentoAnticipato':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataLimitePagamentoAnticipato = dval_
            self.DataLimitePagamentoAnticipato_nsprefix_ = child_.prefix
        elif nodeName_ == 'PenalitaPagamentiRitardati' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'PenalitaPagamentiRitardati')
            fval_ = self.gds_validate_decimal(fval_, node, 'PenalitaPagamentiRitardati')
            self.PenalitaPagamentiRitardati = fval_
            self.PenalitaPagamentiRitardati_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.PenalitaPagamentiRitardati)
        elif nodeName_ == 'DataDecorrenzaPenale':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataDecorrenzaPenale = dval_
            self.DataDecorrenzaPenale_nsprefix_ = child_.prefix
        elif nodeName_ == 'CodicePagamento':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodicePagamento')
            value_ = self.gds_validate_string(value_, node, 'CodicePagamento')
            self.CodicePagamento = value_
            self.CodicePagamento_nsprefix_ = child_.prefix
            # validate type String60Type
            self.validate_String60Type(self.CodicePagamento)
# end class DettaglioPagamentoType


class TerzoIntermediarioSoggettoEmittenteType(GeneratedsSuper):
    """TerzoIntermediarioSoggettoEmittenteType --
    Blocco relativo ai dati del Terzo Intermediario che
    emette fattura elettronica per conto del
    Cedente/Prestatore
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DatiAnagrafici=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DatiAnagrafici = DatiAnagrafici
        self.DatiAnagrafici_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TerzoIntermediarioSoggettoEmittenteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TerzoIntermediarioSoggettoEmittenteType.subclass:
            return TerzoIntermediarioSoggettoEmittenteType.subclass(*args_, **kwargs_)
        else:
            return TerzoIntermediarioSoggettoEmittenteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DatiAnagrafici(self):
        return self.DatiAnagrafici
    def set_DatiAnagrafici(self, DatiAnagrafici):
        self.DatiAnagrafici = DatiAnagrafici
    def _hasContent(self):
        if (
            self.DatiAnagrafici is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='TerzoIntermediarioSoggettoEmittenteType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TerzoIntermediarioSoggettoEmittenteType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TerzoIntermediarioSoggettoEmittenteType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TerzoIntermediarioSoggettoEmittenteType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TerzoIntermediarioSoggettoEmittenteType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TerzoIntermediarioSoggettoEmittenteType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='TerzoIntermediarioSoggettoEmittenteType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DatiAnagrafici is not None:
            namespaceprefix_ = self.DatiAnagrafici_nsprefix_ + ':' if (UseCapturedNS_ and self.DatiAnagrafici_nsprefix_) else ''
            self.DatiAnagrafici.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DatiAnagrafici', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DatiAnagrafici':
            obj_ = DatiAnagraficiTerzoIntermediarioType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DatiAnagrafici = obj_
            obj_.original_tagname_ = 'DatiAnagrafici'
# end class TerzoIntermediarioSoggettoEmittenteType


class DatiAnagraficiTerzoIntermediarioType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdFiscaleIVA=None, CodiceFiscale=None, Anagrafica=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdFiscaleIVA = IdFiscaleIVA
        self.IdFiscaleIVA_nsprefix_ = None
        self.CodiceFiscale = CodiceFiscale
        self.validate_CodiceFiscaleType(self.CodiceFiscale)
        self.CodiceFiscale_nsprefix_ = None
        self.Anagrafica = Anagrafica
        self.Anagrafica_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiAnagraficiTerzoIntermediarioType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiAnagraficiTerzoIntermediarioType.subclass:
            return DatiAnagraficiTerzoIntermediarioType.subclass(*args_, **kwargs_)
        else:
            return DatiAnagraficiTerzoIntermediarioType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdFiscaleIVA(self):
        return self.IdFiscaleIVA
    def set_IdFiscaleIVA(self, IdFiscaleIVA):
        self.IdFiscaleIVA = IdFiscaleIVA
    def get_CodiceFiscale(self):
        return self.CodiceFiscale
    def set_CodiceFiscale(self, CodiceFiscale):
        self.CodiceFiscale = CodiceFiscale
    def get_Anagrafica(self):
        return self.Anagrafica
    def set_Anagrafica(self, Anagrafica):
        self.Anagrafica = Anagrafica
    def validate_CodiceFiscaleType(self, value):
        result = True
        # Validate type CodiceFiscaleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CodiceFiscaleType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CodiceFiscaleType_patterns_, ))
                result = False
        return result
    validate_CodiceFiscaleType_patterns_ = [['^([A-Z0-9]{11,16})$']]
    def _hasContent(self):
        if (
            self.IdFiscaleIVA is not None or
            self.CodiceFiscale is not None or
            self.Anagrafica is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiTerzoIntermediarioType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiAnagraficiTerzoIntermediarioType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiAnagraficiTerzoIntermediarioType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiAnagraficiTerzoIntermediarioType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiAnagraficiTerzoIntermediarioType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiAnagraficiTerzoIntermediarioType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiAnagraficiTerzoIntermediarioType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdFiscaleIVA is not None:
            namespaceprefix_ = self.IdFiscaleIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.IdFiscaleIVA_nsprefix_) else ''
            self.IdFiscaleIVA.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdFiscaleIVA', pretty_print=pretty_print)
        if self.CodiceFiscale is not None:
            namespaceprefix_ = self.CodiceFiscale_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceFiscale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceFiscale>%s</%sCodiceFiscale>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceFiscale), input_name='CodiceFiscale')), namespaceprefix_ , eol_))
        if self.Anagrafica is not None:
            namespaceprefix_ = self.Anagrafica_nsprefix_ + ':' if (UseCapturedNS_ and self.Anagrafica_nsprefix_) else ''
            self.Anagrafica.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Anagrafica', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdFiscaleIVA':
            obj_ = IdFiscaleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdFiscaleIVA = obj_
            obj_.original_tagname_ = 'IdFiscaleIVA'
        elif nodeName_ == 'CodiceFiscale':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceFiscale')
            value_ = self.gds_validate_string(value_, node, 'CodiceFiscale')
            self.CodiceFiscale = value_
            self.CodiceFiscale_nsprefix_ = child_.prefix
            # validate type CodiceFiscaleType
            self.validate_CodiceFiscaleType(self.CodiceFiscale)
        elif nodeName_ == 'Anagrafica':
            obj_ = AnagraficaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Anagrafica = obj_
            obj_.original_tagname_ = 'Anagrafica'
# end class DatiAnagraficiTerzoIntermediarioType


class AllegatiType(GeneratedsSuper):
    """AllegatiType --
    Blocco relativo ai dati di eventuali allegati
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NomeAttachment=None, AlgoritmoCompressione=None, FormatoAttachment=None, DescrizioneAttachment=None, Attachment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NomeAttachment = NomeAttachment
        self.validate_String60LatinType(self.NomeAttachment)
        self.NomeAttachment_nsprefix_ = None
        self.AlgoritmoCompressione = AlgoritmoCompressione
        self.validate_String10Type(self.AlgoritmoCompressione)
        self.AlgoritmoCompressione_nsprefix_ = None
        self.FormatoAttachment = FormatoAttachment
        self.validate_String10Type(self.FormatoAttachment)
        self.FormatoAttachment_nsprefix_ = None
        self.DescrizioneAttachment = DescrizioneAttachment
        self.validate_String100LatinType(self.DescrizioneAttachment)
        self.DescrizioneAttachment_nsprefix_ = None
        self.Attachment = Attachment
        self.Attachment_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AllegatiType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AllegatiType.subclass:
            return AllegatiType.subclass(*args_, **kwargs_)
        else:
            return AllegatiType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NomeAttachment(self):
        return self.NomeAttachment
    def set_NomeAttachment(self, NomeAttachment):
        self.NomeAttachment = NomeAttachment
    def get_AlgoritmoCompressione(self):
        return self.AlgoritmoCompressione
    def set_AlgoritmoCompressione(self, AlgoritmoCompressione):
        self.AlgoritmoCompressione = AlgoritmoCompressione
    def get_FormatoAttachment(self):
        return self.FormatoAttachment
    def set_FormatoAttachment(self, FormatoAttachment):
        self.FormatoAttachment = FormatoAttachment
    def get_DescrizioneAttachment(self):
        return self.DescrizioneAttachment
    def set_DescrizioneAttachment(self, DescrizioneAttachment):
        self.DescrizioneAttachment = DescrizioneAttachment
    def get_Attachment(self):
        return self.Attachment
    def set_Attachment(self, Attachment):
        self.Attachment = Attachment
    def validate_String60LatinType(self, value):
        result = True
        # Validate type String60LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60LatinType_patterns_, ))
                result = False
        return result
    validate_String60LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,60})$']]
    def validate_String10Type(self, value):
        result = True
        # Validate type String10Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String10Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String10Type_patterns_, ))
                result = False
        return result
    validate_String10Type_patterns_ = [['^(([\x00-\x7f]{1,10}))$']]
    def validate_String100LatinType(self, value):
        result = True
        # Validate type String100LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String100LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String100LatinType_patterns_, ))
                result = False
        return result
    validate_String100LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,100})$']]
    def _hasContent(self):
        if (
            self.NomeAttachment is not None or
            self.AlgoritmoCompressione is not None or
            self.FormatoAttachment is not None or
            self.DescrizioneAttachment is not None or
            self.Attachment is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='AllegatiType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AllegatiType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AllegatiType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AllegatiType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AllegatiType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AllegatiType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='AllegatiType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NomeAttachment is not None:
            namespaceprefix_ = self.NomeAttachment_nsprefix_ + ':' if (UseCapturedNS_ and self.NomeAttachment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNomeAttachment>%s</%sNomeAttachment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NomeAttachment), input_name='NomeAttachment')), namespaceprefix_ , eol_))
        if self.AlgoritmoCompressione is not None:
            namespaceprefix_ = self.AlgoritmoCompressione_nsprefix_ + ':' if (UseCapturedNS_ and self.AlgoritmoCompressione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAlgoritmoCompressione>%s</%sAlgoritmoCompressione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AlgoritmoCompressione), input_name='AlgoritmoCompressione')), namespaceprefix_ , eol_))
        if self.FormatoAttachment is not None:
            namespaceprefix_ = self.FormatoAttachment_nsprefix_ + ':' if (UseCapturedNS_ and self.FormatoAttachment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFormatoAttachment>%s</%sFormatoAttachment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FormatoAttachment), input_name='FormatoAttachment')), namespaceprefix_ , eol_))
        if self.DescrizioneAttachment is not None:
            namespaceprefix_ = self.DescrizioneAttachment_nsprefix_ + ':' if (UseCapturedNS_ and self.DescrizioneAttachment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescrizioneAttachment>%s</%sDescrizioneAttachment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DescrizioneAttachment), input_name='DescrizioneAttachment')), namespaceprefix_ , eol_))
        if self.Attachment is not None:
            namespaceprefix_ = self.Attachment_nsprefix_ + ':' if (UseCapturedNS_ and self.Attachment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttachment>%s</%sAttachment>%s' % (namespaceprefix_ , self.gds_format_base64(self.Attachment, input_name='Attachment'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'NomeAttachment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NomeAttachment')
            value_ = self.gds_validate_string(value_, node, 'NomeAttachment')
            self.NomeAttachment = value_
            self.NomeAttachment_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.NomeAttachment)
        elif nodeName_ == 'AlgoritmoCompressione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AlgoritmoCompressione')
            value_ = self.gds_validate_string(value_, node, 'AlgoritmoCompressione')
            self.AlgoritmoCompressione = value_
            self.AlgoritmoCompressione_nsprefix_ = child_.prefix
            # validate type String10Type
            self.validate_String10Type(self.AlgoritmoCompressione)
        elif nodeName_ == 'FormatoAttachment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FormatoAttachment')
            value_ = self.gds_validate_string(value_, node, 'FormatoAttachment')
            self.FormatoAttachment = value_
            self.FormatoAttachment_nsprefix_ = child_.prefix
            # validate type String10Type
            self.validate_String10Type(self.FormatoAttachment)
        elif nodeName_ == 'DescrizioneAttachment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DescrizioneAttachment')
            value_ = self.gds_validate_string(value_, node, 'DescrizioneAttachment')
            self.DescrizioneAttachment = value_
            self.DescrizioneAttachment_nsprefix_ = child_.prefix
            # validate type String100LatinType
            self.validate_String100LatinType(self.DescrizioneAttachment)
        elif nodeName_ == 'Attachment':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Attachment')
            else:
                bval_ = None
            self.Attachment = bval_
            self.Attachment_nsprefix_ = child_.prefix
# end class AllegatiType


class DettaglioLineeType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NumeroLinea=None, TipoCessionePrestazione=None, CodiceArticolo=None, Descrizione=None, Quantita=None, UnitaMisura=None, DataInizioPeriodo=None, DataFinePeriodo=None, PrezzoUnitario=None, ScontoMaggiorazione=None, PrezzoTotale=None, AliquotaIVA=None, Ritenuta=None, Natura=None, RiferimentoAmministrazione=None, AltriDatiGestionali=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NumeroLinea = NumeroLinea
        self.validate_NumeroLineaType(self.NumeroLinea)
        self.NumeroLinea_nsprefix_ = None
        self.TipoCessionePrestazione = TipoCessionePrestazione
        self.validate_TipoCessionePrestazioneType(self.TipoCessionePrestazione)
        self.TipoCessionePrestazione_nsprefix_ = None
        if CodiceArticolo is None:
            self.CodiceArticolo = []
        else:
            self.CodiceArticolo = CodiceArticolo
        self.CodiceArticolo_nsprefix_ = None
        self.Descrizione = Descrizione
        self.validate_String1000LatinType(self.Descrizione)
        self.Descrizione_nsprefix_ = None
        self.Quantita = Quantita
        self.validate_QuantitaType(self.Quantita)
        self.Quantita_nsprefix_ = None
        self.UnitaMisura = UnitaMisura
        self.validate_String10Type(self.UnitaMisura)
        self.UnitaMisura_nsprefix_ = None
        if isinstance(DataInizioPeriodo, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataInizioPeriodo, '%Y-%m-%d').date()
        else:
            initvalue_ = DataInizioPeriodo
        self.DataInizioPeriodo = initvalue_
        self.DataInizioPeriodo_nsprefix_ = None
        if isinstance(DataFinePeriodo, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DataFinePeriodo, '%Y-%m-%d').date()
        else:
            initvalue_ = DataFinePeriodo
        self.DataFinePeriodo = initvalue_
        self.DataFinePeriodo_nsprefix_ = None
        self.PrezzoUnitario = PrezzoUnitario
        self.validate_Amount8DecimalType(self.PrezzoUnitario)
        self.PrezzoUnitario_nsprefix_ = None
        if ScontoMaggiorazione is None:
            self.ScontoMaggiorazione = []
        else:
            self.ScontoMaggiorazione = ScontoMaggiorazione
        self.ScontoMaggiorazione_nsprefix_ = None
        self.PrezzoTotale = PrezzoTotale
        self.validate_Amount8DecimalType(self.PrezzoTotale)
        self.PrezzoTotale_nsprefix_ = None
        self.AliquotaIVA = AliquotaIVA
        self.validate_RateType(self.AliquotaIVA)
        self.AliquotaIVA_nsprefix_ = None
        self.Ritenuta = Ritenuta
        self.validate_RitenutaType(self.Ritenuta)
        self.Ritenuta_nsprefix_ = None
        self.Natura = Natura
        self.validate_NaturaType(self.Natura)
        self.Natura_nsprefix_ = None
        self.RiferimentoAmministrazione = RiferimentoAmministrazione
        self.validate_String20Type(self.RiferimentoAmministrazione)
        self.RiferimentoAmministrazione_nsprefix_ = None
        if AltriDatiGestionali is None:
            self.AltriDatiGestionali = []
        else:
            self.AltriDatiGestionali = AltriDatiGestionali
        self.AltriDatiGestionali_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DettaglioLineeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DettaglioLineeType.subclass:
            return DettaglioLineeType.subclass(*args_, **kwargs_)
        else:
            return DettaglioLineeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NumeroLinea(self):
        return self.NumeroLinea
    def set_NumeroLinea(self, NumeroLinea):
        self.NumeroLinea = NumeroLinea
    def get_TipoCessionePrestazione(self):
        return self.TipoCessionePrestazione
    def set_TipoCessionePrestazione(self, TipoCessionePrestazione):
        self.TipoCessionePrestazione = TipoCessionePrestazione
    def get_CodiceArticolo(self):
        return self.CodiceArticolo
    def set_CodiceArticolo(self, CodiceArticolo):
        self.CodiceArticolo = CodiceArticolo
    def add_CodiceArticolo(self, value):
        self.CodiceArticolo.append(value)
    def insert_CodiceArticolo_at(self, index, value):
        self.CodiceArticolo.insert(index, value)
    def replace_CodiceArticolo_at(self, index, value):
        self.CodiceArticolo[index] = value
    def get_Descrizione(self):
        return self.Descrizione
    def set_Descrizione(self, Descrizione):
        self.Descrizione = Descrizione
    def get_Quantita(self):
        return self.Quantita
    def set_Quantita(self, Quantita):
        self.Quantita = Quantita
    def get_UnitaMisura(self):
        return self.UnitaMisura
    def set_UnitaMisura(self, UnitaMisura):
        self.UnitaMisura = UnitaMisura
    def get_DataInizioPeriodo(self):
        return self.DataInizioPeriodo
    def set_DataInizioPeriodo(self, DataInizioPeriodo):
        self.DataInizioPeriodo = DataInizioPeriodo
    def get_DataFinePeriodo(self):
        return self.DataFinePeriodo
    def set_DataFinePeriodo(self, DataFinePeriodo):
        self.DataFinePeriodo = DataFinePeriodo
    def get_PrezzoUnitario(self):
        return self.PrezzoUnitario
    def set_PrezzoUnitario(self, PrezzoUnitario):
        self.PrezzoUnitario = PrezzoUnitario
    def get_ScontoMaggiorazione(self):
        return self.ScontoMaggiorazione
    def set_ScontoMaggiorazione(self, ScontoMaggiorazione):
        self.ScontoMaggiorazione = ScontoMaggiorazione
    def add_ScontoMaggiorazione(self, value):
        self.ScontoMaggiorazione.append(value)
    def insert_ScontoMaggiorazione_at(self, index, value):
        self.ScontoMaggiorazione.insert(index, value)
    def replace_ScontoMaggiorazione_at(self, index, value):
        self.ScontoMaggiorazione[index] = value
    def get_PrezzoTotale(self):
        return self.PrezzoTotale
    def set_PrezzoTotale(self, PrezzoTotale):
        self.PrezzoTotale = PrezzoTotale
    def get_AliquotaIVA(self):
        return self.AliquotaIVA
    def set_AliquotaIVA(self, AliquotaIVA):
        self.AliquotaIVA = AliquotaIVA
    def get_Ritenuta(self):
        return self.Ritenuta
    def set_Ritenuta(self, Ritenuta):
        self.Ritenuta = Ritenuta
    def get_Natura(self):
        return self.Natura
    def set_Natura(self, Natura):
        self.Natura = Natura
    def get_RiferimentoAmministrazione(self):
        return self.RiferimentoAmministrazione
    def set_RiferimentoAmministrazione(self, RiferimentoAmministrazione):
        self.RiferimentoAmministrazione = RiferimentoAmministrazione
    def get_AltriDatiGestionali(self):
        return self.AltriDatiGestionali
    def set_AltriDatiGestionali(self, AltriDatiGestionali):
        self.AltriDatiGestionali = AltriDatiGestionali
    def add_AltriDatiGestionali(self, value):
        self.AltriDatiGestionali.append(value)
    def insert_AltriDatiGestionali_at(self, index, value):
        self.AltriDatiGestionali.insert(index, value)
    def replace_AltriDatiGestionali_at(self, index, value):
        self.AltriDatiGestionali[index] = value
    def validate_NumeroLineaType(self, value):
        result = True
        # Validate type NumeroLineaType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on NumeroLineaType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on NumeroLineaType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TipoCessionePrestazioneType(self, value):
        result = True
        # Validate type TipoCessionePrestazioneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SC', 'PR', 'AB', 'AC']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TipoCessionePrestazioneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on TipoCessionePrestazioneType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_String1000LatinType(self, value):
        result = True
        # Validate type String1000LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String1000LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String1000LatinType_patterns_, ))
                result = False
        return result
    validate_String1000LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,1000})$']]
    def validate_QuantitaType(self, value):
        result = True
        # Validate type QuantitaType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_QuantitaType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_QuantitaType_patterns_, ))
                result = False
        return result
    validate_QuantitaType_patterns_ = [['^([0-9]{1,12}\\.[0-9]{2,8})$']]
    def validate_String10Type(self, value):
        result = True
        # Validate type String10Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String10Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String10Type_patterns_, ))
                result = False
        return result
    validate_String10Type_patterns_ = [['^(([\x00-\x7f]{1,10}))$']]
    def validate_Amount8DecimalType(self, value):
        result = True
        # Validate type Amount8DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount8DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount8DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount8DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2,8})$']]
    def validate_RateType(self, value):
        result = True
        # Validate type RateType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 100.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RateType' % {"value": value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_RateType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RateType_patterns_, ))
                result = False
        return result
    validate_RateType_patterns_ = [['^([0-9]{1,3}\\.[0-9]{2})$']]
    def validate_RitenutaType(self, value):
        result = True
        # Validate type RitenutaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SI']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on RitenutaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on RitenutaType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_NaturaType(self, value):
        result = True
        # Validate type NaturaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NaturaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_String20Type(self, value):
        result = True
        # Validate type String20Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String20Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String20Type_patterns_, ))
                result = False
        return result
    validate_String20Type_patterns_ = [['^(([\x00-\x7f]{1,20}))$']]
    def _hasContent(self):
        if (
            self.NumeroLinea is not None or
            self.TipoCessionePrestazione is not None or
            self.CodiceArticolo or
            self.Descrizione is not None or
            self.Quantita is not None or
            self.UnitaMisura is not None or
            self.DataInizioPeriodo is not None or
            self.DataFinePeriodo is not None or
            self.PrezzoUnitario is not None or
            self.ScontoMaggiorazione or
            self.PrezzoTotale is not None or
            self.AliquotaIVA is not None or
            self.Ritenuta is not None or
            self.Natura is not None or
            self.RiferimentoAmministrazione is not None or
            self.AltriDatiGestionali
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DettaglioLineeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DettaglioLineeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DettaglioLineeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DettaglioLineeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DettaglioLineeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DettaglioLineeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DettaglioLineeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NumeroLinea is not None:
            namespaceprefix_ = self.NumeroLinea_nsprefix_ + ':' if (UseCapturedNS_ and self.NumeroLinea_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumeroLinea>%s</%sNumeroLinea>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumeroLinea, input_name='NumeroLinea'), namespaceprefix_ , eol_))
        if self.TipoCessionePrestazione is not None:
            namespaceprefix_ = self.TipoCessionePrestazione_nsprefix_ + ':' if (UseCapturedNS_ and self.TipoCessionePrestazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTipoCessionePrestazione>%s</%sTipoCessionePrestazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TipoCessionePrestazione), input_name='TipoCessionePrestazione')), namespaceprefix_ , eol_))
        for CodiceArticolo_ in self.CodiceArticolo:
            namespaceprefix_ = self.CodiceArticolo_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceArticolo_nsprefix_) else ''
            CodiceArticolo_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CodiceArticolo', pretty_print=pretty_print)
        if self.Descrizione is not None:
            namespaceprefix_ = self.Descrizione_nsprefix_ + ':' if (UseCapturedNS_ and self.Descrizione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescrizione>%s</%sDescrizione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Descrizione), input_name='Descrizione')), namespaceprefix_ , eol_))
        if self.Quantita is not None:
            namespaceprefix_ = self.Quantita_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantita_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantita>%s</%sQuantita>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Quantita, input_name='Quantita'), namespaceprefix_ , eol_))
        if self.UnitaMisura is not None:
            namespaceprefix_ = self.UnitaMisura_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitaMisura_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnitaMisura>%s</%sUnitaMisura>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UnitaMisura), input_name='UnitaMisura')), namespaceprefix_ , eol_))
        if self.DataInizioPeriodo is not None:
            namespaceprefix_ = self.DataInizioPeriodo_nsprefix_ + ':' if (UseCapturedNS_ and self.DataInizioPeriodo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataInizioPeriodo>%s</%sDataInizioPeriodo>%s' % (namespaceprefix_ , self.gds_format_date(self.DataInizioPeriodo, input_name='DataInizioPeriodo'), namespaceprefix_ , eol_))
        if self.DataFinePeriodo is not None:
            namespaceprefix_ = self.DataFinePeriodo_nsprefix_ + ':' if (UseCapturedNS_ and self.DataFinePeriodo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataFinePeriodo>%s</%sDataFinePeriodo>%s' % (namespaceprefix_ , self.gds_format_date(self.DataFinePeriodo, input_name='DataFinePeriodo'), namespaceprefix_ , eol_))
        if self.PrezzoUnitario is not None:
            namespaceprefix_ = self.PrezzoUnitario_nsprefix_ + ':' if (UseCapturedNS_ and self.PrezzoUnitario_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrezzoUnitario>%s</%sPrezzoUnitario>%s' % (namespaceprefix_ , self.gds_format_decimal(self.PrezzoUnitario, input_name='PrezzoUnitario'), namespaceprefix_ , eol_))
        for ScontoMaggiorazione_ in self.ScontoMaggiorazione:
            namespaceprefix_ = self.ScontoMaggiorazione_nsprefix_ + ':' if (UseCapturedNS_ and self.ScontoMaggiorazione_nsprefix_) else ''
            ScontoMaggiorazione_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ScontoMaggiorazione', pretty_print=pretty_print)
        if self.PrezzoTotale is not None:
            namespaceprefix_ = self.PrezzoTotale_nsprefix_ + ':' if (UseCapturedNS_ and self.PrezzoTotale_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrezzoTotale>%s</%sPrezzoTotale>%s' % (namespaceprefix_ , self.gds_format_decimal(self.PrezzoTotale, input_name='PrezzoTotale'), namespaceprefix_ , eol_))
        if self.AliquotaIVA is not None:
            namespaceprefix_ = self.AliquotaIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.AliquotaIVA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAliquotaIVA>%s</%sAliquotaIVA>%s' % (namespaceprefix_ , self.gds_format_decimal(self.AliquotaIVA, input_name='AliquotaIVA'), namespaceprefix_ , eol_))
        if self.Ritenuta is not None:
            namespaceprefix_ = self.Ritenuta_nsprefix_ + ':' if (UseCapturedNS_ and self.Ritenuta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRitenuta>%s</%sRitenuta>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Ritenuta), input_name='Ritenuta')), namespaceprefix_ , eol_))
        if self.Natura is not None:
            namespaceprefix_ = self.Natura_nsprefix_ + ':' if (UseCapturedNS_ and self.Natura_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNatura>%s</%sNatura>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Natura), input_name='Natura')), namespaceprefix_ , eol_))
        if self.RiferimentoAmministrazione is not None:
            namespaceprefix_ = self.RiferimentoAmministrazione_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoAmministrazione_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoAmministrazione>%s</%sRiferimentoAmministrazione>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RiferimentoAmministrazione), input_name='RiferimentoAmministrazione')), namespaceprefix_ , eol_))
        for AltriDatiGestionali_ in self.AltriDatiGestionali:
            namespaceprefix_ = self.AltriDatiGestionali_nsprefix_ + ':' if (UseCapturedNS_ and self.AltriDatiGestionali_nsprefix_) else ''
            AltriDatiGestionali_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AltriDatiGestionali', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'NumeroLinea' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumeroLinea')
            ival_ = self.gds_validate_integer(ival_, node, 'NumeroLinea')
            self.NumeroLinea = ival_
            self.NumeroLinea_nsprefix_ = child_.prefix
            # validate type NumeroLineaType
            self.validate_NumeroLineaType(self.NumeroLinea)
        elif nodeName_ == 'TipoCessionePrestazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TipoCessionePrestazione')
            value_ = self.gds_validate_string(value_, node, 'TipoCessionePrestazione')
            self.TipoCessionePrestazione = value_
            self.TipoCessionePrestazione_nsprefix_ = child_.prefix
            # validate type TipoCessionePrestazioneType
            self.validate_TipoCessionePrestazioneType(self.TipoCessionePrestazione)
        elif nodeName_ == 'CodiceArticolo':
            obj_ = CodiceArticoloType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CodiceArticolo.append(obj_)
            obj_.original_tagname_ = 'CodiceArticolo'
        elif nodeName_ == 'Descrizione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Descrizione')
            value_ = self.gds_validate_string(value_, node, 'Descrizione')
            self.Descrizione = value_
            self.Descrizione_nsprefix_ = child_.prefix
            # validate type String1000LatinType
            self.validate_String1000LatinType(self.Descrizione)
        elif nodeName_ == 'Quantita' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Quantita')
            fval_ = self.gds_validate_decimal(fval_, node, 'Quantita')
            self.Quantita = fval_
            self.Quantita_nsprefix_ = child_.prefix
            # validate type QuantitaType
            self.validate_QuantitaType(self.Quantita)
        elif nodeName_ == 'UnitaMisura':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UnitaMisura')
            value_ = self.gds_validate_string(value_, node, 'UnitaMisura')
            self.UnitaMisura = value_
            self.UnitaMisura_nsprefix_ = child_.prefix
            # validate type String10Type
            self.validate_String10Type(self.UnitaMisura)
        elif nodeName_ == 'DataInizioPeriodo':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataInizioPeriodo = dval_
            self.DataInizioPeriodo_nsprefix_ = child_.prefix
        elif nodeName_ == 'DataFinePeriodo':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DataFinePeriodo = dval_
            self.DataFinePeriodo_nsprefix_ = child_.prefix
        elif nodeName_ == 'PrezzoUnitario' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'PrezzoUnitario')
            fval_ = self.gds_validate_decimal(fval_, node, 'PrezzoUnitario')
            self.PrezzoUnitario = fval_
            self.PrezzoUnitario_nsprefix_ = child_.prefix
            # validate type Amount8DecimalType
            self.validate_Amount8DecimalType(self.PrezzoUnitario)
        elif nodeName_ == 'ScontoMaggiorazione':
            obj_ = ScontoMaggiorazioneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ScontoMaggiorazione.append(obj_)
            obj_.original_tagname_ = 'ScontoMaggiorazione'
        elif nodeName_ == 'PrezzoTotale' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'PrezzoTotale')
            fval_ = self.gds_validate_decimal(fval_, node, 'PrezzoTotale')
            self.PrezzoTotale = fval_
            self.PrezzoTotale_nsprefix_ = child_.prefix
            # validate type Amount8DecimalType
            self.validate_Amount8DecimalType(self.PrezzoTotale)
        elif nodeName_ == 'AliquotaIVA' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'AliquotaIVA')
            fval_ = self.gds_validate_decimal(fval_, node, 'AliquotaIVA')
            self.AliquotaIVA = fval_
            self.AliquotaIVA_nsprefix_ = child_.prefix
            # validate type RateType
            self.validate_RateType(self.AliquotaIVA)
        elif nodeName_ == 'Ritenuta':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Ritenuta')
            value_ = self.gds_validate_string(value_, node, 'Ritenuta')
            self.Ritenuta = value_
            self.Ritenuta_nsprefix_ = child_.prefix
            # validate type RitenutaType
            self.validate_RitenutaType(self.Ritenuta)
        elif nodeName_ == 'Natura':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Natura')
            value_ = self.gds_validate_string(value_, node, 'Natura')
            self.Natura = value_
            self.Natura_nsprefix_ = child_.prefix
            # validate type NaturaType
            self.validate_NaturaType(self.Natura)
        elif nodeName_ == 'RiferimentoAmministrazione':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RiferimentoAmministrazione')
            value_ = self.gds_validate_string(value_, node, 'RiferimentoAmministrazione')
            self.RiferimentoAmministrazione = value_
            self.RiferimentoAmministrazione_nsprefix_ = child_.prefix
            # validate type String20Type
            self.validate_String20Type(self.RiferimentoAmministrazione)
        elif nodeName_ == 'AltriDatiGestionali':
            obj_ = AltriDatiGestionaliType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AltriDatiGestionali.append(obj_)
            obj_.original_tagname_ = 'AltriDatiGestionali'
# end class DettaglioLineeType


class CodiceArticoloType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CodiceTipo=None, CodiceValore=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CodiceTipo = CodiceTipo
        self.validate_String35Type(self.CodiceTipo)
        self.CodiceTipo_nsprefix_ = None
        self.CodiceValore = CodiceValore
        self.validate_String35Type(self.CodiceValore)
        self.CodiceValore_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CodiceArticoloType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CodiceArticoloType.subclass:
            return CodiceArticoloType.subclass(*args_, **kwargs_)
        else:
            return CodiceArticoloType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CodiceTipo(self):
        return self.CodiceTipo
    def set_CodiceTipo(self, CodiceTipo):
        self.CodiceTipo = CodiceTipo
    def get_CodiceValore(self):
        return self.CodiceValore
    def set_CodiceValore(self, CodiceValore):
        self.CodiceValore = CodiceValore
    def validate_String35Type(self, value):
        result = True
        # Validate type String35Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String35Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String35Type_patterns_, ))
                result = False
        return result
    validate_String35Type_patterns_ = [['^(([\x00-\x7f]{1,35}))$']]
    def _hasContent(self):
        if (
            self.CodiceTipo is not None or
            self.CodiceValore is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CodiceArticoloType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CodiceArticoloType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CodiceArticoloType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CodiceArticoloType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CodiceArticoloType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CodiceArticoloType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CodiceArticoloType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CodiceTipo is not None:
            namespaceprefix_ = self.CodiceTipo_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceTipo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceTipo>%s</%sCodiceTipo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceTipo), input_name='CodiceTipo')), namespaceprefix_ , eol_))
        if self.CodiceValore is not None:
            namespaceprefix_ = self.CodiceValore_nsprefix_ + ':' if (UseCapturedNS_ and self.CodiceValore_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodiceValore>%s</%sCodiceValore>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodiceValore), input_name='CodiceValore')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CodiceTipo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceTipo')
            value_ = self.gds_validate_string(value_, node, 'CodiceTipo')
            self.CodiceTipo = value_
            self.CodiceTipo_nsprefix_ = child_.prefix
            # validate type String35Type
            self.validate_String35Type(self.CodiceTipo)
        elif nodeName_ == 'CodiceValore':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodiceValore')
            value_ = self.gds_validate_string(value_, node, 'CodiceValore')
            self.CodiceValore = value_
            self.CodiceValore_nsprefix_ = child_.prefix
            # validate type String35Type
            self.validate_String35Type(self.CodiceValore)
# end class CodiceArticoloType


class AltriDatiGestionaliType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TipoDato=None, RiferimentoTesto=None, RiferimentoNumero=None, RiferimentoData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TipoDato = TipoDato
        self.validate_String10Type(self.TipoDato)
        self.TipoDato_nsprefix_ = None
        self.RiferimentoTesto = RiferimentoTesto
        self.validate_String60LatinType(self.RiferimentoTesto)
        self.RiferimentoTesto_nsprefix_ = None
        self.RiferimentoNumero = RiferimentoNumero
        self.validate_Amount8DecimalType(self.RiferimentoNumero)
        self.RiferimentoNumero_nsprefix_ = None
        if isinstance(RiferimentoData, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(RiferimentoData, '%Y-%m-%d').date()
        else:
            initvalue_ = RiferimentoData
        self.RiferimentoData = initvalue_
        self.RiferimentoData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AltriDatiGestionaliType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AltriDatiGestionaliType.subclass:
            return AltriDatiGestionaliType.subclass(*args_, **kwargs_)
        else:
            return AltriDatiGestionaliType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TipoDato(self):
        return self.TipoDato
    def set_TipoDato(self, TipoDato):
        self.TipoDato = TipoDato
    def get_RiferimentoTesto(self):
        return self.RiferimentoTesto
    def set_RiferimentoTesto(self, RiferimentoTesto):
        self.RiferimentoTesto = RiferimentoTesto
    def get_RiferimentoNumero(self):
        return self.RiferimentoNumero
    def set_RiferimentoNumero(self, RiferimentoNumero):
        self.RiferimentoNumero = RiferimentoNumero
    def get_RiferimentoData(self):
        return self.RiferimentoData
    def set_RiferimentoData(self, RiferimentoData):
        self.RiferimentoData = RiferimentoData
    def validate_String10Type(self, value):
        result = True
        # Validate type String10Type, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String10Type_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String10Type_patterns_, ))
                result = False
        return result
    validate_String10Type_patterns_ = [['^(([\x00-\x7f]{1,10}))$']]
    def validate_String60LatinType(self, value):
        result = True
        # Validate type String60LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String60LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String60LatinType_patterns_, ))
                result = False
        return result
    validate_String60LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,60})$']]
    def validate_Amount8DecimalType(self, value):
        result = True
        # Validate type Amount8DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount8DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount8DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount8DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2,8})$']]
    def _hasContent(self):
        if (
            self.TipoDato is not None or
            self.RiferimentoTesto is not None or
            self.RiferimentoNumero is not None or
            self.RiferimentoData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='AltriDatiGestionaliType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AltriDatiGestionaliType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AltriDatiGestionaliType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AltriDatiGestionaliType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AltriDatiGestionaliType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AltriDatiGestionaliType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='AltriDatiGestionaliType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TipoDato is not None:
            namespaceprefix_ = self.TipoDato_nsprefix_ + ':' if (UseCapturedNS_ and self.TipoDato_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTipoDato>%s</%sTipoDato>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TipoDato), input_name='TipoDato')), namespaceprefix_ , eol_))
        if self.RiferimentoTesto is not None:
            namespaceprefix_ = self.RiferimentoTesto_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoTesto_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoTesto>%s</%sRiferimentoTesto>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RiferimentoTesto), input_name='RiferimentoTesto')), namespaceprefix_ , eol_))
        if self.RiferimentoNumero is not None:
            namespaceprefix_ = self.RiferimentoNumero_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoNumero_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoNumero>%s</%sRiferimentoNumero>%s' % (namespaceprefix_ , self.gds_format_decimal(self.RiferimentoNumero, input_name='RiferimentoNumero'), namespaceprefix_ , eol_))
        if self.RiferimentoData is not None:
            namespaceprefix_ = self.RiferimentoData_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoData>%s</%sRiferimentoData>%s' % (namespaceprefix_ , self.gds_format_date(self.RiferimentoData, input_name='RiferimentoData'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TipoDato':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TipoDato')
            value_ = self.gds_validate_string(value_, node, 'TipoDato')
            self.TipoDato = value_
            self.TipoDato_nsprefix_ = child_.prefix
            # validate type String10Type
            self.validate_String10Type(self.TipoDato)
        elif nodeName_ == 'RiferimentoTesto':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RiferimentoTesto')
            value_ = self.gds_validate_string(value_, node, 'RiferimentoTesto')
            self.RiferimentoTesto = value_
            self.RiferimentoTesto_nsprefix_ = child_.prefix
            # validate type String60LatinType
            self.validate_String60LatinType(self.RiferimentoTesto)
        elif nodeName_ == 'RiferimentoNumero' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'RiferimentoNumero')
            fval_ = self.gds_validate_decimal(fval_, node, 'RiferimentoNumero')
            self.RiferimentoNumero = fval_
            self.RiferimentoNumero_nsprefix_ = child_.prefix
            # validate type Amount8DecimalType
            self.validate_Amount8DecimalType(self.RiferimentoNumero)
        elif nodeName_ == 'RiferimentoData':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.RiferimentoData = dval_
            self.RiferimentoData_nsprefix_ = child_.prefix
# end class AltriDatiGestionaliType


class DatiRiepilogoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AliquotaIVA=None, Natura=None, SpeseAccessorie=None, Arrotondamento=None, ImponibileImporto=None, Imposta=None, EsigibilitaIVA=None, RiferimentoNormativo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AliquotaIVA = AliquotaIVA
        self.validate_RateType(self.AliquotaIVA)
        self.AliquotaIVA_nsprefix_ = None
        self.Natura = Natura
        self.validate_NaturaType(self.Natura)
        self.Natura_nsprefix_ = None
        self.SpeseAccessorie = SpeseAccessorie
        self.validate_Amount2DecimalType(self.SpeseAccessorie)
        self.SpeseAccessorie_nsprefix_ = None
        self.Arrotondamento = Arrotondamento
        self.validate_Amount8DecimalType(self.Arrotondamento)
        self.Arrotondamento_nsprefix_ = None
        self.ImponibileImporto = ImponibileImporto
        self.validate_Amount2DecimalType(self.ImponibileImporto)
        self.ImponibileImporto_nsprefix_ = None
        self.Imposta = Imposta
        self.validate_Amount2DecimalType(self.Imposta)
        self.Imposta_nsprefix_ = None
        self.EsigibilitaIVA = EsigibilitaIVA
        self.validate_EsigibilitaIVAType(self.EsigibilitaIVA)
        self.EsigibilitaIVA_nsprefix_ = None
        self.RiferimentoNormativo = RiferimentoNormativo
        self.validate_String100LatinType(self.RiferimentoNormativo)
        self.RiferimentoNormativo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DatiRiepilogoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DatiRiepilogoType.subclass:
            return DatiRiepilogoType.subclass(*args_, **kwargs_)
        else:
            return DatiRiepilogoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AliquotaIVA(self):
        return self.AliquotaIVA
    def set_AliquotaIVA(self, AliquotaIVA):
        self.AliquotaIVA = AliquotaIVA
    def get_Natura(self):
        return self.Natura
    def set_Natura(self, Natura):
        self.Natura = Natura
    def get_SpeseAccessorie(self):
        return self.SpeseAccessorie
    def set_SpeseAccessorie(self, SpeseAccessorie):
        self.SpeseAccessorie = SpeseAccessorie
    def get_Arrotondamento(self):
        return self.Arrotondamento
    def set_Arrotondamento(self, Arrotondamento):
        self.Arrotondamento = Arrotondamento
    def get_ImponibileImporto(self):
        return self.ImponibileImporto
    def set_ImponibileImporto(self, ImponibileImporto):
        self.ImponibileImporto = ImponibileImporto
    def get_Imposta(self):
        return self.Imposta
    def set_Imposta(self, Imposta):
        self.Imposta = Imposta
    def get_EsigibilitaIVA(self):
        return self.EsigibilitaIVA
    def set_EsigibilitaIVA(self, EsigibilitaIVA):
        self.EsigibilitaIVA = EsigibilitaIVA
    def get_RiferimentoNormativo(self):
        return self.RiferimentoNormativo
    def set_RiferimentoNormativo(self, RiferimentoNormativo):
        self.RiferimentoNormativo = RiferimentoNormativo
    def validate_RateType(self, value):
        result = True
        # Validate type RateType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 100.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on RateType' % {"value": value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_RateType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RateType_patterns_, ))
                result = False
        return result
    validate_RateType_patterns_ = [['^([0-9]{1,3}\\.[0-9]{2})$']]
    def validate_NaturaType(self, value):
        result = True
        # Validate type NaturaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NaturaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Amount2DecimalType(self, value):
        result = True
        # Validate type Amount2DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount2DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount2DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount2DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2})$']]
    def validate_Amount8DecimalType(self, value):
        result = True
        # Validate type Amount8DecimalType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_Amount8DecimalType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_Amount8DecimalType_patterns_, ))
                result = False
        return result
    validate_Amount8DecimalType_patterns_ = [['^([\\-]?[0-9]{1,11}\\.[0-9]{2,8})$']]
    def validate_EsigibilitaIVAType(self, value):
        result = True
        # Validate type EsigibilitaIVAType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['D', 'I', 'S']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on EsigibilitaIVAType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EsigibilitaIVAType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on EsigibilitaIVAType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_String100LatinType(self, value):
        result = True
        # Validate type String100LatinType, a restriction on xs:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_String100LatinType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_String100LatinType_patterns_, ))
                result = False
        return result
    validate_String100LatinType_patterns_ = [['^([\x00-\x7f\x80-ÿ]{1,100})$']]
    def _hasContent(self):
        if (
            self.AliquotaIVA is not None or
            self.Natura is not None or
            self.SpeseAccessorie is not None or
            self.Arrotondamento is not None or
            self.ImponibileImporto is not None or
            self.Imposta is not None or
            self.EsigibilitaIVA is not None or
            self.RiferimentoNormativo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiRiepilogoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DatiRiepilogoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DatiRiepilogoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DatiRiepilogoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DatiRiepilogoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DatiRiepilogoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DatiRiepilogoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AliquotaIVA is not None:
            namespaceprefix_ = self.AliquotaIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.AliquotaIVA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAliquotaIVA>%s</%sAliquotaIVA>%s' % (namespaceprefix_ , self.gds_format_decimal(self.AliquotaIVA, input_name='AliquotaIVA'), namespaceprefix_ , eol_))
        if self.Natura is not None:
            namespaceprefix_ = self.Natura_nsprefix_ + ':' if (UseCapturedNS_ and self.Natura_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNatura>%s</%sNatura>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Natura), input_name='Natura')), namespaceprefix_ , eol_))
        if self.SpeseAccessorie is not None:
            namespaceprefix_ = self.SpeseAccessorie_nsprefix_ + ':' if (UseCapturedNS_ and self.SpeseAccessorie_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpeseAccessorie>%s</%sSpeseAccessorie>%s' % (namespaceprefix_ , self.gds_format_decimal(self.SpeseAccessorie, input_name='SpeseAccessorie'), namespaceprefix_ , eol_))
        if self.Arrotondamento is not None:
            namespaceprefix_ = self.Arrotondamento_nsprefix_ + ':' if (UseCapturedNS_ and self.Arrotondamento_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sArrotondamento>%s</%sArrotondamento>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Arrotondamento, input_name='Arrotondamento'), namespaceprefix_ , eol_))
        if self.ImponibileImporto is not None:
            namespaceprefix_ = self.ImponibileImporto_nsprefix_ + ':' if (UseCapturedNS_ and self.ImponibileImporto_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImponibileImporto>%s</%sImponibileImporto>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ImponibileImporto, input_name='ImponibileImporto'), namespaceprefix_ , eol_))
        if self.Imposta is not None:
            namespaceprefix_ = self.Imposta_nsprefix_ + ':' if (UseCapturedNS_ and self.Imposta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImposta>%s</%sImposta>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Imposta, input_name='Imposta'), namespaceprefix_ , eol_))
        if self.EsigibilitaIVA is not None:
            namespaceprefix_ = self.EsigibilitaIVA_nsprefix_ + ':' if (UseCapturedNS_ and self.EsigibilitaIVA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEsigibilitaIVA>%s</%sEsigibilitaIVA>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EsigibilitaIVA), input_name='EsigibilitaIVA')), namespaceprefix_ , eol_))
        if self.RiferimentoNormativo is not None:
            namespaceprefix_ = self.RiferimentoNormativo_nsprefix_ + ':' if (UseCapturedNS_ and self.RiferimentoNormativo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRiferimentoNormativo>%s</%sRiferimentoNormativo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RiferimentoNormativo), input_name='RiferimentoNormativo')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AliquotaIVA' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'AliquotaIVA')
            fval_ = self.gds_validate_decimal(fval_, node, 'AliquotaIVA')
            self.AliquotaIVA = fval_
            self.AliquotaIVA_nsprefix_ = child_.prefix
            # validate type RateType
            self.validate_RateType(self.AliquotaIVA)
        elif nodeName_ == 'Natura':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Natura')
            value_ = self.gds_validate_string(value_, node, 'Natura')
            self.Natura = value_
            self.Natura_nsprefix_ = child_.prefix
            # validate type NaturaType
            self.validate_NaturaType(self.Natura)
        elif nodeName_ == 'SpeseAccessorie' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'SpeseAccessorie')
            fval_ = self.gds_validate_decimal(fval_, node, 'SpeseAccessorie')
            self.SpeseAccessorie = fval_
            self.SpeseAccessorie_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.SpeseAccessorie)
        elif nodeName_ == 'Arrotondamento' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Arrotondamento')
            fval_ = self.gds_validate_decimal(fval_, node, 'Arrotondamento')
            self.Arrotondamento = fval_
            self.Arrotondamento_nsprefix_ = child_.prefix
            # validate type Amount8DecimalType
            self.validate_Amount8DecimalType(self.Arrotondamento)
        elif nodeName_ == 'ImponibileImporto' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ImponibileImporto')
            fval_ = self.gds_validate_decimal(fval_, node, 'ImponibileImporto')
            self.ImponibileImporto = fval_
            self.ImponibileImporto_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.ImponibileImporto)
        elif nodeName_ == 'Imposta' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Imposta')
            fval_ = self.gds_validate_decimal(fval_, node, 'Imposta')
            self.Imposta = fval_
            self.Imposta_nsprefix_ = child_.prefix
            # validate type Amount2DecimalType
            self.validate_Amount2DecimalType(self.Imposta)
        elif nodeName_ == 'EsigibilitaIVA':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EsigibilitaIVA')
            value_ = self.gds_validate_string(value_, node, 'EsigibilitaIVA')
            self.EsigibilitaIVA = value_
            self.EsigibilitaIVA_nsprefix_ = child_.prefix
            # validate type EsigibilitaIVAType
            self.validate_EsigibilitaIVAType(self.EsigibilitaIVA)
        elif nodeName_ == 'RiferimentoNormativo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RiferimentoNormativo')
            value_ = self.gds_validate_string(value_, node, 'RiferimentoNormativo')
            self.RiferimentoNormativo = value_
            self.RiferimentoNormativo_nsprefix_ = child_.prefix
            # validate type String100LatinType
            self.validate_String100LatinType(self.RiferimentoNormativo)
# end class DatiRiepilogoType


class SignatureType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, SignedInfo=None, SignatureValue=None, KeyInfo=None, Object=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        self.SignedInfo = SignedInfo
        self.SignedInfo_nsprefix_ = "ds"
        self.SignatureValue = SignatureValue
        self.SignatureValue_nsprefix_ = "ds"
        self.KeyInfo = KeyInfo
        self.KeyInfo_nsprefix_ = "ds"
        if Object is None:
            self.Object = []
        else:
            self.Object = Object
        self.Object_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SignatureType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignatureType.subclass:
            return SignatureType.subclass(*args_, **kwargs_)
        else:
            return SignatureType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SignedInfo(self):
        return self.SignedInfo
    def set_SignedInfo(self, SignedInfo):
        self.SignedInfo = SignedInfo
    def get_SignatureValue(self):
        return self.SignatureValue
    def set_SignatureValue(self, SignatureValue):
        self.SignatureValue = SignatureValue
    def get_KeyInfo(self):
        return self.KeyInfo
    def set_KeyInfo(self, KeyInfo):
        self.KeyInfo = KeyInfo
    def get_Object(self):
        return self.Object
    def set_Object(self, Object):
        self.Object = Object
    def add_Object(self, value):
        self.Object.append(value)
    def insert_Object_at(self, index, value):
        self.Object.insert(index, value)
    def replace_Object_at(self, index, value):
        self.Object[index] = value
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def _hasContent(self):
        if (
            self.SignedInfo is not None or
            self.SignatureValue is not None or
            self.KeyInfo is not None or
            self.Object
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignatureType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignatureType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignatureType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignatureType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignatureType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='SignatureType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignatureType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SignedInfo is not None:
            namespaceprefix_ = self.SignedInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.SignedInfo_nsprefix_) else ''
            self.SignedInfo.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='SignedInfo', pretty_print=pretty_print)
        if self.SignatureValue is not None:
            namespaceprefix_ = self.SignatureValue_nsprefix_ + ':' if (UseCapturedNS_ and self.SignatureValue_nsprefix_) else ''
            self.SignatureValue.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='SignatureValue', pretty_print=pretty_print)
        if self.KeyInfo is not None:
            namespaceprefix_ = self.KeyInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.KeyInfo_nsprefix_) else ''
            self.KeyInfo.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='KeyInfo', pretty_print=pretty_print)
        for Object_ in self.Object:
            namespaceprefix_ = self.Object_nsprefix_ + ':' if (UseCapturedNS_ and self.Object_nsprefix_) else ''
            Object_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='Object', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SignedInfo':
            obj_ = SignedInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SignedInfo = obj_
            obj_.original_tagname_ = 'SignedInfo'
        elif nodeName_ == 'SignatureValue':
            obj_ = SignatureValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SignatureValue = obj_
            obj_.original_tagname_ = 'SignatureValue'
        elif nodeName_ == 'KeyInfo':
            obj_ = KeyInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.KeyInfo = obj_
            obj_.original_tagname_ = 'KeyInfo'
        elif nodeName_ == 'Object':
            obj_ = ObjectType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Object.append(obj_)
            obj_.original_tagname_ = 'Object'
# end class SignatureType


class SignatureValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SignatureValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignatureValueType.subclass:
            return SignatureValueType.subclass(*args_, **kwargs_)
        else:
            return SignatureValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignatureValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignatureValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignatureValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignatureValueType')
        if self._hasContent():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignatureValueType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='SignatureValueType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignatureValueType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class SignatureValueType


class SignedInfoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, CanonicalizationMethod=None, SignatureMethod=None, Reference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        self.CanonicalizationMethod = CanonicalizationMethod
        self.CanonicalizationMethod_nsprefix_ = "ds"
        self.SignatureMethod = SignatureMethod
        self.SignatureMethod_nsprefix_ = "ds"
        if Reference is None:
            self.Reference = []
        else:
            self.Reference = Reference
        self.Reference_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SignedInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignedInfoType.subclass:
            return SignedInfoType.subclass(*args_, **kwargs_)
        else:
            return SignedInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CanonicalizationMethod(self):
        return self.CanonicalizationMethod
    def set_CanonicalizationMethod(self, CanonicalizationMethod):
        self.CanonicalizationMethod = CanonicalizationMethod
    def get_SignatureMethod(self):
        return self.SignatureMethod
    def set_SignatureMethod(self, SignatureMethod):
        self.SignatureMethod = SignatureMethod
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def add_Reference(self, value):
        self.Reference.append(value)
    def insert_Reference_at(self, index, value):
        self.Reference.insert(index, value)
    def replace_Reference_at(self, index, value):
        self.Reference[index] = value
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def _hasContent(self):
        if (
            self.CanonicalizationMethod is not None or
            self.SignatureMethod is not None or
            self.Reference
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignedInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignedInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignedInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignedInfoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignedInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='SignedInfoType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignedInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CanonicalizationMethod is not None:
            namespaceprefix_ = self.CanonicalizationMethod_nsprefix_ + ':' if (UseCapturedNS_ and self.CanonicalizationMethod_nsprefix_) else ''
            self.CanonicalizationMethod.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='CanonicalizationMethod', pretty_print=pretty_print)
        if self.SignatureMethod is not None:
            namespaceprefix_ = self.SignatureMethod_nsprefix_ + ':' if (UseCapturedNS_ and self.SignatureMethod_nsprefix_) else ''
            self.SignatureMethod.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='SignatureMethod', pretty_print=pretty_print)
        for Reference_ in self.Reference:
            namespaceprefix_ = self.Reference_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_nsprefix_) else ''
            Reference_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='Reference', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CanonicalizationMethod':
            obj_ = CanonicalizationMethodType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CanonicalizationMethod = obj_
            obj_.original_tagname_ = 'CanonicalizationMethod'
        elif nodeName_ == 'SignatureMethod':
            obj_ = SignatureMethodType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SignatureMethod = obj_
            obj_.original_tagname_ = 'SignatureMethod'
        elif nodeName_ == 'Reference':
            obj_ = ReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Reference.append(obj_)
            obj_.original_tagname_ = 'Reference'
# end class SignedInfoType


class CanonicalizationMethodType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Algorithm=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Algorithm = _cast(None, Algorithm)
        self.Algorithm_nsprefix_ = None
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CanonicalizationMethodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CanonicalizationMethodType.subclass:
            return CanonicalizationMethodType.subclass(*args_, **kwargs_)
        else:
            return CanonicalizationMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def add_anytypeobjs_(self, value): self.anytypeobjs_.append(value)
    def insert_anytypeobjs_(self, index, value): self._anytypeobjs_[index] = value
    def get_Algorithm(self):
        return self.Algorithm
    def set_Algorithm(self, Algorithm):
        self.Algorithm = Algorithm
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            self.anytypeobjs_ or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CanonicalizationMethodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CanonicalizationMethodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CanonicalizationMethodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CanonicalizationMethodType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CanonicalizationMethodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='CanonicalizationMethodType'):
        if self.Algorithm is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            outfile.write(' Algorithm=%s' % (quote_attrib(self.Algorithm), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='CanonicalizationMethodType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            for obj_ in self.anytypeobjs_:
                showIndent(outfile, level, pretty_print)
                outfile.write(obj_)
                outfile.write('\n')
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Algorithm', node)
        if value is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            self.Algorithm = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class CanonicalizationMethodType


class SignatureMethodType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Algorithm=None, HMACOutputLength=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Algorithm = _cast(None, Algorithm)
        self.Algorithm_nsprefix_ = None
        self.HMACOutputLength = HMACOutputLength
        self.validate_HMACOutputLengthType(self.HMACOutputLength)
        self.HMACOutputLength_nsprefix_ = "ds"
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SignatureMethodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignatureMethodType.subclass:
            return SignatureMethodType.subclass(*args_, **kwargs_)
        else:
            return SignatureMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HMACOutputLength(self):
        return self.HMACOutputLength
    def set_HMACOutputLength(self, HMACOutputLength):
        self.HMACOutputLength = HMACOutputLength
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def add_anytypeobjs_(self, value): self.anytypeobjs_.append(value)
    def insert_anytypeobjs_(self, index, value): self._anytypeobjs_[index] = value
    def get_Algorithm(self):
        return self.Algorithm
    def set_Algorithm(self, Algorithm):
        self.Algorithm = Algorithm
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_HMACOutputLengthType(self, value):
        result = True
        # Validate type HMACOutputLengthType, a restriction on integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def _hasContent(self):
        if (
            self.HMACOutputLength is not None or
            self.anytypeobjs_ or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='SignatureMethodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignatureMethodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignatureMethodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignatureMethodType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignatureMethodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='SignatureMethodType'):
        if self.Algorithm is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            outfile.write(' Algorithm=%s' % (quote_attrib(self.Algorithm), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='SignatureMethodType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HMACOutputLength is not None:
            namespaceprefix_ = self.HMACOutputLength_nsprefix_ + ':' if (UseCapturedNS_ and self.HMACOutputLength_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHMACOutputLength>%s</%sHMACOutputLength>%s' % (namespaceprefix_ , self.gds_format_integer(self.HMACOutputLength, input_name='HMACOutputLength'), namespaceprefix_ , eol_))
        if not fromsubclass_:
            for obj_ in self.anytypeobjs_:
                showIndent(outfile, level, pretty_print)
                outfile.write(obj_)
                outfile.write('\n')
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Algorithm', node)
        if value is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            self.Algorithm = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'HMACOutputLength' and child_.text is not None:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'HMACOutputLength')
            ival_ = self.gds_validate_integer(ival_, node, 'HMACOutputLength')
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeInteger, 'HMACOutputLength', ival_)
            self.content_.append(obj_)
            self.HMACOutputLength_nsprefix_ = child_.prefix
        elif nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class SignatureMethodType


class ReferenceType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, URI=None, Type=None, Transforms=None, DigestMethod=None, DigestValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        self.URI = _cast(None, URI)
        self.URI_nsprefix_ = None
        self.Type = _cast(None, Type)
        self.Type_nsprefix_ = None
        self.Transforms = Transforms
        self.Transforms_nsprefix_ = "ds"
        self.DigestMethod = DigestMethod
        self.DigestMethod_nsprefix_ = "ds"
        self.DigestValue = DigestValue
        self.DigestValue_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReferenceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReferenceType.subclass:
            return ReferenceType.subclass(*args_, **kwargs_)
        else:
            return ReferenceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transforms(self):
        return self.Transforms
    def set_Transforms(self, Transforms):
        self.Transforms = Transforms
    def get_DigestMethod(self):
        return self.DigestMethod
    def set_DigestMethod(self, DigestMethod):
        self.DigestMethod = DigestMethod
    def get_DigestValue(self):
        return self.DigestValue
    def set_DigestValue(self, DigestValue):
        self.DigestValue = DigestValue
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_URI(self):
        return self.URI
    def set_URI(self, URI):
        self.URI = URI
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def _hasContent(self):
        if (
            self.Transforms is not None or
            self.DigestMethod is not None or
            self.DigestValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='ReferenceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReferenceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReferenceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReferenceType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReferenceType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='ReferenceType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
        if self.URI is not None and 'URI' not in already_processed:
            already_processed.add('URI')
            outfile.write(' URI=%s' % (quote_attrib(self.URI), ))
        if self.Type is not None and 'Type' not in already_processed:
            already_processed.add('Type')
            outfile.write(' Type=%s' % (quote_attrib(self.Type), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='ReferenceType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transforms is not None:
            namespaceprefix_ = self.Transforms_nsprefix_ + ':' if (UseCapturedNS_ and self.Transforms_nsprefix_) else ''
            self.Transforms.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='Transforms', pretty_print=pretty_print)
        if self.DigestMethod is not None:
            namespaceprefix_ = self.DigestMethod_nsprefix_ + ':' if (UseCapturedNS_ and self.DigestMethod_nsprefix_) else ''
            self.DigestMethod.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='DigestMethod', pretty_print=pretty_print)
        if self.DigestValue is not None:
            namespaceprefix_ = self.DigestValue_nsprefix_ + ':' if (UseCapturedNS_ and self.DigestValue_nsprefix_) else ''
            self.DigestValue.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='DigestValue', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
        value = find_attr_value_('URI', node)
        if value is not None and 'URI' not in already_processed:
            already_processed.add('URI')
            self.URI = value
        value = find_attr_value_('Type', node)
        if value is not None and 'Type' not in already_processed:
            already_processed.add('Type')
            self.Type = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Transforms':
            obj_ = TransformsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transforms = obj_
            obj_.original_tagname_ = 'Transforms'
        elif nodeName_ == 'DigestMethod':
            obj_ = DigestMethodType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DigestMethod = obj_
            obj_.original_tagname_ = 'DigestMethod'
        elif nodeName_ == 'DigestValue':
            obj_ = DigestValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DigestValue = obj_
            obj_.original_tagname_ = 'DigestValue'
# end class ReferenceType


class TransformsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transform=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        if Transform is None:
            self.Transform = []
        else:
            self.Transform = Transform
        self.Transform_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TransformsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TransformsType.subclass:
            return TransformsType.subclass(*args_, **kwargs_)
        else:
            return TransformsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transform(self):
        return self.Transform
    def set_Transform(self, Transform):
        self.Transform = Transform
    def add_Transform(self, value):
        self.Transform.append(value)
    def insert_Transform_at(self, index, value):
        self.Transform.insert(index, value)
    def replace_Transform_at(self, index, value):
        self.Transform[index] = value
    def _hasContent(self):
        if (
            self.Transform
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='TransformsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TransformsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TransformsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TransformsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TransformsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='TransformsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='TransformsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Transform_ in self.Transform:
            namespaceprefix_ = self.Transform_nsprefix_ + ':' if (UseCapturedNS_ and self.Transform_nsprefix_) else ''
            Transform_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='Transform', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Transform':
            obj_ = TransformType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transform.append(obj_)
            obj_.original_tagname_ = 'Transform'
# end class TransformsType


class TransformType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Algorithm=None, anytypeobjs_=None, XPath=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Algorithm = _cast(None, Algorithm)
        self.Algorithm_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
        if XPath is None:
            self.XPath = []
        else:
            self.XPath = XPath
        self.XPath_nsprefix_ = None
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TransformType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TransformType.subclass:
            return TransformType.subclass(*args_, **kwargs_)
        else:
            return TransformType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_XPath(self):
        return self.XPath
    def set_XPath(self, XPath):
        self.XPath = XPath
    def add_XPath(self, value):
        self.XPath.append(value)
    def insert_XPath_at(self, index, value):
        self.XPath.insert(index, value)
    def replace_XPath_at(self, index, value):
        self.XPath[index] = value
    def get_Algorithm(self):
        return self.Algorithm
    def set_Algorithm(self, Algorithm):
        self.Algorithm = Algorithm
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            self.anytypeobjs_ is not None or
            self.XPath or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='TransformType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TransformType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TransformType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TransformType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TransformType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='TransformType'):
        if self.Algorithm is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            outfile.write(' Algorithm=%s' % (quote_attrib(self.Algorithm), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='TransformType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for XPath_ in self.XPath:
            namespaceprefix_ = self.XPath_nsprefix_ + ':' if (UseCapturedNS_ and self.XPath_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sXPath>%s</%sXPath>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(XPath_), input_name='XPath')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Algorithm', node)
        if value is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            self.Algorithm = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        elif nodeName_ == 'XPath' and child_.text is not None:
            valuestr_ = child_.text
            valuestr_ = self.gds_parse_string(valuestr_, node, 'XPath')
            valuestr_ = self.gds_validate_string(valuestr_, node, 'XPath')
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'XPath', valuestr_)
            self.content_.append(obj_)
            self.XPath_nsprefix_ = child_.prefix
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class TransformType


class DigestMethodType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Algorithm=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Algorithm = _cast(None, Algorithm)
        self.Algorithm_nsprefix_ = None
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DigestMethodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DigestMethodType.subclass:
            return DigestMethodType.subclass(*args_, **kwargs_)
        else:
            return DigestMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def add_anytypeobjs_(self, value): self.anytypeobjs_.append(value)
    def insert_anytypeobjs_(self, index, value): self._anytypeobjs_[index] = value
    def get_Algorithm(self):
        return self.Algorithm
    def set_Algorithm(self, Algorithm):
        self.Algorithm = Algorithm
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            self.anytypeobjs_ or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DigestMethodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DigestMethodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DigestMethodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DigestMethodType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DigestMethodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='DigestMethodType'):
        if self.Algorithm is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            outfile.write(' Algorithm=%s' % (quote_attrib(self.Algorithm), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='DigestMethodType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            for obj_ in self.anytypeobjs_:
                showIndent(outfile, level, pretty_print)
                outfile.write(obj_)
                outfile.write('\n')
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Algorithm', node)
        if value is not None and 'Algorithm' not in already_processed:
            already_processed.add('Algorithm')
            self.Algorithm = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class DigestMethodType


class KeyInfoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, KeyName=None, KeyValue=None, RetrievalMethod=None, X509Data=None, PGPData=None, SPKIData=None, MgmtData=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        if KeyName is None:
            self.KeyName = []
        else:
            self.KeyName = KeyName
        self.KeyName_nsprefix_ = "ds"
        if KeyValue is None:
            self.KeyValue = []
        else:
            self.KeyValue = KeyValue
        self.KeyValue_nsprefix_ = "ds"
        if RetrievalMethod is None:
            self.RetrievalMethod = []
        else:
            self.RetrievalMethod = RetrievalMethod
        self.RetrievalMethod_nsprefix_ = "ds"
        if X509Data is None:
            self.X509Data = []
        else:
            self.X509Data = X509Data
        self.X509Data_nsprefix_ = "ds"
        if PGPData is None:
            self.PGPData = []
        else:
            self.PGPData = PGPData
        self.PGPData_nsprefix_ = "ds"
        if SPKIData is None:
            self.SPKIData = []
        else:
            self.SPKIData = SPKIData
        self.SPKIData_nsprefix_ = "ds"
        if MgmtData is None:
            self.MgmtData = []
        else:
            self.MgmtData = MgmtData
        self.MgmtData_nsprefix_ = "ds"
        self.anytypeobjs_ = anytypeobjs_
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, KeyInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if KeyInfoType.subclass:
            return KeyInfoType.subclass(*args_, **kwargs_)
        else:
            return KeyInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_KeyName(self):
        return self.KeyName
    def set_KeyName(self, KeyName):
        self.KeyName = KeyName
    def add_KeyName(self, value):
        self.KeyName.append(value)
    def insert_KeyName_at(self, index, value):
        self.KeyName.insert(index, value)
    def replace_KeyName_at(self, index, value):
        self.KeyName[index] = value
    def get_KeyValue(self):
        return self.KeyValue
    def set_KeyValue(self, KeyValue):
        self.KeyValue = KeyValue
    def add_KeyValue(self, value):
        self.KeyValue.append(value)
    def insert_KeyValue_at(self, index, value):
        self.KeyValue.insert(index, value)
    def replace_KeyValue_at(self, index, value):
        self.KeyValue[index] = value
    def get_RetrievalMethod(self):
        return self.RetrievalMethod
    def set_RetrievalMethod(self, RetrievalMethod):
        self.RetrievalMethod = RetrievalMethod
    def add_RetrievalMethod(self, value):
        self.RetrievalMethod.append(value)
    def insert_RetrievalMethod_at(self, index, value):
        self.RetrievalMethod.insert(index, value)
    def replace_RetrievalMethod_at(self, index, value):
        self.RetrievalMethod[index] = value
    def get_X509Data(self):
        return self.X509Data
    def set_X509Data(self, X509Data):
        self.X509Data = X509Data
    def add_X509Data(self, value):
        self.X509Data.append(value)
    def insert_X509Data_at(self, index, value):
        self.X509Data.insert(index, value)
    def replace_X509Data_at(self, index, value):
        self.X509Data[index] = value
    def get_PGPData(self):
        return self.PGPData
    def set_PGPData(self, PGPData):
        self.PGPData = PGPData
    def add_PGPData(self, value):
        self.PGPData.append(value)
    def insert_PGPData_at(self, index, value):
        self.PGPData.insert(index, value)
    def replace_PGPData_at(self, index, value):
        self.PGPData[index] = value
    def get_SPKIData(self):
        return self.SPKIData
    def set_SPKIData(self, SPKIData):
        self.SPKIData = SPKIData
    def add_SPKIData(self, value):
        self.SPKIData.append(value)
    def insert_SPKIData_at(self, index, value):
        self.SPKIData.insert(index, value)
    def replace_SPKIData_at(self, index, value):
        self.SPKIData[index] = value
    def get_MgmtData(self):
        return self.MgmtData
    def set_MgmtData(self, MgmtData):
        self.MgmtData = MgmtData
    def add_MgmtData(self, value):
        self.MgmtData.append(value)
    def insert_MgmtData_at(self, index, value):
        self.MgmtData.insert(index, value)
    def replace_MgmtData_at(self, index, value):
        self.MgmtData[index] = value
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            self.KeyName or
            self.KeyValue or
            self.RetrievalMethod or
            self.X509Data or
            self.PGPData or
            self.SPKIData or
            self.MgmtData or
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='KeyInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('KeyInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'KeyInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='KeyInfoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='KeyInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='KeyInfoType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='KeyInfoType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for KeyName_ in self.KeyName:
            namespaceprefix_ = self.KeyName_nsprefix_ + ':' if (UseCapturedNS_ and self.KeyName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sKeyName>%s</%sKeyName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(KeyName_), input_name='KeyName')), namespaceprefix_ , eol_))
        for KeyValue_ in self.KeyValue:
            namespaceprefix_ = self.KeyValue_nsprefix_ + ':' if (UseCapturedNS_ and self.KeyValue_nsprefix_) else ''
            KeyValue_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='KeyValue', pretty_print=pretty_print)
        for RetrievalMethod_ in self.RetrievalMethod:
            namespaceprefix_ = self.RetrievalMethod_nsprefix_ + ':' if (UseCapturedNS_ and self.RetrievalMethod_nsprefix_) else ''
            RetrievalMethod_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='RetrievalMethod', pretty_print=pretty_print)
        for X509Data_ in self.X509Data:
            namespaceprefix_ = self.X509Data_nsprefix_ + ':' if (UseCapturedNS_ and self.X509Data_nsprefix_) else ''
            X509Data_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='X509Data', pretty_print=pretty_print)
        for PGPData_ in self.PGPData:
            namespaceprefix_ = self.PGPData_nsprefix_ + ':' if (UseCapturedNS_ and self.PGPData_nsprefix_) else ''
            PGPData_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='PGPData', pretty_print=pretty_print)
        for SPKIData_ in self.SPKIData:
            namespaceprefix_ = self.SPKIData_nsprefix_ + ':' if (UseCapturedNS_ and self.SPKIData_nsprefix_) else ''
            SPKIData_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='SPKIData', pretty_print=pretty_print)
        for MgmtData_ in self.MgmtData:
            namespaceprefix_ = self.MgmtData_nsprefix_ + ':' if (UseCapturedNS_ and self.MgmtData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMgmtData>%s</%sMgmtData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(MgmtData_), input_name='MgmtData')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'KeyName' and child_.text is not None:
            valuestr_ = child_.text
            valuestr_ = self.gds_parse_string(valuestr_, node, 'KeyName')
            valuestr_ = self.gds_validate_string(valuestr_, node, 'KeyName')
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'KeyName', valuestr_)
            self.content_.append(obj_)
            self.KeyName_nsprefix_ = child_.prefix
        elif nodeName_ == 'KeyValue':
            obj_ = KeyValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'KeyValue', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_KeyValue'):
              self.add_KeyValue(obj_.value)
            elif hasattr(self, 'set_KeyValue'):
              self.set_KeyValue(obj_.value)
        elif nodeName_ == 'RetrievalMethod':
            obj_ = RetrievalMethodType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'RetrievalMethod', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_RetrievalMethod'):
              self.add_RetrievalMethod(obj_.value)
            elif hasattr(self, 'set_RetrievalMethod'):
              self.set_RetrievalMethod(obj_.value)
        elif nodeName_ == 'X509Data':
            obj_ = X509DataType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'X509Data', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_X509Data'):
              self.add_X509Data(obj_.value)
            elif hasattr(self, 'set_X509Data'):
              self.set_X509Data(obj_.value)
        elif nodeName_ == 'PGPData':
            obj_ = PGPDataType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'PGPData', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_PGPData'):
              self.add_PGPData(obj_.value)
            elif hasattr(self, 'set_PGPData'):
              self.set_PGPData(obj_.value)
        elif nodeName_ == 'SPKIData':
            obj_ = SPKIDataType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'SPKIData', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_SPKIData'):
              self.add_SPKIData(obj_.value)
            elif hasattr(self, 'set_SPKIData'):
              self.set_SPKIData(obj_.value)
        elif nodeName_ == 'MgmtData' and child_.text is not None:
            valuestr_ = child_.text
            valuestr_ = self.gds_parse_string(valuestr_, node, 'MgmtData')
            valuestr_ = self.gds_validate_string(valuestr_, node, 'MgmtData')
            obj_ = self.mixedclass_(MixedContainer.CategorySimple,
                MixedContainer.TypeString, 'MgmtData', valuestr_)
            self.content_.append(obj_)
            self.MgmtData_nsprefix_ = child_.prefix
        elif nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class KeyInfoType


class KeyValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DSAKeyValue=None, RSAKeyValue=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DSAKeyValue = DSAKeyValue
        self.DSAKeyValue_nsprefix_ = "ds"
        self.RSAKeyValue = RSAKeyValue
        self.RSAKeyValue_nsprefix_ = "ds"
        self.anytypeobjs_ = anytypeobjs_
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, KeyValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if KeyValueType.subclass:
            return KeyValueType.subclass(*args_, **kwargs_)
        else:
            return KeyValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DSAKeyValue(self):
        return self.DSAKeyValue
    def set_DSAKeyValue(self, DSAKeyValue):
        self.DSAKeyValue = DSAKeyValue
    def get_RSAKeyValue(self):
        return self.RSAKeyValue
    def set_RSAKeyValue(self, RSAKeyValue):
        self.RSAKeyValue = RSAKeyValue
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            self.DSAKeyValue is not None or
            self.RSAKeyValue is not None or
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='KeyValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('KeyValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'KeyValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='KeyValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='KeyValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='KeyValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='KeyValueType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DSAKeyValue is not None:
            namespaceprefix_ = self.DSAKeyValue_nsprefix_ + ':' if (UseCapturedNS_ and self.DSAKeyValue_nsprefix_) else ''
            self.DSAKeyValue.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='DSAKeyValue', pretty_print=pretty_print)
        if self.RSAKeyValue is not None:
            namespaceprefix_ = self.RSAKeyValue_nsprefix_ + ':' if (UseCapturedNS_ and self.RSAKeyValue_nsprefix_) else ''
            self.RSAKeyValue.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='RSAKeyValue', pretty_print=pretty_print)
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DSAKeyValue':
            obj_ = DSAKeyValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'DSAKeyValue', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_DSAKeyValue'):
              self.add_DSAKeyValue(obj_.value)
            elif hasattr(self, 'set_DSAKeyValue'):
              self.set_DSAKeyValue(obj_.value)
        elif nodeName_ == 'RSAKeyValue':
            obj_ = RSAKeyValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'RSAKeyValue', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_RSAKeyValue'):
              self.add_RSAKeyValue(obj_.value)
            elif hasattr(self, 'set_RSAKeyValue'):
              self.set_RSAKeyValue(obj_.value)
        elif nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class KeyValueType


class RetrievalMethodType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, URI=None, Type=None, Transforms=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.URI = _cast(None, URI)
        self.URI_nsprefix_ = None
        self.Type = _cast(None, Type)
        self.Type_nsprefix_ = None
        self.Transforms = Transforms
        self.Transforms_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RetrievalMethodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RetrievalMethodType.subclass:
            return RetrievalMethodType.subclass(*args_, **kwargs_)
        else:
            return RetrievalMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transforms(self):
        return self.Transforms
    def set_Transforms(self, Transforms):
        self.Transforms = Transforms
    def get_URI(self):
        return self.URI
    def set_URI(self, URI):
        self.URI = URI
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def _hasContent(self):
        if (
            self.Transforms is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='RetrievalMethodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RetrievalMethodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RetrievalMethodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RetrievalMethodType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RetrievalMethodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='RetrievalMethodType'):
        if self.URI is not None and 'URI' not in already_processed:
            already_processed.add('URI')
            outfile.write(' URI=%s' % (quote_attrib(self.URI), ))
        if self.Type is not None and 'Type' not in already_processed:
            already_processed.add('Type')
            outfile.write(' Type=%s' % (quote_attrib(self.Type), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='RetrievalMethodType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transforms is not None:
            namespaceprefix_ = self.Transforms_nsprefix_ + ':' if (UseCapturedNS_ and self.Transforms_nsprefix_) else ''
            self.Transforms.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='Transforms', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('URI', node)
        if value is not None and 'URI' not in already_processed:
            already_processed.add('URI')
            self.URI = value
        value = find_attr_value_('Type', node)
        if value is not None and 'Type' not in already_processed:
            already_processed.add('Type')
            self.Type = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Transforms':
            obj_ = TransformsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transforms = obj_
            obj_.original_tagname_ = 'Transforms'
# end class RetrievalMethodType


class X509DataType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, X509IssuerSerial=None, X509SKI=None, X509SubjectName=None, X509Certificate=None, X509CRL=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if X509IssuerSerial is None:
            self.X509IssuerSerial = []
        else:
            self.X509IssuerSerial = X509IssuerSerial
        self.X509IssuerSerial_nsprefix_ = "ds"
        if X509SKI is None:
            self.X509SKI = []
        else:
            self.X509SKI = X509SKI
        self.X509SKI_nsprefix_ = None
        if X509SubjectName is None:
            self.X509SubjectName = []
        else:
            self.X509SubjectName = X509SubjectName
        self.X509SubjectName_nsprefix_ = None
        if X509Certificate is None:
            self.X509Certificate = []
        else:
            self.X509Certificate = X509Certificate
        self.X509Certificate_nsprefix_ = None
        if X509CRL is None:
            self.X509CRL = []
        else:
            self.X509CRL = X509CRL
        self.X509CRL_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, X509DataType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if X509DataType.subclass:
            return X509DataType.subclass(*args_, **kwargs_)
        else:
            return X509DataType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_X509IssuerSerial(self):
        return self.X509IssuerSerial
    def set_X509IssuerSerial(self, X509IssuerSerial):
        self.X509IssuerSerial = X509IssuerSerial
    def add_X509IssuerSerial(self, value):
        self.X509IssuerSerial.append(value)
    def insert_X509IssuerSerial_at(self, index, value):
        self.X509IssuerSerial.insert(index, value)
    def replace_X509IssuerSerial_at(self, index, value):
        self.X509IssuerSerial[index] = value
    def get_X509SKI(self):
        return self.X509SKI
    def set_X509SKI(self, X509SKI):
        self.X509SKI = X509SKI
    def add_X509SKI(self, value):
        self.X509SKI.append(value)
    def insert_X509SKI_at(self, index, value):
        self.X509SKI.insert(index, value)
    def replace_X509SKI_at(self, index, value):
        self.X509SKI[index] = value
    def get_X509SubjectName(self):
        return self.X509SubjectName
    def set_X509SubjectName(self, X509SubjectName):
        self.X509SubjectName = X509SubjectName
    def add_X509SubjectName(self, value):
        self.X509SubjectName.append(value)
    def insert_X509SubjectName_at(self, index, value):
        self.X509SubjectName.insert(index, value)
    def replace_X509SubjectName_at(self, index, value):
        self.X509SubjectName[index] = value
    def get_X509Certificate(self):
        return self.X509Certificate
    def set_X509Certificate(self, X509Certificate):
        self.X509Certificate = X509Certificate
    def add_X509Certificate(self, value):
        self.X509Certificate.append(value)
    def insert_X509Certificate_at(self, index, value):
        self.X509Certificate.insert(index, value)
    def replace_X509Certificate_at(self, index, value):
        self.X509Certificate[index] = value
    def get_X509CRL(self):
        return self.X509CRL
    def set_X509CRL(self, X509CRL):
        self.X509CRL = X509CRL
    def add_X509CRL(self, value):
        self.X509CRL.append(value)
    def insert_X509CRL_at(self, index, value):
        self.X509CRL.insert(index, value)
    def replace_X509CRL_at(self, index, value):
        self.X509CRL[index] = value
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def _hasContent(self):
        if (
            self.X509IssuerSerial or
            self.X509SKI or
            self.X509SubjectName or
            self.X509Certificate or
            self.X509CRL or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='X509DataType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('X509DataType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'X509DataType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='X509DataType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='X509DataType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='X509DataType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='X509DataType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for X509IssuerSerial_ in self.X509IssuerSerial:
            namespaceprefix_ = self.X509IssuerSerial_nsprefix_ + ':' if (UseCapturedNS_ and self.X509IssuerSerial_nsprefix_) else ''
            X509IssuerSerial_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='X509IssuerSerial', pretty_print=pretty_print)
        for X509SKI_ in self.X509SKI:
            namespaceprefix_ = self.X509SKI_nsprefix_ + ':' if (UseCapturedNS_ and self.X509SKI_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sX509SKI>%s</%sX509SKI>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(X509SKI_), input_name='X509SKI')), namespaceprefix_ , eol_))
        for X509SubjectName_ in self.X509SubjectName:
            namespaceprefix_ = self.X509SubjectName_nsprefix_ + ':' if (UseCapturedNS_ and self.X509SubjectName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sX509SubjectName>%s</%sX509SubjectName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(X509SubjectName_), input_name='X509SubjectName')), namespaceprefix_ , eol_))
        for X509Certificate_ in self.X509Certificate:
            namespaceprefix_ = self.X509Certificate_nsprefix_ + ':' if (UseCapturedNS_ and self.X509Certificate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sX509Certificate>%s</%sX509Certificate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(X509Certificate_), input_name='X509Certificate')), namespaceprefix_ , eol_))
        for X509CRL_ in self.X509CRL:
            namespaceprefix_ = self.X509CRL_nsprefix_ + ':' if (UseCapturedNS_ and self.X509CRL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sX509CRL>%s</%sX509CRL>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(X509CRL_), input_name='X509CRL')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'X509IssuerSerial':
            obj_ = X509IssuerSerialType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.X509IssuerSerial.append(obj_)
            obj_.original_tagname_ = 'X509IssuerSerial'
        elif nodeName_ == 'X509SKI':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'X509SKI')
            value_ = self.gds_validate_string(value_, node, 'X509SKI')
            self.X509SKI.append(value_)
            self.X509SKI_nsprefix_ = child_.prefix
        elif nodeName_ == 'X509SubjectName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'X509SubjectName')
            value_ = self.gds_validate_string(value_, node, 'X509SubjectName')
            self.X509SubjectName.append(value_)
            self.X509SubjectName_nsprefix_ = child_.prefix
        elif nodeName_ == 'X509Certificate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'X509Certificate')
            value_ = self.gds_validate_string(value_, node, 'X509Certificate')
            self.X509Certificate.append(value_)
            self.X509Certificate_nsprefix_ = child_.prefix
        elif nodeName_ == 'X509CRL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'X509CRL')
            value_ = self.gds_validate_string(value_, node, 'X509CRL')
            self.X509CRL.append(value_)
            self.X509CRL_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'X509DataType')
            self.set_anytypeobjs_(content_)
# end class X509DataType


class X509IssuerSerialType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, X509IssuerName=None, X509SerialNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.X509IssuerName = X509IssuerName
        self.X509IssuerName_nsprefix_ = None
        self.X509SerialNumber = X509SerialNumber
        self.X509SerialNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, X509IssuerSerialType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if X509IssuerSerialType.subclass:
            return X509IssuerSerialType.subclass(*args_, **kwargs_)
        else:
            return X509IssuerSerialType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_X509IssuerName(self):
        return self.X509IssuerName
    def set_X509IssuerName(self, X509IssuerName):
        self.X509IssuerName = X509IssuerName
    def get_X509SerialNumber(self):
        return self.X509SerialNumber
    def set_X509SerialNumber(self, X509SerialNumber):
        self.X509SerialNumber = X509SerialNumber
    def _hasContent(self):
        if (
            self.X509IssuerName is not None or
            self.X509SerialNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='X509IssuerSerialType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('X509IssuerSerialType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'X509IssuerSerialType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='X509IssuerSerialType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='X509IssuerSerialType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='X509IssuerSerialType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='X509IssuerSerialType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.X509IssuerName is not None:
            namespaceprefix_ = self.X509IssuerName_nsprefix_ + ':' if (UseCapturedNS_ and self.X509IssuerName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sX509IssuerName>%s</%sX509IssuerName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.X509IssuerName), input_name='X509IssuerName')), namespaceprefix_ , eol_))
        if self.X509SerialNumber is not None:
            namespaceprefix_ = self.X509SerialNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.X509SerialNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sX509SerialNumber>%s</%sX509SerialNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.X509SerialNumber), input_name='X509SerialNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'X509IssuerName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'X509IssuerName')
            value_ = self.gds_validate_string(value_, node, 'X509IssuerName')
            self.X509IssuerName = value_
            self.X509IssuerName_nsprefix_ = child_.prefix
        elif nodeName_ == 'X509SerialNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'X509SerialNumber')
            value_ = self.gds_validate_string(value_, node, 'X509SerialNumber')
            self.X509SerialNumber = value_
            self.X509SerialNumber_nsprefix_ = child_.prefix
# end class X509IssuerSerialType


class PGPDataType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PGPKeyID=None, PGPKeyPacket=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PGPKeyID = PGPKeyID
        self.PGPKeyID_nsprefix_ = None
        self.PGPKeyPacket = PGPKeyPacket
        self.PGPKeyPacket_nsprefix_ = None
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PGPDataType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PGPDataType.subclass:
            return PGPDataType.subclass(*args_, **kwargs_)
        else:
            return PGPDataType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PGPKeyID(self):
        return self.PGPKeyID
    def set_PGPKeyID(self, PGPKeyID):
        self.PGPKeyID = PGPKeyID
    def get_PGPKeyPacket(self):
        return self.PGPKeyPacket
    def set_PGPKeyPacket(self, PGPKeyPacket):
        self.PGPKeyPacket = PGPKeyPacket
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def add_anytypeobjs_(self, value): self.anytypeobjs_.append(value)
    def insert_anytypeobjs_(self, index, value): self._anytypeobjs_[index] = value
    def _hasContent(self):
        if (
            self.PGPKeyID is not None or
            self.PGPKeyPacket is not None or
            self.anytypeobjs_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='PGPDataType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PGPDataType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PGPDataType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PGPDataType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PGPDataType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='PGPDataType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='PGPDataType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PGPKeyID is not None:
            namespaceprefix_ = self.PGPKeyID_nsprefix_ + ':' if (UseCapturedNS_ and self.PGPKeyID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPGPKeyID>%s</%sPGPKeyID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PGPKeyID), input_name='PGPKeyID')), namespaceprefix_ , eol_))
        if self.PGPKeyPacket is not None:
            namespaceprefix_ = self.PGPKeyPacket_nsprefix_ + ':' if (UseCapturedNS_ and self.PGPKeyPacket_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPGPKeyPacket>%s</%sPGPKeyPacket>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PGPKeyPacket), input_name='PGPKeyPacket')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            for obj_ in self.anytypeobjs_:
                showIndent(outfile, level, pretty_print)
                outfile.write(obj_)
                outfile.write('\n')
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PGPKeyID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PGPKeyID')
            value_ = self.gds_validate_string(value_, node, 'PGPKeyID')
            self.PGPKeyID = value_
            self.PGPKeyID_nsprefix_ = child_.prefix
        elif nodeName_ == 'PGPKeyPacket':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PGPKeyPacket')
            value_ = self.gds_validate_string(value_, node, 'PGPKeyPacket')
            self.PGPKeyPacket = value_
            self.PGPKeyPacket_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'PGPDataType')
            self.anytypeobjs_.append(content_)
# end class PGPDataType


class SPKIDataType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SPKISexp=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if SPKISexp is None:
            self.SPKISexp = []
        else:
            self.SPKISexp = SPKISexp
        self.SPKISexp_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SPKIDataType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SPKIDataType.subclass:
            return SPKIDataType.subclass(*args_, **kwargs_)
        else:
            return SPKIDataType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SPKISexp(self):
        return self.SPKISexp
    def set_SPKISexp(self, SPKISexp):
        self.SPKISexp = SPKISexp
    def add_SPKISexp(self, value):
        self.SPKISexp.append(value)
    def insert_SPKISexp_at(self, index, value):
        self.SPKISexp.insert(index, value)
    def replace_SPKISexp_at(self, index, value):
        self.SPKISexp[index] = value
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def _hasContent(self):
        if (
            self.SPKISexp or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='SPKIDataType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SPKIDataType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SPKIDataType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SPKIDataType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SPKIDataType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='SPKIDataType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='SPKIDataType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for SPKISexp_ in self.SPKISexp:
            namespaceprefix_ = self.SPKISexp_nsprefix_ + ':' if (UseCapturedNS_ and self.SPKISexp_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSPKISexp>%s</%sSPKISexp>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(SPKISexp_), input_name='SPKISexp')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SPKISexp':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SPKISexp')
            value_ = self.gds_validate_string(value_, node, 'SPKISexp')
            self.SPKISexp.append(value_)
            self.SPKISexp_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'SPKIDataType')
            self.set_anytypeobjs_(content_)
# end class SPKIDataType


class ObjectType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, MimeType=None, Encoding=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        self.MimeType = _cast(None, MimeType)
        self.MimeType_nsprefix_ = None
        self.Encoding = _cast(None, Encoding)
        self.Encoding_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ObjectType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ObjectType.subclass:
            return ObjectType.subclass(*args_, **kwargs_)
        else:
            return ObjectType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_MimeType(self):
        return self.MimeType
    def set_MimeType(self, MimeType):
        self.MimeType = MimeType
    def get_Encoding(self):
        return self.Encoding
    def set_Encoding(self, Encoding):
        self.Encoding = Encoding
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ObjectType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ObjectType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ObjectType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ObjectType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ObjectType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='ObjectType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
        if self.MimeType is not None and 'MimeType' not in already_processed:
            already_processed.add('MimeType')
            outfile.write(' MimeType=%s' % (quote_attrib(self.MimeType), ))
        if self.Encoding is not None and 'Encoding' not in already_processed:
            already_processed.add('Encoding')
            outfile.write(' Encoding=%s' % (quote_attrib(self.Encoding), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='ObjectType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
        value = find_attr_value_('MimeType', node)
        if value is not None and 'MimeType' not in already_processed:
            already_processed.add('MimeType')
            self.MimeType = value
        value = find_attr_value_('Encoding', node)
        if value is not None and 'Encoding' not in already_processed:
            already_processed.add('Encoding')
            self.Encoding = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class ObjectType


class ManifestType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, Reference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        if Reference is None:
            self.Reference = []
        else:
            self.Reference = Reference
        self.Reference_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ManifestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ManifestType.subclass:
            return ManifestType.subclass(*args_, **kwargs_)
        else:
            return ManifestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def add_Reference(self, value):
        self.Reference.append(value)
    def insert_Reference_at(self, index, value):
        self.Reference.insert(index, value)
    def replace_Reference_at(self, index, value):
        self.Reference[index] = value
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def _hasContent(self):
        if (
            self.Reference
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='ManifestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ManifestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ManifestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ManifestType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ManifestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='ManifestType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='ManifestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Reference_ in self.Reference:
            namespaceprefix_ = self.Reference_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_nsprefix_) else ''
            Reference_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='Reference', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Reference':
            obj_ = ReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Reference.append(obj_)
            obj_.original_tagname_ = 'Reference'
# end class ManifestType


class SignaturePropertiesType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, SignatureProperty=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        if SignatureProperty is None:
            self.SignatureProperty = []
        else:
            self.SignatureProperty = SignatureProperty
        self.SignatureProperty_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SignaturePropertiesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignaturePropertiesType.subclass:
            return SignaturePropertiesType.subclass(*args_, **kwargs_)
        else:
            return SignaturePropertiesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SignatureProperty(self):
        return self.SignatureProperty
    def set_SignatureProperty(self, SignatureProperty):
        self.SignatureProperty = SignatureProperty
    def add_SignatureProperty(self, value):
        self.SignatureProperty.append(value)
    def insert_SignatureProperty_at(self, index, value):
        self.SignatureProperty.insert(index, value)
    def replace_SignatureProperty_at(self, index, value):
        self.SignatureProperty[index] = value
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def _hasContent(self):
        if (
            self.SignatureProperty
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignaturePropertiesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignaturePropertiesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignaturePropertiesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignaturePropertiesType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignaturePropertiesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='SignaturePropertiesType'):
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='SignaturePropertiesType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for SignatureProperty_ in self.SignatureProperty:
            namespaceprefix_ = self.SignatureProperty_nsprefix_ + ':' if (UseCapturedNS_ and self.SignatureProperty_nsprefix_) else ''
            SignatureProperty_.export(outfile, level, namespaceprefix_='ds:', namespacedef_='', name_='SignatureProperty', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SignatureProperty':
            obj_ = SignaturePropertyType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SignatureProperty.append(obj_)
            obj_.original_tagname_ = 'SignatureProperty'
# end class SignaturePropertiesType


class SignaturePropertyType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Target=None, Id=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Target = _cast(None, Target)
        self.Target_nsprefix_ = None
        self.Id = _cast(None, Id)
        self.Id_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SignaturePropertyType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignaturePropertyType.subclass:
            return SignaturePropertyType.subclass(*args_, **kwargs_)
        else:
            return SignaturePropertyType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_Target(self):
        return self.Target
    def set_Target(self, Target):
        self.Target = Target
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='SignaturePropertyType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignaturePropertyType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignaturePropertyType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignaturePropertyType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignaturePropertyType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='SignaturePropertyType'):
        if self.Target is not None and 'Target' not in already_processed:
            already_processed.add('Target')
            outfile.write(' Target=%s' % (quote_attrib(self.Target), ))
        if self.Id is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            outfile.write(' Id=%s' % (quote_attrib(self.Id), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:None="http://www.w3.org/2001/XMLSchema" ', name_='SignaturePropertyType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Target', node)
        if value is not None and 'Target' not in already_processed:
            already_processed.add('Target')
            self.Target = value
        value = find_attr_value_('Id', node)
        if value is not None and 'Id' not in already_processed:
            already_processed.add('Id')
            self.Id = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class SignaturePropertyType


class DSAKeyValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, P=None, Q=None, G=None, Y=None, J=None, Seed=None, PgenCounter=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.P = P
        self.validate_CryptoBinary(self.P)
        self.P_nsprefix_ = "ds"
        self.Q = Q
        self.validate_CryptoBinary(self.Q)
        self.Q_nsprefix_ = "ds"
        self.G = G
        self.validate_CryptoBinary(self.G)
        self.G_nsprefix_ = "ds"
        self.Y = Y
        self.validate_CryptoBinary(self.Y)
        self.Y_nsprefix_ = "ds"
        self.J = J
        self.validate_CryptoBinary(self.J)
        self.J_nsprefix_ = "ds"
        self.Seed = Seed
        self.validate_CryptoBinary(self.Seed)
        self.Seed_nsprefix_ = "ds"
        self.PgenCounter = PgenCounter
        self.validate_CryptoBinary(self.PgenCounter)
        self.PgenCounter_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DSAKeyValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DSAKeyValueType.subclass:
            return DSAKeyValueType.subclass(*args_, **kwargs_)
        else:
            return DSAKeyValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_P(self):
        return self.P
    def set_P(self, P):
        self.P = P
    def get_Q(self):
        return self.Q
    def set_Q(self, Q):
        self.Q = Q
    def get_G(self):
        return self.G
    def set_G(self, G):
        self.G = G
    def get_Y(self):
        return self.Y
    def set_Y(self, Y):
        self.Y = Y
    def get_J(self):
        return self.J
    def set_J(self, J):
        self.J = J
    def get_Seed(self):
        return self.Seed
    def set_Seed(self, Seed):
        self.Seed = Seed
    def get_PgenCounter(self):
        return self.PgenCounter
    def set_PgenCounter(self, PgenCounter):
        self.PgenCounter = PgenCounter
    def validate_CryptoBinary(self, value):
        result = True
        # Validate type CryptoBinary, a restriction on base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.P is not None or
            self.Q is not None or
            self.G is not None or
            self.Y is not None or
            self.J is not None or
            self.Seed is not None or
            self.PgenCounter is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='DSAKeyValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DSAKeyValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DSAKeyValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DSAKeyValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DSAKeyValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='DSAKeyValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='DSAKeyValueType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.P is not None:
            namespaceprefix_ = self.P_nsprefix_ + ':' if (UseCapturedNS_ and self.P_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sP>%s</%sP>%s' % (namespaceprefix_ , self.gds_format_base64(self.P, input_name='P'), namespaceprefix_ , eol_))
        if self.Q is not None:
            namespaceprefix_ = self.Q_nsprefix_ + ':' if (UseCapturedNS_ and self.Q_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQ>%s</%sQ>%s' % (namespaceprefix_ , self.gds_format_base64(self.Q, input_name='Q'), namespaceprefix_ , eol_))
        if self.G is not None:
            namespaceprefix_ = self.G_nsprefix_ + ':' if (UseCapturedNS_ and self.G_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sG>%s</%sG>%s' % (namespaceprefix_ , self.gds_format_base64(self.G, input_name='G'), namespaceprefix_ , eol_))
        if self.Y is not None:
            namespaceprefix_ = self.Y_nsprefix_ + ':' if (UseCapturedNS_ and self.Y_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sY>%s</%sY>%s' % (namespaceprefix_ , self.gds_format_base64(self.Y, input_name='Y'), namespaceprefix_ , eol_))
        if self.J is not None:
            namespaceprefix_ = self.J_nsprefix_ + ':' if (UseCapturedNS_ and self.J_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sJ>%s</%sJ>%s' % (namespaceprefix_ , self.gds_format_base64(self.J, input_name='J'), namespaceprefix_ , eol_))
        if self.Seed is not None:
            namespaceprefix_ = self.Seed_nsprefix_ + ':' if (UseCapturedNS_ and self.Seed_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSeed>%s</%sSeed>%s' % (namespaceprefix_ , self.gds_format_base64(self.Seed, input_name='Seed'), namespaceprefix_ , eol_))
        if self.PgenCounter is not None:
            namespaceprefix_ = self.PgenCounter_nsprefix_ + ':' if (UseCapturedNS_ and self.PgenCounter_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPgenCounter>%s</%sPgenCounter>%s' % (namespaceprefix_ , self.gds_format_base64(self.PgenCounter, input_name='PgenCounter'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'P':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'P')
            else:
                bval_ = None
            self.P = bval_
            self.P_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.P)
        elif nodeName_ == 'Q':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Q')
            else:
                bval_ = None
            self.Q = bval_
            self.Q_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.Q)
        elif nodeName_ == 'G':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'G')
            else:
                bval_ = None
            self.G = bval_
            self.G_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.G)
        elif nodeName_ == 'Y':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Y')
            else:
                bval_ = None
            self.Y = bval_
            self.Y_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.Y)
        elif nodeName_ == 'J':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'J')
            else:
                bval_ = None
            self.J = bval_
            self.J_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.J)
        elif nodeName_ == 'Seed':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Seed')
            else:
                bval_ = None
            self.Seed = bval_
            self.Seed_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.Seed)
        elif nodeName_ == 'PgenCounter':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'PgenCounter')
            else:
                bval_ = None
            self.PgenCounter = bval_
            self.PgenCounter_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.PgenCounter)
# end class DSAKeyValueType


class RSAKeyValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Modulus=None, Exponent=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.Modulus = Modulus
        self.validate_CryptoBinary(self.Modulus)
        self.Modulus_nsprefix_ = "ds"
        self.Exponent = Exponent
        self.validate_CryptoBinary(self.Exponent)
        self.Exponent_nsprefix_ = "ds"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RSAKeyValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RSAKeyValueType.subclass:
            return RSAKeyValueType.subclass(*args_, **kwargs_)
        else:
            return RSAKeyValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Modulus(self):
        return self.Modulus
    def set_Modulus(self, Modulus):
        self.Modulus = Modulus
    def get_Exponent(self):
        return self.Exponent
    def set_Exponent(self, Exponent):
        self.Exponent = Exponent
    def validate_CryptoBinary(self, value):
        result = True
        # Validate type CryptoBinary, a restriction on base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.Modulus is not None or
            self.Exponent is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='RSAKeyValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RSAKeyValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RSAKeyValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RSAKeyValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RSAKeyValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='ds:', name_='RSAKeyValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='ds:', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='RSAKeyValueType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Modulus is not None:
            namespaceprefix_ = self.Modulus_nsprefix_ + ':' if (UseCapturedNS_ and self.Modulus_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sModulus>%s</%sModulus>%s' % (namespaceprefix_ , self.gds_format_base64(self.Modulus, input_name='Modulus'), namespaceprefix_ , eol_))
        if self.Exponent is not None:
            namespaceprefix_ = self.Exponent_nsprefix_ + ':' if (UseCapturedNS_ and self.Exponent_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExponent>%s</%sExponent>%s' % (namespaceprefix_ , self.gds_format_base64(self.Exponent, input_name='Exponent'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Modulus':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Modulus')
            else:
                bval_ = None
            self.Modulus = bval_
            self.Modulus_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.Modulus)
        elif nodeName_ == 'Exponent':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Exponent')
            else:
                bval_ = None
            self.Exponent = bval_
            self.Exponent_nsprefix_ = child_.prefix
            # validate type CryptoBinary
            self.validate_CryptoBinary(self.Exponent)
# end class RSAKeyValueType


class DigestValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "ds"
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DigestValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DigestValueType.subclass:
            return DigestValueType.subclass(*args_, **kwargs_)
        else:
            return DigestValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_DigestValueType_impl(self, value):
        result = True
        # Validate type DigestValueType_impl, a restriction on base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='DigestValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DigestValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DigestValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DigestValueType')
        if self._hasContent():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DigestValueType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DigestValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:ds="http://www.w3.org/2000/09/xmldsig#"', name_='DigestValueType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class DigestValueType


GDSClassesMapping = {
    'CanonicalizationMethod': CanonicalizationMethodType,
    'DSAKeyValue': DSAKeyValueType,
    'DigestMethod': DigestMethodType,
    'DigestValue': DigestValueType,
    'FatturaElettronica': FatturaElettronicaType,
    'KeyInfo': KeyInfoType,
    'KeyValue': KeyValueType,
    'Manifest': ManifestType,
    'Object': ObjectType,
    'PGPData': PGPDataType,
    'RSAKeyValue': RSAKeyValueType,
    'Reference': ReferenceType,
    'RetrievalMethod': RetrievalMethodType,
    'SPKIData': SPKIDataType,
    'Signature': SignatureType,
    'SignatureMethod': SignatureMethodType,
    'SignatureProperties': SignaturePropertiesType,
    'SignatureProperty': SignaturePropertyType,
    'SignatureValue': SignatureValueType,
    'SignedInfo': SignedInfoType,
    'Transform': TransformType,
    'Transforms': TransformsType,
    'X509Data': X509DataType,
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    '''Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    '''
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = ' '.join([
        'xmlns:{}="{}"'.format(prefix, uri)
        for prefix, uri in nsmap.items()
    ])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=namespacedefs,
            pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True,
               mapping=None, reverse_mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if mapping is None:
        mapping = {}
    if reverse_mapping is None:
        reverse_mapping = {}
    rootElement = rootObj.to_etree(
        None, name_=rootTag, mapping_=mapping,
        reverse_mapping_=reverse_mapping, nsmap_=nsmap)
    reverse_node_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_node_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FatturaElettronicaType'
        rootClass = FatturaElettronicaType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from models import *\n\n')
        sys.stdout.write('import models as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

RenameMappings_ = {
}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2': [('CodiceDestinatarioType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CodiceType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('FormatoTrasmissioneType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CausalePagamentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TipoScontoMaggiorazioneType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('Art73Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TipoCassaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TipoDocumentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TipoRitenutaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('RiferimentoNumeroLineaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('SoggettoEmittenteType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('RegimeFiscaleType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CondizioniPagamentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('ModalitaPagamentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('IBANType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('BICType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('RitenutaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('EsigibilitaIVAType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('NaturaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CodiceFiscaleType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CodiceFiscalePFType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CodEORIType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('SocioUnicoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('StatoLiquidazioneType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TipoCessionePrestazioneType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TitoloType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String10Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String15Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String20Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String35Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String60Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String80Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String100Type',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String60LatinType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String80LatinType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String100LatinType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String200LatinType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('String1000LatinType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('ProvinciaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('NazioneType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('DivisaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TipoResaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('NumeroCivicoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('BolloVirtualeType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('TelFaxType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('EmailType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('PesoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('Amount8DecimalType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('Amount2DecimalType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('RateType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('RiferimentoFaseType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('NumeroColliType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('NumeroLineaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CAPType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('ABIType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('CABType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('GiorniTerminePagamentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('QuantitaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('DataFatturaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'ST'),
                                                                   ('FatturaElettronicaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('FatturaElettronicaHeaderType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('FatturaElettronicaBodyType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiTrasmissioneType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('IdFiscaleType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('ContattiTrasmittenteType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiGeneraliType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiGeneraliDocumentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiRitenutaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiBolloType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiCassaPrevidenzialeType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('ScontoMaggiorazioneType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiSALType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiDocumentiCorrelatiType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiDDTType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiTrasportoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('IndirizzoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('FatturaPrincipaleType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('CedentePrestatoreType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiAnagraficiCedenteType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('AnagraficaType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiAnagraficiVettoreType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('IscrizioneREAType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('ContattiType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('RappresentanteFiscaleType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiAnagraficiRappresentanteType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('CessionarioCommittenteType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('RappresentanteFiscaleCessionarioType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiAnagraficiCessionarioType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiBeniServiziType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiVeicoliType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiPagamentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DettaglioPagamentoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('TerzoIntermediarioSoggettoEmittenteType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiAnagraficiTerzoIntermediarioType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('AllegatiType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DettaglioLineeType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('CodiceArticoloType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('AltriDatiGestionaliType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT'),
                                                                   ('DatiRiepilogoType',
                                                                    'ya_fattura_elettronica_generator\\package_data\\Schema_del_file_xml_FatturaPA_versione_1.2.xsd',
                                                                    'CT')],
 'http://www.w3.org/2000/09/xmldsig#': [('CryptoBinary',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'ST'),
                                        ('DigestValueType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'ST'),
                                        ('HMACOutputLengthType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'ST'),
                                        ('SignatureType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('SignatureValueType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('SignedInfoType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('CanonicalizationMethodType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('SignatureMethodType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('ReferenceType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('TransformsType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('TransformType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('DigestMethodType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('KeyInfoType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('KeyValueType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('RetrievalMethodType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('X509DataType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('X509IssuerSerialType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('PGPDataType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('SPKIDataType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('ObjectType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('ManifestType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('SignaturePropertiesType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('SignaturePropertyType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('DSAKeyValueType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT'),
                                        ('RSAKeyValueType',
                                         'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd',
                                         'CT')]}

__all__ = [
    "AllegatiType",
    "AltriDatiGestionaliType",
    "AnagraficaType",
    "CanonicalizationMethodType",
    "CedentePrestatoreType",
    "CessionarioCommittenteType",
    "CodiceArticoloType",
    "ContattiTrasmittenteType",
    "ContattiType",
    "DSAKeyValueType",
    "DatiAnagraficiCedenteType",
    "DatiAnagraficiCessionarioType",
    "DatiAnagraficiRappresentanteType",
    "DatiAnagraficiTerzoIntermediarioType",
    "DatiAnagraficiVettoreType",
    "DatiBeniServiziType",
    "DatiBolloType",
    "DatiCassaPrevidenzialeType",
    "DatiDDTType",
    "DatiDocumentiCorrelatiType",
    "DatiGeneraliDocumentoType",
    "DatiGeneraliType",
    "DatiPagamentoType",
    "DatiRiepilogoType",
    "DatiRitenutaType",
    "DatiSALType",
    "DatiTrasmissioneType",
    "DatiTrasportoType",
    "DatiVeicoliType",
    "DettaglioLineeType",
    "DettaglioPagamentoType",
    "DigestMethodType",
    "DigestValueType",
    "FatturaElettronicaBodyType",
    "FatturaElettronicaHeaderType",
    "FatturaElettronicaType",
    "FatturaPrincipaleType",
    "IdFiscaleType",
    "IndirizzoType",
    "IscrizioneREAType",
    "KeyInfoType",
    "KeyValueType",
    "ManifestType",
    "ObjectType",
    "PGPDataType",
    "RSAKeyValueType",
    "RappresentanteFiscaleCessionarioType",
    "RappresentanteFiscaleType",
    "ReferenceType",
    "RetrievalMethodType",
    "SPKIDataType",
    "ScontoMaggiorazioneType",
    "SignatureMethodType",
    "SignaturePropertiesType",
    "SignaturePropertyType",
    "SignatureType",
    "SignatureValueType",
    "SignedInfoType",
    "TerzoIntermediarioSoggettoEmittenteType",
    "TransformType",
    "TransformsType",
    "X509DataType",
    "X509IssuerSerialType"
]
