var pass_allow = true;
var i = 0;
_global.Player.Delay = 6;
i = 0;
while(i < 121)
{
   if(_global.Obj_array[46][i] == 110)
   {
      pass_allow = false;
   }
   i++;
}
_global.EndGridNo = 16;
if(!pass_allow)
{
   _global.CurObj_array[16].IconNo = 52;
   _global.CurObj_array[16].EventNo = -1027;
   _global.CurObj_array[27].IconNo = 229;
   _global.CurObj_array[27].EventNo = 0;
   _global.SubEvent_str = "MessageEnd";
   _global.Message_mc_dsp(25);
   gotoAndStop(1);
}
