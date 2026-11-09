
import { useState } from "react";
import "./SkincareAssistant.css";

function SkincareAssistant() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! I'm your SkinSense AI assistant. Ask me about skincare ingredients, skin types, or building a skincare routine.",
    },
  ]);

  const handleSend = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    setMessages((previous) => [
      ...previous,
      { role: "user", text: userMessage },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userMessage,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Unable to get a response from the assistant.");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: data.response,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: "Sorry, I couldn't connect to the assistant. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="assistant-page">
      <header className="assistant-header">
        <a href="/" className="assistant-brand">✿ SkinSense AI</a>
        <a href="/" className="assistant-back">← Back to Home</a>
      </header>

      <main className="assistant-container">
        <section className="assistant-intro">
          <span className="eyebrow">YOUR PERSONAL SKINCARE GUIDE</span>
          <h1>Let's talk about skincare.</h1>
          <p>
            Ask questions about skincare ingredients, routines,
            and research-backed skincare information.
          </p>
        </section>

        <section className="chat-card">
          <div className="chat-heading">
            <div className="assistant-avatar">✿</div>
            <div>
              <h2>SkinSense Assistant</h2>
              <span>Skincare information assistant</span>
            </div>
          </div>

          <div className="chat-messages">
            {messages.map((item, index) => (
              <div
                key={index}
                className={`chat-message ${item.role}`}
              >
                {item.text}
              </div>
            ))}

            {loading && (
              <div className="chat-message assistant">
                Thinking...
              </div>
            )}
          </div>

          <div className="chat-input-area">
            <input
              type="text"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") handleSend();
              }}
              placeholder="Ask something about skincare..."
              disabled={loading}
            />

            <button
              type="button"
              onClick={handleSend}
              disabled={loading}
            >
              {loading ? "Sending..." : "Send ↑"}
            </button>
          </div>

          <p className="assistant-disclaimer">
            This assistant provides skincare information and is not a substitute for medical advice.
          </p>
        </section>
      </main>
    </div>
  );
}

export default SkincareAssistant;
