onClipEvent(keyDown){
   if(_global.Player.Delay > 0)
   {
      return undefined;
   }
   var key_code = Key.getCode();
   if(_global.Player.Act_str != "" || _global.MainEvent_str != "")
   {
      return undefined;
   }
   _global.MainEvent_str = "PlayerActive";
   switch(key_code)
   {
      case 38:
         this.Up_mc._visible = true;
         this.Down_mc._visible = false;
         this.Left_mc._visible = false;
         this.Right_mc._visible = false;
         this.Fight_mc._visible = false;
         _global.EndGridNo = _global.CurUpNo;
         break;
      case 40:
         this.Down_mc._visible = true;
         this.Up_mc._visible = false;
         this.Left_mc._visible = false;
         this.Right_mc._visible = false;
         this.Fight_mc._visible = false;
         _global.EndGridNo = _global.CurDownNo;
         break;
      case 37:
         this.Left_mc._visible = true;
         this.Up_mc._visible = false;
         this.Down_mc._visible = false;
         this.Right_mc._visible = false;
         this.Fight_mc._visible = false;
         _global.EndGridNo = _global.CurLeftNo;
         break;
      case 39:
         this.Right_mc._visible = true;
         this.Up_mc._visible = false;
         this.Down_mc._visible = false;
         this.Left_mc._visible = false;
         this.Fight_mc._visible = false;
         _global.EndGridNo = _global.CurRightNo;
         break;
      default:
         _global.MainEvent_str = "";
         return undefined;
   }
   _global.Player.Direction = key_code;
   _global.Msg_str(key_code);
   _global.Player_onBeforeMoving(_global.EndGridNo);
   if(_global.SubEvent_str != "PlayerMoving")
   {
      _global.Player_stand(this);
   }
   else
   {
      _global.Player_mc_walk(true);
   }
}
