if(_global.MainEvent_str == "MessageEnd")
{
   _global.Message_mc_dsp(40);
}
else
{
   gotoAndPlay(_currentframe - 1);
}
