if(_global.Player.GridNo == _global.EndGridNo - 1 && _global.Player.MaxFloorNo > _global.Player.FloorNo)
{
   _global.CurObj_array[_global.EndGridNo].IconNo = 26;
   _global.CurObj_array[_global.EndGridNo].EventNo = 1006;
   _global.Icon_mc_crt(_global.EndGridNo);
}
else
{
   _global.CurObj_array[_global.EndGridNo].IconNo = 126;
   _global.CurObj_array[_global.EndGridNo].EventNo = 0;
   gotoAndStop(1);
}
