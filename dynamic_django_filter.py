from django.db.models import Q

def get_and_args(**kwargs):
    """take the key_word argument value with value as list 
       calculate the equivalent And query as args
       return the args to use as And filter 
    """
    args_list = [Q(),]
    for key , value in kwargs.iteritems() :
        column = "%s__in" %(key)

        _null, _ids = get_sanitize_value( value )

        if _ids :
            x = Q(**{column:_ids})
        if _null :
            x = x | Q(**{key:None})

	args_list.append(x)
    _args = reduce(lambda x, y: x & y, args_list)
    return (_args, ) 

def get_sanitize_value(_value):
    """
        This methods takes the list input from filter criteria and returns if_null_filter_required, ids
        Check whether Null filter required and sanitize the given ids as well
    """
    _null = False
    _nullable = ('blank', 'None', '', None)
    if not isinstance(_value, (list)):
        return _null, _value
    _null = True if (set(_value).intersection(_nullable)) else False   
    _ids = sorted([x for x in _value if x not in _nullable])
    return _null, _ids
