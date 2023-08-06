#!/usr/bin/env python
'''
component
Created by Seria at 25/11/2018 2:58 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
from ..kit.utility import cap, autopad
from collections import namedtuple

__all__ = ('Pod', 'Tensor', 'coat', 'shell', 'autopad')

from .craft import *
from . import craft
__all__ += craft.__all__


Tensor = namedtuple('tensor', ('key', 'val'))
def coat(datum, as_const=True, sync=True):
    raise NotImplementedError('NEBULAE ERROR ⨷ coat function becomes valid only after setting up an Engine.')

def shell(datum, as_np=True, sync=False):
    raise NotImplementedError('NEBULAE ERROR ⨷ shell function becomes valid only after setting up an Engine.')


class Pod():
    def __init__(self, name, comp=[], symbol=''):
        self.name = name
        if len(comp)==0: # atomic pod
            self.comp = comp
        else:
            assert len(comp)==2
            left_sym = comp[0].symbol
            right_sym = comp[1].symbol
            if left_sym == right_sym:
                if right_sym=='':
                    self.comp = comp
                else:
                    self.comp = comp[0].comp + comp[1].comp
            else:
                if left_sym=='':
                    self.comp = [comp[0]] + comp[1].comp
                elif right_sym=='':
                    self.comp = comp[0].comp + [comp[1]]
                else:
                    self.comp = comp
        self.symbol = symbol


    def __gt__(self, other):
        return Pod('', [self, other], '>')

    def __add__(self, other):
        return Pod('', [self, other], '+')

    def __sub__(self, other):
        return Pod('', [self, other], '-')

    def __mul__(self, other):
        return Pod('', [self, other], '*')

    def __matmul__(self, other):
        return Pod('', [self, other], '@')

    def __and__(self, other):
        return Pod('', [self, other], '&')

    def __or__(self, other):
        return Pod('', [self, other], '|')

    def __xor__(self, other):
        return Pod('', [self, other], '^')

    def _cap(self, scope):
        if '/' not in self.name:
            self.name = cap(self.name, scope)
        for c in self.comp:
            c._cap(scope)