const API_URL = 'http://127.0.0.1:8000/predict';

function $(id){return document.getElementById(id)}

function readValues(){
  return {
    diaperSize: $('diaperSize').value,
    topsheetMaterial: $('topsheetMaterial').value,
    sapType: $('sapType').value,
    pulpType: $('pulpType').value,
    additives: $('additives').value,
    supplier: $('supplier').value,
    sapRatio: Number($('sapRatio').value),
    coreGsm: Number($('coreGsm').value),
    hydroScore: Number($('hydroScore').value),
    // backend expects integer channels count; map dropdown to 1 or 0
    channels: $('channels').value === 'With Channels' ? 1 : 0,
    coreShaping: $('coreShaping').value,
  };
}

function setButtonRunning(running){
  const btn = $('predictButton');
  const spinner = $('buttonSpinner');
  const label = $('buttonLabel');
  if(!btn) return;
  btn.disabled = running;
  if(spinner) spinner.style.display = running ? 'inline-block' : 'none';
  if(label) label.textContent = running ? 'Running Prediction...' : 'Run ML Prediction';
}

function showMessage(msg, isError){
  const m = $('messageArea');
  if(!m) return;
  m.textContent = msg;
  if(!msg){
    m.classList.remove('message-error','message-success');
    return;
  }
  m.classList.toggle('message-error', !!isError);
  m.classList.toggle('message-success', !isError);
}

function setStatusState(statusText, state){
  const statusEl = $('sumStatus');
  if(!statusEl) return;
  statusEl.textContent = statusText;
  statusEl.classList.remove('status-success','status-error','status-pending');
  if(state) statusEl.classList.add(`status-${state}`);
}

function updateFleet(response){
  // Update only these two cards
  const m = $('materialCostValue');
  const a = $('absorptionValue');
  if(m) m.textContent = response.materialCost !== undefined ? formatCost(response.materialCost) : m.textContent;
  if(a) a.textContent = response.absorption !== undefined ? formatAbs(response.absorption) : a.textContent;
}

function formatCost(val){
  // ensure dollar format with 3 decimals if small
  if(typeof val === 'number') return `$${val.toFixed(3)}`;
  return val;
}

function formatAbs(val){
  if(typeof val === 'number') return `${Math.round(val)}g`;
  return val;
}

function formatConfidence(val){
  if (val === undefined || val === null) return '--';
  // Accept either 0-1 or 0-100 formats
  const n = Number(val);
  if (isNaN(n)) return '--';
  return (n > 1 ? n : n * 100).toFixed(1) + '%';
}

function showSummary(resp, durationSeconds){
  const s = $('predictionSummary');
  if(!s) return;
  $('sumMaterial').textContent = resp.materialCost !== undefined ? formatCost(resp.materialCost) : '--';
  $('sumAbsorption').textContent = resp.absorption !== undefined ? formatAbs(resp.absorption) : '--';
  $('sumConfidence').textContent = formatConfidence(resp.confidence);
  $('sumPrediction').textContent = resp.prediction ?? '--';
  $('sumTime').textContent = typeof durationSeconds === 'number' ? `${durationSeconds.toFixed(2)} sec` : '--';
  setStatusState('Prediction Completed', 'success');
  // ensure hidden -> visible with smooth fade-in (CSS handles transition)
  s.classList.add('visible');
}

async function runPrediction(){
  showMessage('');
  setStatusState('Running...','pending');
  const payload = readValues();
  setButtonRunning(true);

  const start = performance.now();
  try{
    const res = await fetch(API_URL,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });

    if(!res.ok) throw new Error(`Status ${res.status}`);
    const data = await res.json();
    const duration = (performance.now() - start) / 1000;
    updateFleet(data);
    showSummary(data, duration);
    showMessage('Prediction completed.');
  }catch(err){
    console.error(err);
    setStatusState('Prediction Failed','error');
    showMessage('Unable to reach the prediction API. Please try again.', true);
  }finally{
    setButtonRunning(false);
  }
}

// wire up controls
document.addEventListener('DOMContentLoaded',()=>{
  const btn = $('predictButton');
  if(btn) btn.addEventListener('click', runPrediction);

  // range displays
  const sap = $('sapRatio');
  const sapVal = $('sapRatioVal');
  if(sap && sapVal){ sapVal.textContent = sap.value + '%'; sap.addEventListener('input',()=> sapVal.textContent = sap.value + '%'); }

  const gsm = $('coreGsm');
  const gsmVal = $('coreGsmVal');
  if(gsm && gsmVal){ gsmVal.textContent = gsm.value; gsm.addEventListener('input',()=> gsmVal.textContent = gsm.value); }

  const hydro = $('hydroScore');
  const hydroVal = $('hydroScoreVal');
  if(hydro && hydroVal){ hydroVal.textContent = hydro.value; hydro.addEventListener('input',()=> hydroVal.textContent = hydro.value); }
});

