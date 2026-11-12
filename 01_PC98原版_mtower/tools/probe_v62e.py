# -*- coding: utf-8 -*-
"""V62 verification probe: runs full route to V62 endpoint, dumps 32F."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['MOTA_PROBE_FLOOR'] = '32'
import z2_route
sys.exit(z2_route.main())
