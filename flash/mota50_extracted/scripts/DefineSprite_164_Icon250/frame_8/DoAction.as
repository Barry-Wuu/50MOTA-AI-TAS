if(_global.MainEvent_str != "MessageEnd")
{
   gotoAndPlay(_currentframe - 1);
}
else
{
   _global.MessageNo = _global.MessageNo + 1;
}
