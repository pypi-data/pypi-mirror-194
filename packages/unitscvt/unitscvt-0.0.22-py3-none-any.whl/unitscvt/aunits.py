#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:47:09 2022

@author: lucas

Convert rates from Hartree atomic units to SI
"""
# %% Atomic Units to SI
Planck = 6.62607015e-34 # [J/Hz]
'Planck constant to Joules per Hz (energy to frequency)'
redPlanck = 1.054571817e-34  # [J.s]
'reduced Planck constant to Joules sec (energy to time)'
eCharge = 1.602176634e-19 # [C]
'elementary charge in Coulombs'
BohrRadius = 5.29177210903e-11 # [m]
'Bohr radius in meter'
masselectron = 9.1093837015e-31 # [kg]
'electron rest mass in kg'
HartreeEnergy = 4.3597447222071e-18 # [J]
'Hartree energy in Joules'
HEeV = HartreeEnergy/1.602176634e-19 # [eV]
'Hartree energy in eV'
Dalton = 1.66053906660e-27 # [kg]
'unified atomic mass unit in kilograms'

# %% Derived Units to SI
edipolemoment = eCharge*BohrRadius # [Cm]
'electric dipole moment to Coulomb meter'
edipolemomentDebye = 2.541746473 # [D]
'electric dipole moment to Debye, not SI'
elecPotential = HartreeEnergy/eCharge # [V]
'electric potential in Volts'
autime = redPlanck/HartreeEnergy # [s]
'atomic unit of time in seconds, ~240fs'
auvelocity = BohrRadius*HartreeEnergy/redPlanck # [m/s]
'atomic unit of velocity in meter per sec'

# %% hbar == 1; m == 1; e**2 == 1; Old version, to delete soon
# '''length'''
# a0 = 5.29177249e-1           # Bohr radius to meter a0:[Å]
# '''velocity'''
# v0 = 2.18769142e6            # electron velocity 1st Bohr orbit v0:[m/s]
# '''time'''
# tau0 = 2.41888433e-17        # a0/v0=tau0:[s]
# '''frequency'''
# nu0 = 1/tau0                 # inverse of time 1/tau0=nu0:[Hz]
# '''energy'''
# Eau = 27.2113962             # 2x hydrogen binding energy Eau:[eV]
 
# '''mass'''
# Mu = 9.10953e-31             # atomic mass Mu:[Kg]
# me = 5.4858e-04              # electron rest mass in atomic mass units me:[uA]
# '''Planck'''
# hbar = 6.58212e-16           # hbar:[ev.s] 
# ev2J = 1.602176565e-19       # eV:[J] 

# '''Electromagnetic'''
# c = 299792458
# mu0 = 1.25663706212e-6       # permeability [N/A^2]
# ep0 = 1/c**2/mu0             # permitivitty [F/m] 

# E0 = 5.14220826e11           # unit of electric field strength [V/m]




