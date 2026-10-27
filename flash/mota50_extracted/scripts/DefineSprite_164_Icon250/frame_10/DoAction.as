_root.Stage_mc[_global.CurObj_array[49].mcName]._alpha -= 4;
if(_root.Stage_mc[_global.CurObj_array[49].mcName]._alpha > 5)
{
   gotoAndPlay(_currentframe - 1);
}
else
{
   _global.CurObj_array[49].IconNo = 31;
   _global.CurObj_array[49].EventNo = -1001;
   _global.Icon_mc_crt(49);
   _root.Stage_mc[_global.CurObj_array[49].mcName]._alpha = 0;
}
