
import "./App.css";
import { Routes, Route } from "react-router-dom";
import SkinAnalysis from "./pages/SkinAnalysis";
import ProductRecommendations from "./pages/ProductRecommendations";
import SkincareAssistant from "./pages/SkincareAssistant";

function Home() {
  return (
    <div className="app">
      <nav className="navbar">
        <a className="brand" href="#">
          <span className="brand-icon">✿</span>
          SkinSense AI
        </a>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#about">About</a>
        </div>

        <a className="nav-button" href="#features">
          Get Started ↗
        </a>
      </nav>

      <main>
        <section className="hero" id="about">
          <div className="hero-content">
            <span className="eyebrow">
              ✦ AI-POWERED SKINCARE
            </span>

            <h1>
              Understand your skin.
              <br />
              <span>Care with confidence.</span>
            </h1>

            <p>
              Discover your skin type, explore personalized
              skincare recommendations, and learn about
              ingredients with the help of AI.
            </p>

            <div className="hero-actions">
              <a className="primary-button" href="#features">
                Explore SkinCare <span>→</span>
              </a>
              <a className="secondary-button" href="#features">
                Discover features
              </a>
            </div>

            <div className="trust-note">
              <span>✳</span>
              Personalized insights. Smarter skincare.
            </div>
          </div>

          <div className="hero-visual">
            <div className="decor decor-one" />
            <div className="decor decor-two" />

            <div className="skin-card">
              {/* <div className="skin-illustration">
                <div className="face">
                  <div className="hair" />
                  <div className="eye eye-left" />
                  <div className="eye eye-right" />
                  <div className="nose" />
                  <div className="mouth" />
                  <div className="cheek cheek-left" />
                  <div className="cheek cheek-right" />
                </div>
              </div> */}
              <div className="hero-visual">
                <img
                  src="https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?auto=format&fit=crop&w=1000&q=85"
                  alt="Natural skincare and glowing skin"
                  className="hero-photo"
                />
              </div>

              <div className="skin-card-footer">
                <div>
                  <span className="small-label">YOUR SKIN JOURNEY</span>
                  <h3>Start with self-care</h3>
                </div>
                <span className="sparkle">✧</span>
              </div>
            </div>

            <div className="floating-note note-top">
              <span>✿</span> Your skin, your journey
            </div>

            <div className="floating-note note-bottom">
              <span className="status-dot" />
              AI-assisted insights
            </div>
          </div>
        </section>

        <section className="features" id="features">
          <div className="section-heading">
            <span className="eyebrow">MADE FOR YOUR SKIN</span>
            <h2>Your skincare journey starts here</h2>
            <p>
              Explore tools designed to help you make more
              informed skincare choices.
            </p>
          </div>

          <div className="feature-grid">
            <article className="feature-card">
              <div className="feature-icon">◎</div>
              <h3>Skin Analysis</h3>
              <p>
                Explore AI-assisted skin type and skin concern
                classification using your image.
              </p>
              <a href="/skin-analysis">Explore analysis →</a>
            </article>

            <article className="feature-card">
              <div className="feature-icon">✿</div>
              <h3>Product Recommendations</h3>
              <p>
                Discover skincare products based on ingredients,
                preferences, and your budget.
              </p>
                <a href="/products">Explore products →</a> 
           </article>

            <article className="feature-card">
              <div className="feature-icon">✧</div>
              <h3>AI Skincare Assistant</h3>
              <p>
                Explore skincare ingredients and research-backed
                information through an AI assistant.
              </p>
                <a href="/assistant">Meet your assistant →</a>
            </article>
          </div>
        </section>

        <section className="coming-section" id="analysis">
          <span className="eyebrow">COMING TO YOUR SKINCARE SPACE</span>
          <h2>A more thoughtful way to care for your skin.</h2>
          <p>
            Our analysis, recommendation, and research tools
            will come together in one convenient platform.
          </p>
        </section>
      </main>

      <footer className="footer">
        <a className="brand" href="#">
          <span className="brand-icon">✿</span>
          SkinSense AI
        </a>
        <p>AI-assisted skincare exploration.</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/skin-analysis" element={<SkinAnalysis />} />
      <Route path="/products" element={<ProductRecommendations />} />
      <Route path="/assistant" element={<SkincareAssistant />} />
    </Routes>
  );
}

export default App;