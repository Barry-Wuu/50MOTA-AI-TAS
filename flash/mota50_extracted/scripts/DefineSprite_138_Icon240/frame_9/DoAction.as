if(_global.CurEventEnd)
{
   _global.CurObj_array[0].EventNo = -1;
   _global.CurObj_array[71].IconNo = _global.CurObj_array[_global.ObjGridNo].IconNo;
   _global.CurObj_array[71].EventNo = 1000;
   _global.Icon_mc_crt(71);
   _global.CurEnemy_set(71);
   _global.MainEvent_str = "PlayerWait";
   _global.Player.Act_str = "Fighting";
   _global.SubEvent_str = "BeforeDefense";
   _global.Icon_mc_cls(_global.ObjGridNo);
   switch(_global.ObjGridNo)
   {
      case 37:
      case 36:
      case 14:
      case 13:
         _global.ObjGridNo--;
         gotoAndStop(7);
         break;
      case 18:
      case 19:
      case 39:
      case 40:
         _global.ObjGridNo = _global.ObjGridNo + 1;
         gotoAndStop(7);
         break;
      case 5:
      case 12:
      case 20:
      case 35:
      case 41:
         _global.MessageNo = _global.MessageNo + 1;
         gotoAndStop(3);
   }
}
else
{
   gotoAndPlay(_currentframe - 1);
}
