#!/usr/bin/env python
# coding: utf-8
# BASE


import numpy as np
import pandas as pd
import sys

from datetime import datetime
from copy import deepcopy
from math import sqrt

N_EMPTY  = 1
X_TUMOR = 2     
Y_CYTOTOXIC = 3
ZX_IMMCOMPLEX = 4
ZY_IMMCOMPLEX = 5
P_DEAD  = 6