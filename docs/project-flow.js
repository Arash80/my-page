
(() => {
 'use strict';
 const flows={"aegisops":[["Prepare data","Clean and validate credit-risk records before model development.","Validated features"],["Train & select","Compare models and select a cost-aware threshold on validation data.","Governed model candidate"],["Serve & observe","Promote the tested artifact, serve predictions, and collect monitoring evidence.","Monitoring signal"],["Investigate safely","Route an incident through evidence-gathering tools before forming a read-only diagnosis.","Recommendation, not a production change"]],"techrag":[["Read PDFs","Extract document text while retaining source and page information.","Page-aware passages"],["Embed & retrieve","Build embeddings and retrieve the passages most relevant to a question.","Ranked source context"],["Answer locally","Provide retrieved context to an Ollama-hosted model.","Context-grounded response"],["Show sources","Display source pages, relevant chunks, and retrieval metadata.","An inspectable answer"]],"workplaceops":[["Authenticate","Validate the request token and reload the current user account.","Current identity"],["Check permissions","Enforce role-specific access and booking ownership.","Authorized operation"],["Validate booking","Check the room, capacity, and requested time interval.","Eligible request"],["Protect the database","Use PostgreSQL transactions and overlap protection to accept or reject concurrent writes.","Booking or conflict response"]],"fraud":[["Order data by time","Separate historical transactions into earlier and later periods.","Temporal dataset"],["Train features & models","Fit transformations and boosted models without using future observations.","Trained candidates"],["Evaluate decisions","Check performance, calibration, and uncertainty with held-out observations.","Model decision policy"],["Serve & monitor","Orchestrate repeatable workflows and monitor incoming data behavior.","Operational evidence"]],"alignmentops":[["Curate examples","Select and format OASST1 training conversations.","Training dataset"],["Prepare completion targets","Build completion-only supervised fine-tuning samples.","Supervised examples"],["Adapt with LoRA","Fine-tune a small Gemma model with parameter-efficient adapters.","Adapted model"],["Evaluate differences","Compare base and adapter outputs under controlled prompts.","Generation diagnostics"]],"metrictrace":[["Validate inputs","Use typed schemas to constrain incoming metric requests.","Checked data"],["Calculate reliably","Compute authoritative statistics in deterministic code.","Reproducible metrics"],["Store the evidence","Return structured values and context through shared contracts.","Auditable records"],["Explain optionally","Let the language layer describe the verified results, not invent new calculations.","Grounded explanation"]],"agenticrag":[["Ask a question","Receive a document question and prepare retrieval.","Search request"],["Retrieve and rerank","Compare dense, sparse, hybrid, or multi-query search and order passages.","Prioritized evidence"],["Check sufficiency","Route weak-evidence queries through corrective retrieval.","Sufficient context or a corrective step"],["Answer with citations","Produce a response with supporting passages and traces.","Auditable answer"]],"deskpilot":[["Gather local knowledge","Read CSV, SQLite, and PDF support sources.","Indexed records"],["Retrieve evidence","Find the information relevant to the user question.","Relevant help content"],["Generate locally","Use a local Ollama model with the retrieved context.","Draft response"],["Answer or escalate","Provide a grounded reply or an escalation path.","Support outcome"]],"nasa":[["Fetch APOD","Retrieve NASA Astronomy Picture of the Day records.","API response"],["Check fields","Validate and normalize incoming data.","Clean record"],["Run the DAG","Use Airflow to coordinate extraction and loading.","Scheduled pipeline"],["Upsert safely","Insert or update PostgreSQL rows without duplicating reruns.","Consistent table"]],"chestxray":[["Split by patient","Keep samples from the same patient out of different evaluation partitions.","Patient-disjoint data"],["Train image model","Fit DenseNet121 with imbalance-aware handling.","Trained classifier"],["Evaluate & track","Report AUROC and capture configuration in experiment records.","Tracked results"],["Explain visually","Use GradCAM to identify image regions influencing model outputs.","Visual explanation"]],"fraudscope":[["Receive CSV & question","Start with local data and an explicit analysis task.","Analysis request"],["Agents prepare work","Use separate code-writing and review roles to propose operations.","Candidate actions"],["Validate & execute","Check approved Python operations; use deterministic routines for actual metrics.","Trusted calculations"],["Verify & report","Apply bounded repair and produce structured JSON, CSV, and Markdown evidence.","Auditable report"]],"cybergraph":[["Ingest research","Prepare cybersecurity papers with source identifiers.","Document evidence"],["Create graph context","Build graph relationships and semantic representations.","Graph and vector context"],["Retrieve evidence","Combine relevant connected entities with supporting passages.","Focused sources"],["Generate with citations","Provide a locally generated response linked to source pages.","Research answer"]],"reflexion":[["Draft","Produce an initial answer to the task.","First response"],["Critique","Check gaps or weaknesses using structured state.","Revision targets"],["Research if needed","Gather additional supporting information using tools.","New evidence"],["Revise within limits","Use bounded iterations, validation, and stopping rules.","Tracked revision"]],"prm":[["Define the scene","Specify start, goal, obstacles, and workspace bounds.","Planning problem"],["Sample a roadmap","Generate reproducible candidate waypoints.","Graph nodes"],["Check each connection","Reject edges that intersect obstacles.","Safe roadmap"],["Find the route","Search the weighted graph for a feasible shortest path.","Path or explicit failure"]],"twolink":[["Set a target","Specify a desired Cartesian end-effector location.","Reference point"],["Solve kinematics","Translate the target into joint-angle references.","Joint references"],["Simulate dynamics","Apply the manipulator and motor model in Simulink.","Simulated motion"],["Animate the arm","Visualize the resulting joint and end-effector movement.","Motion demonstration"]],"desalination":[["Observe the process","Read demand, renewable power availability, storage, and plant state.","Operating observation"],["Choose an RL action","Use a learned policy to choose an operating decision.","Control command"],["Simulate operation","Apply process and storage constraints as the plant evolves.","Updated state"],["Feed information back","Use state and performance to inform the next step.","Closed-loop control"]],"hardware":[["Measure power traces","Collect hardware measurements for normal and Trojan examples.","Signal samples"],["Prepare representations","Create time-series and image-like features.","Model inputs"],["Detect and identify","Use staged deep-learning models to classify unusual behavior.","Detection estimate"],["Assess uncertainty","Inspect Monte Carlo dropout outputs alongside the prediction.","Uncertainty evidence"]],"lpv":[["Collect process data","Observe changing conditions, inputs, and dynamic responses.","Identification dataset"],["Define varying model","Represent dependence on scheduling variables.","LPV model form"],["Estimate parameters","Use Bayesian inference to learn model relationships and uncertainty.","Posterior estimates"],["Examine dynamics","Interpret the changing model across operating conditions.","Control-oriented model"]],"edge":[["Run the first model part","Compute a partition of the network on a Raspberry Pi.","Intermediate features"],["Transfer activations","Send intermediate representations to another edge device.","Feature stream"],["Check perturbations","Use a Mahalanobis-distance detector on the feature space.","Anomaly signal"],["Continue and evaluate","Complete distributed inference and record detection and latency evidence.","Measured edge-system behavior"]]};
 const demo={
 aegisops:['Credit data','Model service','Monitor','Incident triage'],
 techrag:['Technical PDFs','Retrieval','Local model','Cited answer'],
 workplaceops:['User + token','Business rules','PostgreSQL','Booking / 409'],
 fraud:['Past records','Train','Validate','Future data'],
 alignmentops:['Conversations','LoRA SFT','Adapter','Comparison'],
 metrictrace:['Typed data','Calculator','Evidence','Explanation'],
 agenticrag:['Question','Retrieve','Sufficiency','Citations'],
 deskpilot:['IT knowledge','Local index','Ollama','Answer'],
 nasa:['NASA API','Airflow','Validation','PostgreSQL'],
 chestxray:['Patient split','DenseNet','AUROC','GradCAM'],
 fraudscope:['Dataset','Agents','Guarded checks','Report'],
 cybergraph:['Papers','Graph + vectors','Retrieval','Citations'],
 reflexion:['Draft','Critique','Research','Revise'],
 prm:['Start / goal','Sample nodes','Safe edges','Path'],
 twolink:['Target','Kinematics','Dynamics','Animation'],
 desalination:['Plant state','RL policy','Process','Feedback'],
 hardware:['Signals','Features','Detector','Uncertainty'],
 lpv:['Measurements','LPV model','Bayesian fit','Dynamics'],
 edge:['Pi 1','Feature stream','Detector','Pi 3']
 };
 const dialog=document.getElementById('project-dialog');
 if(!dialog)return;
 dialog.classList.add('vf-dialog');
 const body=dialog.querySelector('.dialog-body');
 const oldDetails=dialog.querySelector('.dialog-section');
 const technical=document.createElement('details');technical.className='vf-deep-dive';
 const summary=document.createElement('summary');summary.textContent='Read engineering context';
 technical.append(summary);
 oldDetails.parentNode.insertBefore(technical,oldDetails);technical.append(oldDetails);
 const main=document.createElement('section');main.className='vf-explainer';main.setAttribute('aria-label','Interactive project workflow');
 const top=document.createElement('div');top.className='vf-meta';
 top.innerHTML='<strong>HOW THE SYSTEM WORKS</strong><span>Select a stage to see what happens</span>';
 const map=document.createElement('div');map.className='vf-map';map.setAttribute('role','group');map.setAttribute('aria-label','Stages in project workflow');
 const focus=document.createElement('div');focus.className='vf-focus';
 focus.innerHTML='<div><span class="vf-count" id="vf-count">STEP 01 / 04</span><h3 id="vf-stage-title"></h3><p id="vf-stage-desc"></p></div><div class="vf-result"><span>WHAT THIS STAGE PRODUCES</span><strong id="vf-stage-out"></strong></div>';
 const example=document.createElement('div');example.className='vf-example';example.setAttribute('aria-label','Simplified system architecture');
 const caption=document.createElement('p');caption.className='vf-caption';caption.textContent='Conceptual architecture — an explanation of the project, not a live system or measured results.';
 main.append(top,map,focus,example,caption);
 body.insertBefore(main,technical);
 const source=dialog.querySelector('#dialog-link');
 source.textContent='Original notes / source (optional) ↗';
 let activeId=null,activeStage=0;
 function selectStage(index){
  const steps=flows[activeId]||[];
  if(!steps[index])return;
  activeStage=index;
  dialog.querySelector('#vf-count').textContent='STAGE '+String(index+1).padStart(2,'0')+' / '+String(steps.length).padStart(2,'0');
  dialog.querySelector('#vf-stage-title').textContent=steps[index][0];
  dialog.querySelector('#vf-stage-desc').textContent=steps[index][1];
  dialog.querySelector('#vf-stage-out').textContent=steps[index][2];
  Array.from(map.children).forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
 }
 function render(id){
  if(!flows[id])return;
  activeId=id;activeStage=0;
  const arr=flows[id];map.replaceChildren();
  arr.forEach((stage,i)=>{
   const b=document.createElement('button');b.type='button';b.className='vf-node';
   const num=document.createElement('span');num.className='vf-number';num.textContent=String(i+1).padStart(2,'0');
   const name=document.createElement('b');name.textContent=stage[0];b.append(num,name);
   b.addEventListener('click',()=>selectStage(i));map.append(b);
  });
  selectStage(0);
  example.replaceChildren();
  (demo[id]||arr.map(x=>x[0])).forEach((label,i,a)=>{
   const pill=document.createElement('span');pill.textContent=label;example.append(pill);
   if(i<a.length-1){const arrow=document.createElement('b');arrow.textContent='→';arrow.setAttribute('aria-hidden','true');example.append(arrow);}
  });
  technical.open=false;
  const heading=dialog.querySelector('#dialog-type');
  if(heading)heading.textContent='VISUAL ENGINEERING WALKTHROUGH';
  const link=source.href;
  source.textContent=link==='https://github.com/Arash80/'?'GitHub profile (optional) ↗':'Original notes / source (optional) ↗';
 }
 document.addEventListener('click',event=>{
  const button=event.target.closest('[data-open]');
  if(!button)return;
  const id=button.dataset.open;
  if(!flows[id])return;
  queueMicrotask(()=>render(id));
 },true);
})();
