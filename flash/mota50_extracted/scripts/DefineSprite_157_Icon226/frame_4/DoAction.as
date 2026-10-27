if(_global.MainEvent_str != "MessageEnd")
{
   gotoAndPlay(_currentframe - 1);
}
else
{
   _global.Message_mc_dsp(64);
}
