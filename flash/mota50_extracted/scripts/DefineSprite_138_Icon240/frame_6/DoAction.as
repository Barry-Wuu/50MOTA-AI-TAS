if(_global.MainEvent_str != "MessageEnd")
{
   gotoAndPlay(_currentframe - 1);
}
else
{
   switch(_global.MessageNo)
   {
      case 41:
         _global.ObjGridNo = 37;
         break;
      case 42:
         _global.ObjGridNo = 39;
         break;
      case 43:
         _global.ObjGridNo = 14;
         break;
      case 44:
         _global.ObjGridNo = 18;
         break;
      case 45:
         _global.ObjGridNo = 5;
         break;
      case 46:
         gotoAndPlay(10);
   }
}
