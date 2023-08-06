# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2023.03.01
version: 2023.03.01
function: Some useful tools
"""

import os, sys, re, time
from decimal import Decimal
from glob import glob
from pathlib import Path
from tqdm import tqdm
import _pickle as pickle
from func_timeout import func_set_timeout, func_timeout
import numpy as np
from joblib import Parallel, delayed

__author__ = 'Bowei Pu'
__version__ = '2023.02.21'
__maintainer__ = 'Bowei Pu'
__email__ = 'pubowei@foxmail.com'
__status__ = 'Beta'
__date__ = '2023-02-21'


def time_parser(sec):
    s = int(sec)
    m, sec = s // 60, s % 60
    h, mins = m // 60, m % 60
    day, hour = h // 24, h % 24
    return {'day': day, 'hour': hour, 'min': mins, 'sec': sec, 's': s}


class PickleDump():
    '''
    Easy usage for pickle
    '''
    def __init__(self):
        self._function = 'Easy usage for pickle'
    
    @classmethod
    def dump(cls, obj, file_obj):
        pickle.dump(obj, file_obj)
    
    @classmethod
    def load(cls, file_obj):
        return pickle.load(file_obj)
    
    @classmethod
    def save(cls, obj, file):
        if not os.path.exists(Path(file).parent):
            os.makedirs(Path(file).parent)
        with open(file, 'wb') as f:
            cls.dump(obj, f)
    
    @classmethod
    def read(cls, file):
        with open(file, 'rb') as f:
            return cls.load(f)



class DictDoc():
    '''
    Dict to class
    Designed to compatible with MPDoc
    '''
    def __init__(self, dic: dict={}):
        self.dic = dic
        self._generate_attributes()
    
    def __repr__(self):
        if hasattr(self, 'structure'):
            return '<DictDoc: {}>'.format(self.structure.formula)
        else:
            return '<DictDoc: >'
    
    def __str__(self):
        return self.__repr__()
        
    def dict(self):
        return self.dic
    
    def as_dict(self):
        return self.dic
    
    def keys(self):
        return self.dic.keys()
    
    def values(self):
        return self.dic.values()
    
    def _generate_attributes(self):
        for k, v in self.dic.items():
            setattr(self, k, v)
    
    def setattr(self, name, value):
        self.dic[name] = value
        setattr(self, name, value)
    
    def add(self, name, value):
        self.setattr(name, value)
    
    def get_light_doc(self, reserve=[]):
        reserves = ['formula_pretty', 'formula_anonymous', 'chemsys',
                    'property_name', 'material_id', 'es_source_calc_id',
                    'ordering', 'database_version']
        reserves += ['nsites', 'nelements', 'num_magnetic_sites', 
                     'num_unique_magnetic_sites']
        reserves += ['volume', 'density', 'density_atomic',
                     'uncorrected_energy_per_atom', 'energy_per_atom',
                     'formation_energy_per_atom', 'energy_above_hull',
                     'band_gap', 'cbm', 'vbm', 'efermi',
                     'total_magnetization',
                     'total_magnetization_normalized_vol',
                     'total_magnetization_normalized_formula_units']
        reserves += ['deprecated', 'is_stable', 'is_gap_direct',
                     'is_metal',  'is_magnetic', 'theoretical']
        reserves += ['elements', 'composition', 'composition_reduced', 
                     'decomposes_to', 'symmetry', 'structure', 'task_ids', 
                     'possible_species', 
                     'guess_oxi_states', 'oxi_states']
        reserves += reserve
        return self.__class__({i: self.__getattribute__(i) 
                               for i in reserves if i in self.__dir__()})


