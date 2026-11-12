# -*- coding: utf-8 -*-
"""V66 planning/verification probe: runs full route to current endpoint, dumps 34F."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '34'
import z2_route
sys.exit(z2_route.main())
