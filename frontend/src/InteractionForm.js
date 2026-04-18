// ONLY CHANGE IS IN SEARCH RESULTS SECTION (bottom)

import React, { useState, useEffect } from "react";
import "./styles.css";
import { useDispatch, useSelector } from "react-redux";
import { fetchInteractions, addInteraction } from "./redux/interactionSlice";
import axios from "axios";

export default function InteractionForm() {

  const dispatch = useDispatch();
  const interactions = useSelector((state) => state.interaction.list);

  const [form, setForm] = useState({
    hcp_name: "",
    date: "2025-04-19",
    time: "19:36",
    interaction_type: "Meeting",
    attendees: "",
    topics: "",
    sentiment: "neutral",
    outcomes: "",
    follow_ups: ""
  });

  const [chatInput, setChatInput] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSentiment = (value) => {
    setForm({ ...form, sentiment: value });
  };

  const handleSubmit = async () => {
    try {
      await dispatch(addInteraction({
        hcp_name: form.hcp_name,
        interaction_date: form.date,
        topics: form.topics,
        sentiment: form.sentiment,
        outcomes: form.outcomes
      }));

      dispatch(fetchInteractions());
      alert("Saved Successfully");

    } catch (err) {
      console.error(err);
    }
  };

  const handleChat = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/chat/chat", {
        query: chatInput
      });

      console.log("AI RESPONSE:", res.data);

      if (res.data.action === "error") {
        alert(res.data.message || "AI could not process input");
        return;
      }

      if (res.data.action === "search") {
        setSearchResults(res.data.data || []);
        return;
      }

      const data = res.data.extracted_data || {};

      setForm({
        ...form,
        hcp_name: data.hcp_name || "",
        date: data.date || form.date,
        time: data.time || form.time,
        attendees: data.attendees || "",
        topics: data.topics || "",
        sentiment: (data.sentiment || "neutral").toLowerCase(),
        outcomes: data.outcomes || ""
      });

    } catch (err) {
      console.error("AI ERROR:", err.response?.data || err.message);
      alert("Backend not responding or AI error");
    }
  };

  return (
    <div className="main-wrapper">
      <div className="container">
        <header>
          <h2>Log HCP Interaction</h2>
        </header>

        <div className="dashboard-layout">

          <div className="form-pane">

            <section className="section">
              <h3>Interaction Details</h3>

              <div className="form-row">
                <div className="field">
                  <label>HCP Name</label>
                  <input name="hcp_name" value={form.hcp_name} onChange={handleChange} />
                </div>

                <div className="field">
                  <label>Interaction Type</label>
                  <select name="interaction_type" value={form.interaction_type} onChange={handleChange}>
                    <option>Meeting</option>
                  </select>
                </div>
              </div>

              <div className="form-row">
                <div className="field">
                  <label>Date</label>
                  <input type="date" name="date" value={form.date} onChange={handleChange} />
                </div>

                <div className="field">
                  <label>Time</label>
                  <input type="time" name="time" value={form.time} onChange={handleChange} />
                </div>
              </div>

              <div className="field full-width">
                <label>Attendees</label>
                <input name="attendees" value={form.attendees} onChange={handleChange} />
              </div>

              <div className="field full-width">
                <label>Topics Discussed</label>
                <textarea name="topics" value={form.topics} onChange={handleChange}></textarea>
                <button className="voice-btn">🎤 Summarize from Voice Note</button>
              </div>
            </section>

            <section className="section">
              <h3>Materials Shared / Samples Distributed</h3>
              <div className="table-like-row">
                <span>Materials Shared</span>
                <button className="outline-btn">Search/Add</button>
              </div>
              <div className="table-like-row">
                <span>Samples Distributed</span>
                <button className="outline-btn">Add Sample</button>
              </div>
            </section>

            <section className="section">
              <h3>Observed/Inferred HCP Sentiment</h3>

              <div className="sentiment-row">
                <label>
                  <input type="radio" checked={form.sentiment === "positive"} onChange={() => handleSentiment("positive")} />
                  Positive
                </label>

                <label>
                  <input type="radio" checked={form.sentiment === "neutral"} onChange={() => handleSentiment("neutral")} />
                  Neutral
                </label>

                <label>
                  <input type="radio" checked={form.sentiment === "negative"} onChange={() => handleSentiment("negative")} />
                  Negative
                </label>
              </div>
            </section>

            <button className="log-btn" onClick={handleSubmit}>
              Submit
            </button>

            <div style={{ marginTop: "20px" }}>
              <h3>Saved Interactions</h3>
              {interactions.map((i) => (
                <div key={i.id}>
                  {i.hcp_name} - {i.topics} ({i.sentiment})
                </div>
              ))}
            </div>

            {/* ✅ UPDATED: REMOVE DUPLICATES */}
            {searchResults.length > 0 && (
              <div style={{ marginTop: "20px" }}>
                <h3>Search Results</h3>
                {[...new Map(searchResults.map(item => [item.id || item.hcp_name + item.topics, item])).values()]
                  .map((item, index) => (
                    <div key={index}>
                      <strong>{item.hcp_name}</strong> - {item.topics} ({item.sentiment})
                    </div>
                  ))}
              </div>
            )}

          </div>

          <div className="ai-pane">

            <div className="ai-header">
              <span className="ai-icon">👁️</span>
              <div>
                <strong>AI Assistant</strong>
                <p>Log interaction via chat</p>
              </div>
            </div>

            <div className="ai-chat-box">
              <div className="ai-msg">
                Log interaction details here (e.g., "Met Dr. Smith, discussed Product X...")
              </div>
            </div>

            <div className="ai-input-group">
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Describe interaction..."
              />
              <button className="log-btn" onClick={handleChat}>
                Log
              </button>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}