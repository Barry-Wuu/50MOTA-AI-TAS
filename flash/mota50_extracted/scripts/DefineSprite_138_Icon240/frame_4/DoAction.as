if(_global.MessageNo == 46)
{
   _global.CurObj_array[5].IconNo = 101;
   _global.CurObj_array[5].EventNo = 0;
   _global.Icon_mc_crt(5);
   _global.CurObj_array[60].IconNo = 28;
   _global.CurObj_array[60].EventNo = 0;
   _global.Icon_mc_crt(60);
   _global.ObjGridNo = 60;
}
_global.Message_mc_dsp(_global.MessageNo);
