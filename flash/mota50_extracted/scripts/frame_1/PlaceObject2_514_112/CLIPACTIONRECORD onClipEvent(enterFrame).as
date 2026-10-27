onClipEvent(enterFrame){
   if(_global.StageDelay > 0)
   {
      _global.StageDelay--;
   }
   if(_global.StageAct_str == "")
   {
      if(_global.MainEvent_str == "StageActive")
      {
         _global.MainEvent_str = "";
      }
      return undefined;
   }
   if(_global.StageAct_str === "StageChange")
   {
      if(SubEvent_str == "Stair")
      {
         _global.SubEvent_str = "StageClose";
      }
      else
      {
         _global.SubEvent_str = "StageChg";
      }
      switch(_global.SubEvent_str)
      {
         case "StageClose":
            _global.SubEvent_str = "StageChg";
            break;
         case "StageChg":
            _global.Stage_save();
            _global.Stage_load();
            _global.StageAct_str = "";
            break;
         case "StageOpen":
      }
   }
}
