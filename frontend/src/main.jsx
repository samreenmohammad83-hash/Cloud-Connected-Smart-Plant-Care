import React, {useEffect, useState} from "react";
import {createRoot} from "react-dom/client";
import {LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer} from "recharts";
import "./style.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const DEVICE = "PLANT-001";

function App(){
  const [latest,setLatest]=useState(null), [history,setHistory]=useState([]), [alerts,setAlerts]=useState([]);
  const [device,setDevice]=useState(null), [threshold,setThreshold]=useState(30), [auto,setAuto]=useState(true);
  const load=async()=>{
    try{
      const [d,r,h,a]=await Promise.all([
        fetch(`${API}/api/devices/${DEVICE}`).then(x=>x.json()),
        fetch(`${API}/api/devices/${DEVICE}/latest`).then(x=>x.json()),
        fetch(`${API}/api/devices/${DEVICE}/history?limit=50`).then(x=>x.json()),
        fetch(`${API}/api/alerts?device_id=${DEVICE}`).then(x=>x.json())
      ]);
      setDevice(d); setLatest(r); setHistory([...h].reverse()); setAlerts(a);
      setThreshold(d.moisture_threshold); setAuto(d.auto_water);
    }catch(e){ console.error(e); }
  };
  useEffect(()=>{load(); const id=setInterval(load,3000); return()=>clearInterval(id)},[]);
  const status = latest && latest.soil_moisture < threshold ? "Needs Water" : "Healthy";
  const water=async()=>{await fetch(`${API}/api/devices/${DEVICE}/water`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({duration:5})}); load()};
  const saveThreshold=async()=>{await fetch(`${API}/api/devices/${DEVICE}/threshold`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({moisture_threshold:Number(threshold)})});load()};
  const toggle=async()=>{await fetch(`${API}/api/devices/${DEVICE}/auto-water`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({auto_water:!auto})});load()};
  return <main>
    <header><div><h1>🌱 Smart Plant Care</h1><p>Cloud-connected virtual IoT monitoring</p></div><span className="badge">{device?.device_id||DEVICE}</span></header>
    <section className="grid">
      <Card title="Soil Moisture" value={latest?`${latest.soil_moisture}%`:"—"}/>
      <Card title="Temperature" value={latest?`${latest.temperature}°C`:"—"}/>
      <Card title="Humidity" value={latest?`${latest.humidity}%`:"—"}/>
      <Card title="Light" value={latest?`${latest.light_level}%`:"—"}/>
      <Card title="Plant Status" value={status}/>
      <Card title="Pump" value="Virtual"/>
    </section>
    <section className="panel"><h2>Soil Moisture History</h2><ResponsiveContainer width="100%" height={280}>
      <LineChart data={history}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="timestamp" tickFormatter={x=>new Date(x).toLocaleTimeString()}/><YAxis domain={[0,100]}/><Tooltip/><Line type="monotone" dataKey="soil_moisture"/></LineChart>
    </ResponsiveContainer></section>
    <section className="controls">
      <div><h2>Controls</h2><label>Moisture threshold <input value={threshold} onChange={e=>setThreshold(e.target.value)} type="number" min="0" max="100"/> %</label><button onClick={saveThreshold}>Save Threshold</button></div>
      <div><button onClick={toggle}>Auto Water: {auto?"ON":"OFF"}</button><button onClick={water}>Manual Water</button></div>
    </section>
    <section className="panel"><h2>Alerts</h2>{alerts.length?alerts.slice(0,8).map(a=><div className="alert" key={a.alert_id}><b>{a.level}</b> — {a.message} <small>{a.status}</small></div>):<p>No alerts yet.</p>}</section>
  </main>
}
function Card({title,value}){return <div className="card"><span>{title}</span><strong>{value}</strong></div>}
createRoot(document.getElementById("root")).render(<App/>);
