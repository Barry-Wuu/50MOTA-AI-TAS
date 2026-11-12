# -*- coding: utf-8 -*-
"""V65 verification probe: runs full route to V65 endpoint, dumps 7F."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '7'
import z2_route
sys.exit(z2_route.main())
