_global.MainEvent_str = "";
_global.CurObj_array[_global.EndGridNo].Icon = 100;
if(_global.Curobj_array[15].IconNo == 27 && _global.Curobj_array[17].IconNo == 27 && _global.Curobj_array[37].IconNo == 27 && _global.Curobj_array[39].IconNo == 27 && _global.CurObj_array[27].IconNo == 31)
{
   _global.Enemy_array[31].Life /= 10;
   _global.Enemy_array[31].Offense /= 10;
   _global.Enemy_array[31].Defense /= 10;
   _global.SubEvent_str = "MessageEnd";
   _global.Message_mc_dsp(60);
}
