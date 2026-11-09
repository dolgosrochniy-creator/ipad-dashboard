// Private Supabase photo sync. No service-role key, no public bucket, no deletion.
// Uses the owner's Supabase Auth session stored for this GitHub Pages origin.
import {createClient} from 'https://esm.sh/@supabase/supabase-js@2';
const client=createClient('https://huxnfwmxfrsvgxurgpkn.supabase.co','sb_publishable_iCh1OvLTSrTzp1xbj7jSUg_2-lSut_w',{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:false}});
const DB_NAME='ramka_personal_photos', STORE='images';
function database(){return new Promise((resolve,reject)=>{const req=indexedDB.open(DB_NAME,1);req.onupgradeneeded=()=>{if(!req.result.objectStoreNames.contains(STORE))req.result.createObjectStore(STORE,{keyPath:'id',autoIncrement:true})};req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error)})}
function readAll(db){return new Promise((resolve,reject)=>{const req=db.transaction(STORE,'readonly').objectStore(STORE).getAll();req.onsuccess=()=>resolve(req.result||[]);req.onerror=()=>reject(req.error)})}
function add(db,record){return new Promise((resolve,reject)=>{const tx=db.transaction(STORE,'readwrite');tx.objectStore(STORE).add(record);tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error)})}
let busy=false;
export async function syncFramePhotos(){
 if(busy)return {status:'busy'};busy=true;let db;
 try{
  const {data:{user},error:authError}=await client.auth.getUser();
  if(authError||!user)return {status:'login-required'};
  db=await database();
  const existing=await readAll(db);
  const known=new Set(existing.map(x=>x.remoteKey).filter(Boolean));
  const {data,error}=await client.storage.from('frame-photos').list('',{limit:100,sortBy:{column:'created_at',order:'asc'}});
  if(error)throw error;
  let added=0,failed=0;
  for(const item of (data||[])){
   if(!item.name||item.name.startsWith('.')||known.has(item.name))continue;
   if(!/\.(jpe?g|png|webp|gif|heic|heif)$/i.test(item.name))continue;
   const {data:blob,error:downloadError}=await client.storage.from('frame-photos').download(item.name);
   if(downloadError||!blob){failed++;continue}
   try{await add(db,{blob,name:'remote_'+item.name,originalSize:blob.size,added:Date.now(),remoteKey:item.name});known.add(item.name);added++}catch(e){failed++}
  }
  if(added&&typeof window.ramkaReloadPhotos==='function')window.ramkaReloadPhotos();
  return {status:'ok',added,failed,remoteCount:(data||[]).length,localCount:existing.length+added};
 }catch(e){return {status:'error',message:String(e&&e.message||e)}}finally{if(db)db.close();busy=false}
}
export function startFramePhotoSync(){syncFramePhotos();setInterval(()=>{if(!document.hidden&&navigator.onLine)syncFramePhotos()},10*60*1000)}
