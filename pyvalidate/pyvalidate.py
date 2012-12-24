'''
pyvalidate

Created on Oct 25, 2010

@author: Vahid Mardani 
'''


import re

class ValidationException(Exception):
    pass 

class ArgumentTypeException(ValidationException):
    pass

class MandatoryException(ValidationException):
    pass

class DenialException(ValidationException):
    pass

class ParameterTypeException(ValidationException):
    pass

class ParameterValueException(ValidationException):
    pass

def validate_parameters(args, kwargs, arg_types=None
                                     , deny_match=None
                                     , requires=None
                                     , deny=None
                                     , deny_except=None
                                     , types=None
                                     , values=None
                                     , ignore=None
                                     , json_decode=None
                                     , defaults=None):
    """Validates input parameters of a callable
    
    @param arg_types:       list of types, Required argument's types  & counts in order
    @param deny_match            list of string ,regex pattern, if any argument matches with the pattern, exception raises
    @param requires:             list of fields to check for mandatory
    @param deny:                 string ,regex pattern, if any parameter matches with the pattern, exception raises
    @param deny_except:          string ,regex pattern for excluding fields from deny
    @param types:                dict of key:name and value:type to check for types, if mismatch it will be raises exception
    @param values:               dict of key:name and value:regex pattern to check the values, & fire exception if mismatch
    @param ignore:               string ,regex pattern of parameters to filter    
    @param defaults:             dict of key:name and value:default_value
    
    @raise MandatoryException:           if any param in requires does not provided
    @raise ArgumentException:            if arguments are invalid , short or mismatch type.
    @raise DenialException:              if found param in deny list
    @raise ParameterTypeException:       if parameter types invalid
    @raise ParameterValueException:      if values are not in correct format
    """

    
    #check deny arguments
    if deny_match:
        if isinstance(deny_match, basestring):
            deny_match = [deny_match]
        for arg in [a  for a in args if isinstance(a, basestring)]:
            for pattern in deny_match: 
                if re.match(pattern, arg):
                    raise DenialException('the argument %s was not allowed' % arg)
    
#    #decoding json parameters
#    if json_decode:
#        decoder = JSONDecoder(parse_float=Decimal)
#        def decode(d):
#            try:
#                return decoder.decode(d)
#            except (JSONDecodeError, TypeError):
#                return d
#
#        if isinstance(json_decode, list):
#            decoded_list = [(key, decode(kwargs[key])) for key in kwargs if key in json_decode]
#        else:
#            decoded_list = [(key, decode(kwargs[key])) for key in kwargs]
#        kwargs.update(decoded_list) 
        
        

    #check required arguments
    if arg_types: 
        try:
            new_args = list(args)
            for index in range(len(arg_types)):
                at = arg_types[index]
                if not isinstance(new_args[index], at):
                    try:
                        #try to cast
                        new_args[index] = at(new_args[index])
                    except:
                        raise ParameterTypeException('argument at index:%s must be %s' % (index, at))
            args = tuple(new_args)
        except IndexError:
            raise ArgumentTypeException('argument\'s length is too short, expected: (%s)' % ','.join([t.__name__ for t in arg_types]))
    
    #check required parameters
    if requires: 
        for name in requires:
            if name not in kwargs:
                raise MandatoryException('the parameter:"%s" is mandatory' % name)
        
    
    filtered_params = {}
    for param in kwargs:
        
        #checking requires
        if requires and param in requires and not kwargs[param]:
            raise MandatoryException('the parameter:"%s" is mandatory' % param)
        
        #checking for denial
        if deny and re.match(deny, param) and  (not deny_except or not re.match(deny_except, param)):
            raise DenialException('Parameter: %s was denied' % param)

        #value checking
        if values and param in values and not re.match(values[param], kwargs[param]):
            raise ParameterValueException('Parameter:%s does not meet value pattern: given value:%s' % (param, kwargs[param]))
        
        #checking for types
        if types and param in types:
            if kwargs[param] and not isinstance(kwargs[param], types[param]):
                try:
                    #try to cast the type too needed type
                    kwargs[param] = types[param](kwargs[param])
                except:
                    raise ParameterTypeException('Parameter:%s must be type:%s, given type:%s' % (param, types[param], type(kwargs[param])))
        
        
        #filtering parameters
        if not ignore or not re.match(ignore, param):
            filtered_params[param] = kwargs[param]
    
    #add defaults if not supplied
    if defaults:
        for param in defaults:
            if param not in filtered_params:
                filtered_params[param] = defaults[param]
    
    return args, filtered_params
    

def validate(**val_cfg):
    def validecorator(func):
        def wrapper(*args, **kwargs):
                if len(func.func_code.co_varnames) and func.func_code.co_varnames[0] == 'self':
                    new_args, filtered_params = validate_parameters(args[1:], kwargs, **val_cfg)
                    return func(*(args[0],) + new_args, **filtered_params)
                else:
                    new_args, filtered_params = validate_parameters(args, kwargs, **val_cfg)
                    return func(*new_args, **filtered_params)
            #calling the callable!
            
        return wrapper
    return validecorator

validate.__doc__ = validate_parameters.__doc__
