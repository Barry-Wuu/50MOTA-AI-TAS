var i = 0;
if(_global.CurObj_array[52].IconNo != 0)
{
   _global.CurObj_array[52].EventNo = -107;
   i++;
}
if(_global.CurObj_array[54].IconNo != 0)
{
   _global.CurObj_array[54].EventNo = -107;
   i++;
}
if(_global.CurObj_array[74].IconNo != 0)
{
   _global.CurObj_array[74].EventNo = -107;
   i++;
}
if(_global.CurObj_array[76].IconNo != 0)
{
   _global.CurObj_array[76].EventNo = -107;
   i++;
}
if(i > 0)
{
   _global.CurObj_array[42].IconNo = 107;
   _global.CurObj_array[42].EventNo = - i;
   _global.CurObj_array[86].IconNo = 107;
   _global.CurObj_array[86].EventNo = - i;
   _global.Icon_mc_crt(42);
   _global.Icon_mc_crt(86);
}
_global.MainEvent_str = "";
_global.CurObj_array[43].IconNo = 100;
_global.CurObj_array[43].EventNo = 0;
_global.Icon_mc_crt(43);
