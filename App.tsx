import { useEffect, useState } from "react";
import { Activity, Bell, Bot, Brain, CalendarDays, Mail, Mic, Monitor, Send, Settings, ShieldCheck, Sparkles } from "lucide-react";

const API = "http://127.0.0.1:8765";
type Message = { role: "user" | "assistant"; content: string };

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hello! Main Kitsune hoon 🦊. Main ready hoon. Aaj kya karna hai?" }
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [backend, setBackend] = useState("Checking...");
  const [privacy, setPrivacy] = useState(true);

  useEffect(() => {
    window.kitsune.health().then(x => setBackend(x.ok ? "Connected" : "Offline")).catch(() => setBackend("Offline"));
  }, []);

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setInput("");
    setBusy(true);
    try {
      const response = await fetch(`${API}/chat`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: "assistant", content: data.reply ?? "No response received." }]);
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "Backend connect nahi ho raha. Pehle FastAPI server start karo." }]);
    } finally { setBusy(false); }
  }

  return <main className="shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-icon">狐</span><div><b>KITSUNE AI</b><small>DESKTOP COMPANION</small></div></div>
      <div className="nav-label">WORKSPACE</div>
      <nav>
        <a className="active"><Sparkles size={17}/> Overview</a>
        <a><Bot size={17}/> AI Chat</a>
        <a><Mail size={17}/> Emails <span className="soon">SETUP</span></a>
        <a><Bell size={17}/> Notifications</a>
        <a><Brain size={17}/> Memory</a>
        <a><CalendarDays size={17}/> Productivity</a>
        <a><Monitor size={17}/> PC Automation</a>
      </nav>
      <div className="sidebar-bottom">
        <div className="secure"><ShieldCheck size={16}/><span>Local-first privacy</span></div>
        <a><Settings size={17}/> Settings</a>
      </div>
    </aside>

    <section className="main">
      <header className="topbar">
        <div><span className="eyebrow">YOUR PERSONAL AI COMPANION</span><h1>Good day, Ayush <span>✦</span></h1></div>
        <div className="top-status"><i className={backend === "Connected" ? "dot on" : "dot"}/>{backend}</div>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <div className="pill"><span/> KITSUNE IS READY</div>
          <h2>Your day,<br/><em>with a little magic.</em></h2>
          <p>Your personal AI companion for conversations, productivity and desktop assistance.</p>
          <div className="hero-actions"><button className="primary" onClick={() => document.getElementById("chat-input")?.focus()}><Mic size={16}/> Start a conversation</button><button className="secondary" onClick={() => setPrivacy(!privacy)}>{privacy ? "Privacy mode on" : "Privacy mode off"}</button></div>
        </div>
        <div className="avatar-wrap">
          <div className="orbit orbit-one"/><div className="orbit orbit-two"/>
          <div className="avatar-placeholder"><div className="ears"><i/><i/></div><div className="avatar-face"><span className="hair">✦</span><div className="eyes"><i/><i/></div><div className="mouth">ᴗ</div></div><div className="tail">〰</div></div>
          <div className="avatar-caption"><span className="live-dot"/> 3D AVATAR SLOT <small>Import a VRM model in a later milestone</small></div>
        </div>
      </section>

      <section className="stats">
        <div className="stat"><span><Activity size={17}/></span><small>AI ENGINE</small><b>{backend}</b></div>
        <div className="stat"><span><Brain size={17}/></span><small>LOCAL MEMORY</small><b>SQLite ready</b></div>
        <div className="stat"><span><ShieldCheck size={17}/></span><small>PRIVACY</small><b>{privacy ? "Protected" : "Review settings"}</b></div>
      </section>

      <section className="chat-panel">
        <div className="panel-heading"><div><span className="eyebrow">KITSUNE ASSISTANT</span><h3>Let's talk</h3></div><span className="chat-state"><i className="dot on"/>{busy ? "Thinking..." : "Text mode"}</span></div>
        <div className="messages">
          {messages.map((m, i) => <div className={`message ${m.role}`} key={i}><div className="message-avatar">{m.role === "assistant" ? "狐" : "A"}</div><div><small>{m.role === "assistant" ? "KITSUNE" : "YOU"}</small><p>{m.content}</p></div></div>)}
        </div>
        <form className="composer" onSubmit={e => { e.preventDefault(); void send(); }}>
          <input id="chat-input" value={input} onChange={e => setInput(e.target.value)} placeholder="Message Kitsune... (Hindi, English or Hinglish)" />
          <button className="send" disabled={busy || !input.trim()} aria-label="Send"><Send size={17}/></button>
        </form>
        <div className="hint">Text chat is active. Voice, Gmail and Windows notification integrations are staged for subsequent setup.</div>
      </section>
      <footer> KITSUNE AI <span>•</span> LOCAL DESKTOP COMPANION <span>•</span> EARLY ACCESS BUILD</footer>
    </section>
  </main>;
}
