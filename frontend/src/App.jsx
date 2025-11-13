import { useState, useEffect } from "react";

const API_BASE = "http://127.0.0.1:5000"; // Your Flask backend URL

function App() {
  const [formData, setFormData] = useState({
    name: "",
    aadhar: "",
    address: "",
    documentType: "",
  });

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [apiAvailable, setApiAvailable] = useState(false);

  // 🔍 Check if backend is available
  useEffect(() => {
    const checkAPI = async () => {
      try {
        const res = await fetch(`${API_BASE}/ping`);
        if (res.ok) setApiAvailable(true);
      } catch {
        setApiAvailable(false);
      }
    };
    checkAPI();
  }, []);

  // 🔁 Load past verifications
  const loadFromStorage = async () => {
    if (apiAvailable) {
      try {
        const res = await fetch(`${API_BASE}/history`);
        const data = await res.json();
        setResults(data);
      } catch (err) {
        console.error("Backend error:", err);
      }
    } else {
      const localData = JSON.parse(localStorage.getItem("verifications") || "[]");
      setResults(localData);
    }
  };

  useEffect(() => {
    loadFromStorage();
  }, [apiAvailable]);

  // 💾 Save verification (to backend or local)
  const saveToStorage = async (entry) => {
    if (apiAvailable) {
      try {
        const res = await fetch(`${API_BASE}/verify`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(entry),
        });
        const data = await res.json();
        setResults((prev) => [data, ...prev]);
      } catch (err) {
        console.error("Error saving to backend:", err);
      }
    } else {
      const updated = [entry, ...results];
      setResults(updated);
      localStorage.setItem("verifications", JSON.stringify(updated));
    }
  };

  // 📤 Handle verify button click
  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);

    const mockResponse = {
      fraudProbability: (Math.random() * 100).toFixed(2),
      riskLevel: ["Low", "Medium", "High"][Math.floor(Math.random() * 3)],
      status: "Verified",
      timestamp: new Date().toLocaleString(),
      ...formData,
    };

    if (!apiAvailable) {
      await saveToStorage(mockResponse);
    } else {
      await saveToStorage(formData);
    }

    setFormData({ name: "", aadhar: "", address: "", documentType: "" });
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-cyan-400">
        AI-Powered KYC Fraud Detection
      </h1>

      {/* 🔗 API connection status */}
      <div className="text-center mb-4">
        {apiAvailable ? (
          <span className="text-green-400">✅ Connected to GNN Backend</span>
        ) : (
          <span className="text-red-400">⚠️ Offline Mode (Mock Data)</span>
        )}
      </div>

      {/* 🧾 Form Section */}
      <form
        onSubmit={handleVerify}
        className="bg-gray-800 p-6 rounded-2xl shadow-lg max-w-lg mx-auto mb-8"
      >
        <input
          type="text"
          placeholder="Full Name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
          className="w-full p-2 mb-3 rounded bg-gray-700 text-white"
        />
        <input
          type="text"
          placeholder="Aadhar Number"
          value={formData.aadhar}
          onChange={(e) => setFormData({ ...formData, aadhar: e.target.value })}
          required
          className="w-full p-2 mb-3 rounded bg-gray-700 text-white"
        />
        <input
          type="text"
          placeholder="Address"
          value={formData.address}
          onChange={(e) => setFormData({ ...formData, address: e.target.value })}
          required
          className="w-full p-2 mb-3 rounded bg-gray-700 text-white"
        />
        <select
          value={formData.documentType}
          onChange={(e) => setFormData({ ...formData, documentType: e.target.value })}
          required
          className="w-full p-2 mb-3 rounded bg-gray-700 text-white"
        >
          <option value="">Select Document Type</option>
          <option value="PAN">PAN</option>
          <option value="Voter ID">Voter ID</option>
          <option value="Passport">Passport</option>
        </select>

        <button
          type="submit"
          disabled={loading}
          className="bg-cyan-500 hover:bg-cyan-600 w-full py-2 rounded-lg font-semibold"
        >
          {loading ? "Verifying..." : "Verify Identity"}
        </button>
      </form>

      {/* 📋 Verification Results */}
      <div className="max-w-3xl mx-auto">
        <h2 className="text-xl font-semibold mb-3 text-cyan-300">
          Verification Results
        </h2>
        {results.length === 0 ? (
          <p className="text-gray-400">No verifications yet.</p>
        ) : (
          <div className="space-y-3">
            {results.map((r, i) => (
              <div
                key={i}
                className="p-4 bg-gray-800 rounded-xl border border-gray-700 hover:scale-[1.01] transition"
              >
                <div className="flex justify-between">
                  <span className="font-bold text-lg">{r.name}</span>
                  <span
                    className={`font-semibold ${
                      r.riskLevel === "High"
                        ? "text-red-400"
                        : r.riskLevel === "Medium"
                        ? "text-yellow-400"
                        : "text-green-400"
                    }`}
                  >
                    {r.riskLevel} Risk
                  </span>
                </div>
                <p className="text-sm text-gray-300">
                  Fraud Probability: {r.fraudProbability || "N/A"}%
                </p>
                <p className="text-xs text-gray-400">
                  Verified on: {r.timestamp || "Just now"}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
