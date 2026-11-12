# -*- coding: utf-8 -*-
"""V60 verification probe: runs full route to V60 endpoint, dumps 38F."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '38'
import z2_route
sys.exit(z2_route.main())
