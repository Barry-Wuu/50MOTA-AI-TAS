_global.CurObj_array[_global.EndGridNo].IconNo = 247;
var grid_no = -1;
var grid1_no = -1;
var grid2_no = -1;
var event_no = 0;
var i = 0;
while(i < 4)
{
   switch(i)
   {
      case 0:
         grid_no = _global.CurUpNo;
         grid1_no = _global.CurUpNo - 11;
         grid2_no = _global.CurUpNo - 22;
         break;
      case 1:
         var grid_no = _global.CurDownNo;
         if(grid_no > 0 && grid_no < 110)
         {
            grid1_no = _global.CurDownNo + 11;
            grid2_no = _global.CurDownNo + 22;
         }
         else
         {
            grid1_no = -1;
            grid2_no = -1;
         }
         break;
      case 2:
         var grid_no = _global.CurLeftNo;
         if(grid_no % 11 > 1)
         {
            grid1_no = _global.CurLeftNo - 1;
         }
         else
         {
            grid1_no = -1;
         }
         if(grid_no % 11 > 2)
         {
            grid2_no = _global.CurLeftNo - 2;
         }
         else
         {
            grid2_no = -1;
         }
         break;
      case 3:
         var grid_no = _global.CurRightNo;
         if(grid_no % 11 < 10)
         {
            grid1_no = _global.CurLeftNo - 1;
         }
         else
         {
            grid1_no = -1;
         }
         if(grid_no % 11 < 9)
         {
            grid2_no = _global.CurLeftNo - 2;
         }
         else
         {
            grid2_no = -1;
         }
   }
   if(grid1_no < 0 || grid1_no > 120)
   {
      grid_no = -1;
   }
   if(grid_no >= 0 && grid_no <= 120)
   {
      if(_global.CurObj_array[grid_no].IconNo == 26)
      {
         _global.CurObj_array[grid_no].IconNo = 0;
         var event_no = _global.CurObj_array[grid1_no].EventNo;
         _global.CurObj_array[grid1_no].IconNo = 26;
         _global.CurObj_array[grid1_no].EventNo = _global.CurObj_array[grid_no].EventNo;
         _global.CurObj_array[grid_no].EventNo = 0;
         _global.Icon_mc_cls(grid_no);
         _global.Icon_mc_crt(grid1_no);
         if(grid2_no >= 0 && grid2_no <= 120)
         {
            if(_global.CurObj_array[grid2_no].IconNo == 0)
            {
               _global.CurObj_array[grid2_no].EventNo = event_no;
               _global.CurObj_array[grid_no].EventNo = event_no;
            }
         }
      }
   }
   i++;
}
