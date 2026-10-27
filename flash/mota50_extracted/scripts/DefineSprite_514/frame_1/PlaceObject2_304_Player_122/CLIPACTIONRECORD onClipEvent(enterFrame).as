onClipEvent(enterFrame){
   if(_global.Player.Delay > 0)
   {
      _global.Player.Delay--;
      return undefined;
   }
   if(_global.Player.Act_str == "")
   {
      if(_global.MainEvent_str == "PlayerActive")
      {
         _global.MainEvent_str = "";
      }
      return undefined;
   }
   if(_global.Player.Act_str == "Stop")
   {
      _global.Player_stand(this);
      return undefined;
   }
   switch(_global.SubEvent_str)
   {
      case "PlayerMoving":
         _global.Icon_mc_move(this,_global.CurObj_array[_global.EndGridNo]._x,_global.CurObj_array[_global.EndGridNo]._y,_global.Player.Speed);
         if(this._x == _global.CurObj_array[_global.EndGridNo]._x && this._y == _global.CurObj_array[_global.EndGridNo]._y)
         {
            _global.Player_onArrive();
         }
         break;
      case "PlayerMagicDamage":
         _global.Player_onActCheck();
         break;
      case "BeforeOffense":
         _global.Player.Delay = 1;
         _global.SubEvent_str = "PlayerOffense";
         _global.Player_mc_BeforeOffense();
         if(_global.Player.Life <= 0)
         {
            _global.Player.Delay = 0;
            _global.Player.Life = 0;
            _global.MainEvent_str = "PlayerDead";
            _global.Player.Act_str = "PlayerDead";
            _global.Message_mc_dsp(80);
         }
         _global.Player_dspLife(_global.Player.Life);
         break;
      case "PlayerOffense":
         _global.Player.Delay = 1;
         _global.SubEvent_str = "BeforeDefense";
         _global.Player_mc_Offense();
         _global.CurEnemy.Life -= _global.CurEnemy.PlayerOffense;
         break;
      case "BeforeDefense":
         _global.Player.Delay = 1;
         _global.SubEvent_str = "PlayerDefense";
         _global.Player_mc_BeforeDefense();
         if(_global.CurEnemy.Life <= 0)
         {
            _global.Player.Delay = 0;
            _global.SubEvent_str = "EnemyDead";
            _global.Player_onEnemyDead();
         }
         else
         {
            _global.CurEnemy_dspLife(_global.CurEnemy.Life);
         }
         break;
      case "PlayerDefense":
         _global.Player.Delay = 1;
         _global.SubEvent_str = "BeforeOffense";
         _global.Player_mc_Defense();
         _global.Player.Life -= _global.CurEnemy.EnemyOffense;
   }
}
