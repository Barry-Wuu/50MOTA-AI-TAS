# -*- coding: utf-8 -*-
"""V63 verification probe: runs full route to V63 endpoint, dumps 39F."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '39'
import z2_route
sys.exit(z2_route.main())
