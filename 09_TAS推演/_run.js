const fs = require('fs');
const code0 = fs.readFileSync(process.argv[2], 'utf8');
const idx = parseInt(process.argv[3] || '0', 10);
const code = code0.replace(/select\(0\);\s*\}\)\(\);/, 'select(' + idx + ');})();');
function El(id){
  const o = {
    id, style:{setProperty(){}, getPropertyValue(){return '';}}, dataset:{}, _html:'', textContent:'', value:'', src:'',
    classList:{add(){},remove(){},toggle(){},contains(){return false;}},
    addEventListener(){}, querySelector(){return null;}, querySelectorAll(){return [];},
    scrollIntoView(){}, appendChild(){}, setAttribute(){},
  };
  Object.defineProperty(o,'innerHTML',{get(){return o._html;},set(v){o._html=String(v);}});
  Object.defineProperty(o,'onclick',{get(){return null;},set(v){}});
  return o;
}
const els = {};
global.document = {
  getElementById(id){ return els[id] || (els[id] = El(id)); },
  querySelectorAll(){ return []; },
  createElement(){ return El('tmp'); },
  head:{appendChild(){}},
  addEventListener(){},
};
try{
  eval(code);
  console.log('RUN OK idx=' + idx);
  console.log('  marker:', els['marker'].style.left, els['marker'].style.top, 'dir', els['dirbadge'].textContent);
  console.log('  heroImg src len:', String(els['heroImg'].src).length);
  console.log('  floorname:', els['floorname'].innerHTML);
  console.log('  posline:', els['posline'].innerHTML);
  console.log('  statSub:', els['stateSub'].textContent);
  console.log('  tblTitle/Sub:', els['tblTitle'].textContent, '|', els['tblSub'].textContent);
  console.log('  bg set:', String(els['mapbox'].style.backgroundImage).slice(0,26));
  console.log('  patchLayer:', els['patchLayer']._html.slice(0,120));
  console.log('  cons divs:', (els['consumeLayer']._html.match(/class="cons/g)||[]).length,
              '| kinds:', (els['consumeLayer']._html.match(/class="cons k[a-z]/g)||[]).slice(0,6).join(','));
}catch(e){
  console.log('RUN ERROR idx=' + idx + ':', e && e.stack || e);
  process.exit(1);
}
