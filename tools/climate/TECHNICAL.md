# TERRA-X: Technical Architecture 📡

This document outlines the high-level architecture and data flow of the **TERRA-X Scenario Lab**.

## 🏗 System Overview
TERRA-X is a full-stack predictive simulation environment that combines **Three.js 3D Visualization**, **Real-time Meteorological Data**, and **Generative AI** to project global climate and socio-economic outcomes.

---

## 🛠 Technology Stack
- **Frontend**: React.js with Vite.
- **3D Engine**: Three.js (@react-three/fiber & @react-three/drei).
- **Styling**: Vanilla CSS with Framer Motion for micro-animations and Bootstrap for grid layout.
- **Backend Engine**: FastAPI (Python 3.10+).
- **Simulation AI**: Groq Cloud (Llama 3.3 70B) with OpenAI (GPT-3.5) fallback.
- **Geo-Data**: OpenStreetMap (Nominatim API) for geocoding and reverse-geocoding.
- **Climate Data**: OpenWeatherMap API for live terrestrial baselines.

---

## 🔄 Core Data Flow (The "Simulation Loop")

### 1. Target Acquisition
*   **User Action**: User searches for a city or clicks directly on the 3D globe.
*   **Vector Conversion**: If clicked, the 3D vector coordinates `(x, y, z)` are converted to spherical coordinates `(Lat, Lon)`.
*   **Geocoding**: The coordinates are sent to Nominatim to retrieve a human-readable sector name (e.g., "Mumbai, India").

### 2. Parameterization
*   **Interaction**: User adjusts variables (Carbon, Population, Economy, Resources).
*   **Validation**: The React state clamps these values between -100% and +100% to ensure simulation stability.

### 3. Backend Synthesis
*   **Weather Grounding**: The backend fetches the current "Real-feel" temperature and conditions for the target Lat/Lon.
*   **Contextual Prompting**: The engine constructs a "System-Level Analysis Prompt" that combines:
    *   The **Location** name.
    *   The **Real-time Weather** baseline.
    *   The **User-defined Variable Deltas**.

### 4. AI Prediction
*   The prompt is dispatched to **Groq's Llama-3.3-70B** engine.
*   **Fallback Logic**: If the primary engine is busy, the system instantly switches to **Llama-3-8B** to ensure zero-latency response.

### 5. Visualization
*   The result is streamed back to the frontend and rendered in the **Sector Analysis Panel** using high-contrast typography and monospace formatting for a clinical "Terminal" aesthetic.

---

## 🔒 Security & Deployment
- **API Keys**: All sensitive credentials reside in the `.env` file and are never exposed to the client.
- **Deployment**:
    *   **Frontend**: Hosted on GitHub Pages via relative path routing.
    *   **Backend**: Hosted on Back4App with dynamic port binding and CORS protection.

---

*“Data without insight is just noise. TERRA-X provides the insight.”* 🌍🧪
