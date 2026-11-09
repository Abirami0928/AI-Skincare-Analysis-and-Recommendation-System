
import { useState } from "react";
import "./SkinAnalysis.css";


function SkinAnalysis() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleImage = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please select an image file.");
      return;
    }

    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

const removeImage = () => {
  if (preview) URL.revokeObjectURL(preview);

  setImage(null);
  setPreview(null);
  setResult(null);
  setLoading(false);
};

  return (
    <div className="analysis-page">
      <nav className="analysis-nav">
        <a href="/" className="analysis-brand">✿ SkinSense AI</a>
        <a href="/">Back to Home</a>
      </nav>

      <section className="analysis-header">
        <span className="eyebrow">AI-POWERED SKINCARE</span>
        <h1>Let's understand your skin.</h1>
        <p>
          Upload a clear facial image to begin your
          personalized skin analysis journey.
        </p>
      </section>

      <section className="upload-container">
        <div className="upload-card">
          <h2>Upload your skin image</h2>
          <p>Choose a clear, front-facing facial photograph.</p>

          <label className="upload-area">
            {preview ? (
              <img
                src={preview}
                alt="Uploaded skin preview"
                className="image-preview"
              />
            ) : (
              <div className="upload-placeholder">
                <span className="upload-icon">↑</span>
                <h3>Drag and drop your image</h3>
                <p>or click to browse your files</p>
                <span className="file-info">
                  JPG, JPEG or PNG
                </span>
              </div>
            )}

            <input
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              onChange={handleImage}
              hidden
            />
          </label>

          {image && (
            <div className="selected-image">
              <span>{image.name}</span>
              <button onClick={removeImage}>Remove image</button>
            </div>
          )}

         <button
  className="analyze-button"
  disabled={!image || loading}
  onClick={async () => {
    const formData = new FormData();
    formData.append("file", image);

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed");
      }

      setResult(data);

    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  }}
>
  {loading ? "Analyzing..." : "Analyze My Skin →"}
</button>
                    {result && (
            <div className="result-card">
              <h2>Skin Analysis Result</h2>

              <h3>
                {result.predicted_class.toUpperCase()}
              </h3>

              <p>
                Model Confidence: {result.confidence}%
              </p>

              <p>
                This is an AI-generated estimate, not a medical diagnosis.
              </p>
            </div>
          )}

          <p className="privacy-note">
  Your image is sent to our backend for analysis and is not saved to disk by this demo.
</p>
        </div>

        <aside className="guidelines-card">
          <h3>For better results</h3>
          <ul>
            <li>Use natural lighting.</li>
            <li>Face the camera directly.</li>
            <li>Avoid heavy makeup and filters.</li>
            <li>Keep your face clearly visible.</li>
          </ul>
          <div className="guidelines-note">
            <span>✧</span>
            AI predictions are estimates, not medical diagnoses.
          </div>
        </aside>
      </section>
    </div>
  );
}

export default SkinAnalysis;
