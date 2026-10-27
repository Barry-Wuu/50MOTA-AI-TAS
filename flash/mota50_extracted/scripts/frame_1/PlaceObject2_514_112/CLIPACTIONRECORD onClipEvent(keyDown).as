onClipEvent(keyDown){
   if(_global.StageDelay > 0)
   {
      return undefined;
   }
   switch(Key.getCode())
   {
      case 32:
         _global.Help_mc_dsp();
         break;
      case 76:
         _global.Load_mc_dsp();
         break;
      case 82:
         _global.Game_reset();
         break;
      case 83:
         _global.Game_save(0);
         break;
      case 72:
         _global.Dict_mc_dsp();
         break;
      case 78:
         _global.Note_mc_dsp();
         break;
      case 33:
         _global.calcFlyUp();
         break;
      case 34:
         _global.calcFlyDown();
         break;
      case 68:
         _global.calcJumpdown();
         break;
      case 74:
         _global.calcJump();
         break;
      case 85:
         _global.calcJumpUp();
         break;
      case 73:
         _global.calcIce();
         break;
      case 80:
         _global.calcPick();
         break;
      case 81:
         _global.calcQuake();
         break;
      case 75:
         _global.calcKeyMagic();
         break;
      case 66:
         _global.calcBomb();
         break;
      case 87:
         _global.calcHoly();
   }
}
