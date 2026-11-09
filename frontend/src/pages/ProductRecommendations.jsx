
import { useState } from "react";
import "./ProductRecommendations.css";

function ProductRecommendations() {
  const [category, setCategory] = useState("Moisturiser");
  const [skinType, setSkinType] = useState("dry");
  const [budget, setBudget] = useState(1000);

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchRecommendations = async () => {
    setLoading(true);
    setError("");
    setProducts([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/recommendations",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            skin_label: skinType,
            budget: Number(budget),
            product_type: category || null,
            ingredient_keywords:
              skinType === "dry"
                ? ["glycerin", "sodium hyaluronate"]
                : skinType === "oil"
                ? ["niacinamide", "salicylic acid"]
                : ["salicylic acid", "benzoyl peroxide"],
            top_n: 10,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Unable to fetch product recommendations.");
      }

      const data = await response.json();
      setProducts(data.recommendations || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="products-page">
      <header className="products-header">
        <a href="/" className="products-brand">✿ SkinSense AI</a>
        <a href="/" className="back-home">← Back to Home</a>
      </header>

      <section className="products-intro">
        <span className="eyebrow">YOUR SKINCARE COLLECTION</span>
        <h1>Find products for your skin.</h1>
        <p>
          Explore skincare products, discover their ingredients,
          and make informed choices for your routine.
        </p>
      </section>

      <section className="products-content">
        <div className="products-toolbar">
          <h2>Explore Products</h2>

          <select
            value={skinType}
            onChange={(event) => setSkinType(event.target.value)}
          >
            <option value="dry">Dry / Hydration</option>
            <option value="oil">Oily</option>
            <option value="acne">Acne</option>
          </select>

          <select
            value={category}
            onChange={(event) => setCategory(event.target.value)}
          >
            <option value="Moisturiser">Moisturiser</option>
            <option value="Cleanser">Cleanser</option>
            <option value="Serum">Serum</option>
            <option value="Sunscreen">Sunscreen</option>
          </select>

          <input
            type="number"
            min="1"
            value={budget}
            onChange={(event) => setBudget(event.target.value)}
            placeholder="Budget in ₹"
          />

          <button
            type="button"
            onClick={fetchRecommendations}
            disabled={loading}
          >
            {loading ? "Finding Products..." : "Get Recommendations"}
          </button>
        </div>

        {error && <p className="error-message">{error}</p>}

        {loading && <p>Finding suitable products for you...</p>}

        {!loading && products.length === 0 && !error && (
          <p>Choose your preferences and click Get Recommendations.</p>
        )}

        <div className="products-grid">
          {products.map((product) => (
            <article className="product-card" key={product.rank}>
  <div className="product-image">
    <img
      src="https://placehold.co/400x300/f1f5f0/526b55?text=Skincare+Product"
      alt={product.product_name}
    />
  </div>

  <div className="product-details">
                <span className="product-category">
                  {product.product_type}
                </span>

                <h3>{product.product_name}</h3>

                <p className="product-description">
                  Ingredient matches: {product.ingredient_matches}
                </p>

                <div className="ingredient-info">
                  <strong>Ingredients</strong>
                  <p>{product.ingredients_clean}</p>
                </div>

                <div className="product-bottom">
                  <strong>
                    ₹{Number(product.Price_INR).toFixed(2)}
                  </strong>

                  <a
                    href={product.product_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View Product
                  </a>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

export default ProductRecommendations;
