import React, { useState, Suspense, useCallback, useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import Globe from '../components/Globe';
import { motion, AnimatePresence } from 'framer-motion';
import { FaSearch, FaTimes, FaGlobeAmericas, FaSlidersH, FaWind, FaUsers, FaChartLine, FaBoxOpen, FaFlask, FaCloudSun, FaExclamationTriangle } from 'react-icons/fa';

// --- CONFIGURATION ---
const API_BASE = import.meta.env.VITE_API_URL || "https://terrax1-gfp5u3xc.b4a.run";

const Home = () => {
    const [result, setResult] = useState(null);
    const [baseline, setBaseline] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [activeLocation, setActiveLocation] = useState(null);
    const [error, setError] = useState(null);
    const [engineStatus, setEngineStatus] = useState("CHECKING...");
    const [searchQuery, setSearchQuery] = useState("");
    const [isSearching, setIsSearching] = useState(false);
    const [isPanelOpen, setIsPanelOpen] = useState(true);

    // Simulation Parameters
    const [params, setParams] = useState({
        carbon: 0,
        pop: 0,
        econ: 0,
        resource: 0
    });

    // Check Server Health (Safe Polling)
    useEffect(() => {
        let isActive = true;
        const check = async () => {
            try {
                const res = await fetch(`${API_BASE}/health`);
                const data = await res.json();
                if (isActive && data.status === "online") {
                    setEngineStatus("ONLINE");
                }
            } catch (err) {
                if (isActive) setEngineStatus("CONNECTING...");
            }
        };

        check();
        const interval = setInterval(check, 10000);
        return () => {
            isActive = false;
            clearInterval(interval);
        };
    }, []);

    const handleSearch = async (e) => {
        if (e) e.preventDefault();
        if (!searchQuery.trim()) return;

        setIsSearching(true);
        try {
            const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=1`);
            const data = await res.json();
            if (data && data.length > 0) {
                const place = data[0];
                const loc = {
                    name: place.display_name.split(',')[0],
                    lat: parseFloat(place.lat),
                    lon: parseFloat(place.lon)
                };
                setActiveLocation(loc);
                setSearchQuery("");
            } else {
                throw new Error("Location not found");
            }
        } catch (err) {
            console.error(err);
        } finally {
            setIsSearching(false);
        }
    };

    const handleParamChange = (key, val) => {
        let num = parseInt(val);
        if (isNaN(num)) num = 0;
        const limits = { carbon: [-100, 100], pop: [-50, 100], econ: [-50, 100], resource: [-50, 100] };
        const [min, max] = limits[key];
        num = Math.max(min, Math.min(max, num));
        setParams(prev => ({ ...prev, [key]: num }));
    };

    const runSimulation = useCallback(async (locData) => {
        const location = locData || activeLocation;
        if (!location) return;

        setActiveLocation(location);
        setIsLoading(true);
        setResult(null);
        setBaseline(null);
        setError(null);

        try {
            const response = await fetch(`${API_BASE}/api/simulate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    location: location.name,
                    lat: location.lat,
                    lon: location.lon,
                    carbon_change: params.carbon,
                    pop_growth: params.pop,
                    econ_shift: params.econ,
                    resource_use: params.resource
                })
            });

            {/* Auto-close panel on mobile when simulation starts */ }
            if (window.innerWidth < 768) {
                setIsPanelOpen(false);
            }

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || "Engine failure");

            setResult(data.analysis);
            setBaseline(data.baseline);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    }, [activeLocation, params]);

    return (
        <div className="vh-100 w-100 overflow-hidden position-relative bg-black text-white font-sans">

            {/* Background Canvas */}
            <div className="w-100 h-100 position-absolute top-0 start-0" style={{ zIndex: 0 }}>
                <Canvas camera={{ position: [0, 0, 7], fov: window.innerWidth < 768 ? 65 : 40 }}>
                    <ambientLight intensity={0.5} />
                    <Suspense fallback={null}>
                        <Globe onCountrySelect={runSimulation} targetLocation={activeLocation} />
                    </Suspense>
                </Canvas>
            </div>

            {/* Header / Search Area */}
            <div className="position-absolute top-0 start-0 p-4 w-100 d-flex flex-column flex-md-row justify-content-between align-items-start pointer-events-none" style={{ zIndex: 100 }}>
                <div className="pointer-events-auto mb-4 mb-md-0">
                    <h1 className="h4 fw-bold tracking-tighter text-white mb-0 d-flex align-items-center gap-3">
                        <div className="p-2 rounded-4 bg-info bg-opacity-20 shadow-glow"><FaFlask className="text-info fs-5" /></div>
                        TERRA-X SCENARIO LAB
                    </h1>
                    <div className="d-flex align-items-center gap-2 x-small mt-2 ms-5">
                        <div className={`spinner-grow spinner-grow-sm ${engineStatus === 'ONLINE' ? 'text-info' : 'text-danger'}`} style={{ width: '6px', height: '6px' }} />
                        <span className="opacity-50">ENGINE:</span>
                        <span className={engineStatus === 'ONLINE' ? 'text-info' : 'text-danger'} style={{ letterSpacing: '2px' }}>{engineStatus}</span>
                    </div>
                </div>

                {/* Global Place Search */}
                <form onSubmit={handleSearch} className="pointer-events-auto search-container d-flex align-items-center gap-2 p-1 rounded-pill glass-panel w-sm-100" style={{ minWidth: '300px' }}>
                    <div className="ms-3 text-info opacity-50"><FaSearch /></div>
                    <input
                        type="text"
                        placeholder="SEARCH SECTOR OR CITY..."
                        className="bg-transparent border-0 text-white x-small flex-grow-1 outline-none py-2 px-1"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        style={{ outline: 'none' }}
                    />
                    <button type="submit" className="btn btn-info btn-sm rounded-pill px-4 tracking-widest fw-bold" disabled={isSearching}>
                        {isSearching ? "FLYING..." : "GOTO"}
                    </button>
                </form>
            </div>

            {/* Variables Panel Toggle Button */}
            {!isPanelOpen && (
                <motion.div
                    initial={{ x: -50, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    className="position-absolute top-50 start-0 translate-middle-y ms-2 ms-md-4 pointer-events-auto"
                    style={{ zIndex: 90 }}
                >
                    <button
                        onClick={() => setIsPanelOpen(true)}
                        className="btn btn-dark border border-info border-opacity-50 text-info rounded-circle d-flex align-items-center justify-content-center shadow-glow"
                        style={{ width: '48px', height: '48px', backdropFilter: 'blur(10px)', background: 'rgba(0,0,0,0.6)' }}
                    >
                        <FaSlidersH />
                    </button>
                </motion.div>
            )}

            {/* Variables Panel (Left) */}
            <AnimatePresence>
                {isPanelOpen && (
                    <motion.div
                        initial={{ x: -50, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: -50, opacity: 0 }}
                        className="position-absolute top-50 start-0 translate-middle-y ms-4 p-4 glass-panel pointer-events-auto"
                        style={{ width: '340px', zIndex: 250, borderRadius: '24px' }}
                    >
                        <div className="d-flex align-items-center justify-content-between mb-4">
                            <div className="d-flex align-items-center gap-3 text-info opacity-75">
                                <FaSlidersH /> <span className="small fw-black tracking-widest text-uppercase">Variables</span>
                            </div>
                            <button onClick={() => setIsPanelOpen(false)} className="btn btn-sm text-white-50 p-1 border-0 rounded-circle hover-bg-white-10"><FaTimes /></button>
                        </div>

                        {[
                            { key: 'carbon', label: 'CARBON EMISSIONS', icon: <FaWind className="text-info" />, min: -100, max: 100 },
                            { key: 'pop', label: 'POPULATION GROWTH', icon: <FaUsers />, min: -50, max: 100 },
                            { key: 'econ', label: 'ECONOMIC SHIFT', icon: <FaChartLine />, min: -50, max: 100 },
                            { key: 'resource', label: 'RESOURCE USE', icon: <FaBoxOpen />, min: -50, max: 100 }
                        ].map((varItem) => (
                            <div className="mb-4" key={varItem.key}>
                                <div className="d-flex justify-content-between align-items-center x-small mb-2 text-white-50">
                                    <span className="d-flex align-items-center gap-2">{varItem.icon} {varItem.label}</span>
                                    <div className="input-group-custom d-flex align-items-center gap-1">
                                        <input
                                            type="number"
                                            className="number-input-small"
                                            value={params[varItem.key]}
                                            onChange={(e) => handleParamChange(varItem.key, e.target.value)}
                                        />
                                        <span className="opacity-50">%</span>
                                    </div>
                                </div>
                                <input type="range" className="w-100 custom-slider" min={varItem.min} max={varItem.max} value={params[varItem.key]} onChange={(e) => handleParamChange(varItem.key, e.target.value)} />
                            </div>
                        ))}

                        <button
                            onClick={() => runSimulation()}
                            className={`btn w-100 rounded-pill py-3 fw-bold tracking-widest mt-4 shadow-lg transition-all ${!activeLocation ? 'btn-secondary opacity-50' : 'btn-info btn-simulate'}`}
                            disabled={!activeLocation || isLoading}
                        >
                            {!activeLocation ? "SEARCH OR SELECT REGION" : isLoading ? "PROCESSING..." : "INITIATE SIMULATION"}
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Analysis Panel (Right/Bottom) */}
            <AnimatePresence>
                {activeLocation && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: 30 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: 30 }}
                        className="position-absolute bottom-0 end-0 m-4 p-4 glass-panel pointer-events-auto"
                        style={{
                            width: window.innerWidth < 768 ? 'calc(100% - 32px)' : '520px',
                            zIndex: 200,
                            background: 'rgba(5, 5, 10, 0.98)',
                            borderRadius: '24px',
                            border: '1px solid rgba(0, 243, 255, 0.2)'
                        }}
                    >
                        <div className="d-flex justify-content-between align-items-start mb-4">
                            <div className="d-flex align-items-center gap-3">
                                <div className="p-3 rounded-4 bg-info bg-opacity-10 text-info fs-4"><FaGlobeAmericas /></div>
                                <div>
                                    <span className="x-small text-info opacity-75 tracking-tighter text-uppercase">TARGET // {activeLocation.name}</span>
                                    <h5 className="fw-bold mb-0 text-white">STRATEGIC SECTOR ANALYSIS</h5>
                                </div>
                            </div>
                            <button onClick={() => { setActiveLocation(null); setBaseline(null); setResult(null); setError(null); }} className="btn btn-sm text-white-50 p-2 border-0"><FaTimes /></button>
                        </div>

                        {baseline && !error && (
                            <div className="mb-4 p-3 rounded-4 bg-white bg-opacity-5 border border-white border-opacity-10 d-flex justify-content-between align-items-center">
                                <div>
                                    <div className="x-small text-info opacity-40 mb-1">LOCAL CLIMATE BASELINE</div>
                                    <div className="d-flex align-items-center gap-3">
                                        <div className="h4 mb-0 fw-bold text-info">{Math.round(baseline.temp)}°C</div>
                                        <div className="small text-uppercase tracking-wider font-monospace text-white opacity-90">{baseline.desc}</div>
                                    </div>
                                </div>
                                <FaCloudSun className="fs-1 text-info opacity-10" />
                            </div>
                        )}

                        <div className="simulation-output p-4 rounded-4 bg-info bg-opacity-5 border border-info border-opacity-10" style={{ minHeight: '200px' }}>
                            {isLoading ? (
                                <div className="py-5 text-center">
                                    <div className="spinner-border spinner-border-sm text-info mb-4 shadow-glow" />
                                    <div className="small text-white-50 tracking-widest">CALCULATING PROBABILITIES...</div>
                                </div>
                            ) : error ? (
                                <div className="py-4 text-center">
                                    <FaExclamationTriangle className="fs-2 mb-3 text-danger" />
                                    <div className="small fw-bold text-danger mb-2 uppercase">ENGINE_ERROR</div>
                                    <div className="x-small text-white opacity-70 font-monospace px-3">{error}</div>
                                </div>
                            ) : result ? (
                                <div className="lh-lg">
                                    <div className="text-info x-small mb-3 fw-bold tracking-widest border-bottom border-info border-opacity-20 pb-2">PRED-ENGINE OUTPUT:</div>
                                    <p className="text-white fw-medium font-monospace" style={{ fontSize: '1rem', lineHeight: '1.7' }}>{result}</p>
                                </div>
                            ) : (
                                <div className="py-5 text-center opacity-30">
                                    <FaSearch className="fs-1 mb-3 text-info" />
                                    <p className="small tracking-widest">USE SEARCH OR CLICK GLOBE TO ACTIVATE SECTOR</p>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <style>{`
                .glass-panel {
                    box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9);
                    backdrop-filter: blur(50px);
                    border: 1px solid rgba(0, 243, 255, 0.1);
                }
                .shadow-glow { filter: drop-shadow(0 0 10px rgba(0, 243, 255, 0.8)); }
                .x-small { font-size: 0.65rem; font-weight: 800; letter-spacing: 0.25em; }
                .search-container { background: rgba(0, 0, 0, 0.6); border: 1px solid rgba(0, 243, 255, 0.2); transition: all 0.3s ease; }
                .search-container:focus-within { border-color: #00f3ff; box-shadow: 0 0 20px rgba(0, 243, 255, 0.2); }
                
                .number-input-small {
                    background: rgba(0, 243, 255, 0.05);
                    border: 1px solid rgba(0, 243, 255, 0.2);
                    color: #00f3ff;
                    font-family: 'Orbitron', monospace;
                    width: 60px;
                    font-weight: bold;
                    outline: none;
                    font-size: 0.85rem;
                    text-align: center;
                    border-radius: 6px;
                }
                
                .custom-slider {
                    -webkit-appearance: none;
                    width: 100%;
                    height: 12px;
                    background: transparent;
                    outline: none;
                }
                .custom-slider::-webkit-slider-runnable-track {
                    width: 100%;
                    height: 2px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 2px;
                }
                .custom-slider::-webkit-slider-thumb {
                    -webkit-appearance: none;
                    width: 16px;
                    height: 16px;
                    background: #00f3ff;
                    border-radius: 50%;
                    cursor: pointer;
                    margin-top: -7px;
                    border: 2px solid white;
                    box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
                }
                .spacing-wider { letter-spacing: 0.4rem; text-transform: uppercase; }

                /* Mobile Optimizations */
                @media (max-width: 768px) {
                    .glass-panel {
                        backdrop-filter: blur(20px);
                        margin: 10px !important;
                        width: calc(100% - 20px) !important;
                    }
                    .h4 { font-size: 1.1rem; }
                    .search-container { min-width: auto !important; width: 100%; }
                    .number-input-small { width: 45px; font-size: 0.75rem; }
                }
            `}</style>
        </div>
    );
};

export default Home;
