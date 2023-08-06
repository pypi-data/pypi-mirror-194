#!/usr/bin/env python
'''
vae
Created by Seria at 2022/11/3 4:06 PM
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
from ... import dock, Craft
from .architect import ResVQE, ResVQD, VecQuant



class VQVAE(Craft):
    def __init__(self, in_shape, hidden_dim, ncodes, scope='VQVAE'):
        super(VQVAE, self).__init__(scope)
        self.E = ResVQE(in_shape, hidden_dim, ncodes)
        self.D = ResVQD(in_shape, hidden_dim)
        self.Q = VecQuant(ncodes, self.E.ochs[-1])

    def run(self, x):
        z = self.E(x)
        q = self.Q(z)
        s = dock.shell(q-z, as_np=False)
        y = self.D(z+s)
        return z, q, y