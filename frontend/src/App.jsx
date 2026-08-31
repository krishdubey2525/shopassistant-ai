import axios from "axios";
import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      type: "bot",
      text: "Hi! 👋 I'm ShopAssist AI. Tell me what you're looking for and I'll help you find the right product.",
      product: null,
    },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: userMessage,
        product: null,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/recommend",
        {
          message: userMessage,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: response.data.response,
          product: response.data.product,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: "Sorry, I couldn't connect to ShopAssist AI. Please make sure the backend is running.",
          product: null,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        type: "bot",
        text: "Hi! 👋 I'm ShopAssist AI. Tell me what you're looking for and I'll help you find the right product.",
        product: null,
      },
    ]);
  };

  const useSuggestion = (text) => {
    setMessage(text);
  };

  const getReasons = (product) => {
    const reasons = [];

    if (product.rating >= 4.5) {
      reasons.push(`Highly rated with ${product.rating}★`);
    }

    if (product.description) {
      if (
        product.description.toLowerCase().includes("programming") ||
        product.description.toLowerCase().includes("development")
      ) {
        reasons.push("Designed for programming and development");
      }

      if (
        product.description.toLowerCase().includes("16gb") ||
        product.description.toLowerCase().includes("16 gb")
      ) {
        reasons.push("16GB RAM for smooth multitasking");
      }

      if (
        product.description.toLowerCase().includes("1tb") ||
        product.description.toLowerCase().includes("1 tb")
      ) {
        reasons.push("1TB SSD provides ample storage");
      }

      if (
        product.description.toLowerCase().includes("512gb") ||
        product.description.toLowerCase().includes("512 gb")
      ) {
        reasons.push("512GB SSD provides fast storage");
      }
    }

    if (reasons.length === 0) {
      reasons.push("Matches your requested product category");
      reasons.push(`Rated ${product.rating}★ by customers`);
      reasons.push(`Available from ${product.brand}`);
    }

    return reasons.slice(0, 3);
  };

  return (
    <div className="app">

      <header className="header">
        <div className="brand">
          <div className="brand-icon">🛍️</div>

          <div>
            <h1>ShopAssist AI</h1>

            <div className="online-status">
              <span className="status-dot"></span>
              AI Shopping Assistant
            </div>
          </div>
        </div>

        <button className="clear-button" onClick={clearChat}>
          🗑️ Clear
        </button>
      </header>


      <main className="chat-container">

        {messages.length === 1 && (
          <div className="welcome-section">

            <div className="welcome-icon">
              🤖
            </div>

            <h2>What are you looking for?</h2>

            <p>
              Describe your requirements and ShopAssist AI
              will find the best matching product.
            </p>

            <div className="suggestions">

              <button
                onClick={() =>
                  useSuggestion(
                    "I need a laptop under ₹70000 for programming"
                  )
                }
              >
                💻 Laptop under ₹70,000
              </button>

              <button
                onClick={() =>
                  useSuggestion(
                    "I need a smartphone under ₹50000"
                  )
                }
              >
                📱 Smartphone under ₹50,000
              </button>

              <button
                onClick={() =>
                  useSuggestion(
                    "I need headphones under ₹5000"
                  )
                }
              >
                🎧 Headphones under ₹5,000
              </button>

            </div>
          </div>
        )}


        <div className="messages">

          {messages.map((msg, index) => (

            <div
              className={`message-row ${
                msg.type === "user"
                  ? "user-row"
                  : "bot-row"
              }`}
              key={index}
            >

              {msg.type === "bot" && (
                <div className="avatar bot-avatar">
                  🤖
                </div>
              )}

              <div className="message-content">

                <div
                  className={`message-bubble ${
                    msg.type === "user"
                      ? "user-message"
                      : "bot-message"
                  }`}
                >
                  {msg.text}
                </div>


                {msg.product && (
                  <div className="product-card">

                    <div className="recommendation-label">
                      <span>✨</span>
                      ShopAssist recommends
                    </div>


                    <div className="product-main">

                      <div className="product-icon">
                        {msg.product.category === "Laptop"
                          ? "💻"
                          : msg.product.category === "Smartphone"
                          ? "📱"
                          : msg.product.category === "Headphones"
                          ? "🎧"
                          : "🛍️"}
                      </div>


                      <div className="product-info">

                        <div className="product-category">
                          {msg.product.category}
                        </div>

                        <h3>
                          {msg.product.name}
                        </h3>

                        <div className="product-brand">
                          by {msg.product.brand}
                        </div>

                      </div>

                    </div>


                    <div className="product-stats">

                      <div className="stat price-stat">
                        <span className="stat-label">
                          Price
                        </span>

                        <strong>
                          ₹{msg.product.price.toLocaleString("en-IN")}
                        </strong>
                      </div>


                      <div className="stat rating-stat">
                        <span className="stat-label">
                          Rating
                        </span>

                        <strong>
                          ⭐ {msg.product.rating}
                        </strong>
                      </div>

                    </div>


                    <div className="product-description">
                      {msg.product.description}
                    </div>


                    {/* WHY THIS PRODUCT */}
                    <div className="why-section">

                      <div className="why-title">
                        <span>🧠</span>
                        Why ShopAssist chose this
                      </div>

                      <div className="reason-list">

                        {getReasons(msg.product).map(
                          (reason, reasonIndex) => (
                            <div
                              className="reason"
                              key={reasonIndex}
                            >
                              <span className="reason-check">
                                ✓
                              </span>

                              <span>
                                {reason}
                              </span>
                            </div>
                          )
                        )}

                      </div>

                    </div>


                    <div className="verified">
                      <span>✓</span>
                      Verified product from database
                    </div>

                  </div>
                )}

              </div>


              {msg.type === "user" && (
                <div className="avatar user-avatar">
                  👤
                </div>
              )}

            </div>

          ))}


          {loading && (
            <div className="message-row bot-row">

              <div className="avatar bot-avatar">
                🤖
              </div>

              <div className="message-bubble bot-message typing">

                <span></span>
                <span></span>
                <span></span>

                <label>
                  ShopAssist is thinking...
                </label>

              </div>

            </div>
          )}

        </div>

      </main>


      <footer className="input-area">

        <div className="input-wrapper">

          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask ShopAssist for a product recommendation..."
            rows="1"
          />

          <button
            className="send-button"
            onClick={sendMessage}
            disabled={!message.trim() || loading}
          >
            ➤
          </button>

        </div>

        <div className="input-hint">
          Press <strong>Enter</strong> to send
        </div>

      </footer>

    </div>
  );
}

export default App;