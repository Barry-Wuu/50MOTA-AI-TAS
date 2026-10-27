if(_global.MainEvent_str == "MessageEnd")
{
   _global.Message_mc_dsp(4);
}
else
{
   gotoAndPlay(_currentframe - 1);
}
