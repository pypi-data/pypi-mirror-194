import re
from collections.abc import Mapping
from collections import OrderedDict


def merge_dics(dict_ref, dict_opt):
    """
    mergeia dicionarios dict_ref e dict_opt

    - remove valores "nulos"
    - em caso de colisoes, considera o dict_ref como referencia

    """

    def cleanup(dicio):
        return {k: v for k, v in dicio.items() if v not in ('', None)}

    ref = cleanup(dict_ref)
    opt = cleanup(dict_opt)
    for k, v_opt in opt.items():
        v_ref = ref.get(k, v_opt)
        if isinstance(v_ref, Mapping):
            ref[k] = merge_dics(v_ref, v_opt)
        else:
            ref[k] = ref.get(k, v_opt)

    return ref


def flatten_dict(d, prepend=''):
    """
    Transforma um dicionario de muitas camadas em uma estrutura de unica camada

    :param d: objeto dict-like
    :param prepend: string a ser "prependada" + _ a cada chave
    :return: generator de tuplas chave-valor
    """

    for k, v in d.items():
        prepended_k = f'{prepend}_{k}' if prepend else k

        if isinstance(v, Mapping):
            for tp in flatten_dict(v, prepend=prepended_k):
                yield tp
        else:
            yield prepended_k, v


def camel2snake(name):
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def snake_dict_keys(d):
    def _convert_seq(s):
        for el in s:
            if isinstance(el, Mapping):
                yield snake_dict_keys(el)
            else:
                yield el

    new_d = OrderedDict() if isinstance(d, OrderedDict) else {}

    for k, v in d.items():

        new_k = camel2snake(k)
        if isinstance(v, Mapping):
            new_v = snake_dict_keys(v)

        elif isinstance(v, list):
            new_v = list(_convert_seq(v))

        else:
            new_v = v

        new_d[new_k] = new_v

    return new_d
