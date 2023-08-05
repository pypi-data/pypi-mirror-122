import json
import datetime
from itertools import chain, starmap


def jstone(js_obj):
    '''
    convert any parsed json object into a jstone object:
    a flattened dictionary of tuple path keys _  indices & values
    '''
    more = True
    
    if type(js_obj) not in (dict, list):
        js_obj = {
            tuple(): js_obj
        }
        more = False
    
    elif not js_obj:
        js_obj = {
                tuple(): type(js_obj),
        }
        more = False
    
    else:
        js_obj = {
            tuple(): js_obj
        }

    def unpack(parent_key, parent_value):

        if isinstance(parent_value, dict) and parent_value:
            yield parent_key, dict
            for key, value in parent_value.items():
                yield (
                    (*parent_key, key, ), 
                    value if not (
                        value in ({}, []) and not value
                    ) else type(value),
                )
                
        elif isinstance(parent_value, list) and parent_value:
            yield parent_key, list
            for i in range(len(parent_value)):
                yield (
                    (*parent_key, (i, ), ), 
                    parent_value[i] if not (
                        parent_value[i] in ({}, []) and not parent_value[i]
                    ) else type(parent_value[i]),
                )
                
        else:
            yield parent_key, parent_value

    if more:
        while (
            any(type(value) in (dict, list) for value in js_obj.values())
        ):
            js_obj = dict(chain.from_iterable(starmap(unpack, js_obj.items())))

    return js_obj


def render_lists(set_of_lists, new_obj):
    '''
    takes prebuild set_of_lists and converts 
    dict representations of lists to lists in new_obj
    '''
    for i in sorted(set_of_lists, key=lambda x: len(x), reverse=True):

        if follow(new_obj, i, rebuild=True):
            if i == tuple():
                new_obj = [i[1] for i in sorted(follow(new_obj, i, rebuild=True).items())]
            else:
                follow(new_obj, i[:-1], rebuild=True)[i[-1]] = [i[1] for i in sorted(follow(new_obj, i, rebuild=True).items())]
                            
        else:
            if i == tuple():
                new_obj = []
            else:
                follow(new_obj, i[:-1], rebuild=True)[i[-1]] = []

    return new_obj


def prebuild(jstone_obj):
    '''
    creates object with tuple keyed dicts for lists
    and a set of lists from a jstone formatted object
    '''
    set_of_lists = set()

    if tuple() in jstone_obj and jstone_obj[tuple()] not in [dict, list]:
        new_obj = jstone_obj[tuple()]
    else:
        if tuple() in jstone_obj and jstone_obj[tuple()] == list:
            set_of_lists.add(tuple())
            new_obj = {}
        else:
            new_obj = {}

        if any([len(i) for i in jstone_obj]):
            
            for i in jstone_obj:
                                
                if jstone_obj[i] == list:

                    set_of_lists.add(i)

                for j in range(len(i)):
                                        
                    if type(i[j]) == tuple:

                        set_of_lists.add(i[:j])

                    if i[j] not in follow(new_obj, i[:j], rebuild=True):

                        if j != len(i)-1:

                            follow(new_obj, i[:j], rebuild=True)[i[j]] = {}

                        elif jstone_obj[i] not in (dict, list) or i[j] not in follow(new_obj, i[:j], rebuild=True):

                            follow(new_obj, i[:j], rebuild=True)[i[j]] = jstone_obj[i] if jstone_obj[i] not in (dict, list) else {}
    
    return {
        'new_obj': new_obj,
        'set_of_lists': set_of_lists,
    }


def rebuild(jstone_obj):
    
        pre = prebuild(jstone_obj)
            
        return render_lists(pre['set_of_lists'], pre['new_obj'])


def follow(js_obj, path, rebuild=False):
    '''
    given a parsed json object and tuple of keys and indices as a path 
    return the value in the object at the given path
    '''
    val = js_obj
    
    for step in path:
    
        if not rebuild and type(step) == tuple:
            val = val[step[0]]
        
        else:
            val = val[step]
    
    return val
