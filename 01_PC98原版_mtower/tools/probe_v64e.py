# -*- coding: utf-8 -*-
"""V64 verification probe: runs full route to V64 endpoint, dumps 40F."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '40'
import z2_route
sys.exit(z2_route.main())
