import React, { useRef, useState, useMemo, Suspense, useEffect } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { Html, Sphere, useTexture, OrbitControls, Stars, Sparkles } from '@react-three/drei';
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import * as THREE from 'three';
import { motion, AnimatePresence } from 'framer-motion';

const EARTH_TEXTURE_URL = "https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_atmos_2048.jpg";
const NIGHT_TEXTURE_URL = "https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_lights_2048.png";
const CLOUDS_URL = "https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_clouds_1024.png";
const BUMP_URL = "https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_normal_2048.jpg";

// Predefined major hubs (Beacon Sectors)
const regions = [
    { name: "North America", lat: 37.0902, lon: -95.7129 },
    { name: "South Asia", lat: 20.5937, lon: 78.9629 },
    { name: "East Asia", lat: 36.2048, lon: 138.2529 },
    { name: "South America", lat: -14.2350, lon: -51.9253 },
    { name: "Oceania", lat: -25.2744, lon: 133.7751 },
    { name: "Europe", lat: 51.1657, lon: 10.4515 },
    { name: "Middle East", lat: 23.8859, lon: 45.0792 },
    { name: "Africa", lat: 1.6508, lon: 16.3333 },
];

function RegionMarker({ lat, lon, name, onSelect, active }) {
    const [hovered, setHovered] = useState(false);
    const pulseRef = useRef();

    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    const radius = 2.05;

    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const z = (radius * Math.sin(phi) * Math.sin(theta));
    const y = (radius * Math.cos(phi));

    useFrame(({ clock }) => {
        if (pulseRef.current) {
            const s = (active ? 1.5 : 1) + Math.sin(clock.getElapsedTime() * 4) * 0.2;
            pulseRef.current.scale.set(s, s, s);
            pulseRef.current.opacity = (active ? 0.8 : 0.4) + Math.sin(clock.getElapsedTime() * 4) * 0.3;
        }
    });

    return (
        <group position={[x, y, z]}>
            <mesh ref={pulseRef}>
                <sphereGeometry args={[0.04, 16, 16]} />
                <meshBasicMaterial color={active ? "#ff3e3e" : "#00f3ff"} transparent opacity={0.6} />
            </mesh>

            <mesh
                onPointerEnter={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = 'pointer'; }}
                onPointerLeave={(e) => { e.stopPropagation(); setHovered(false); document.body.style.cursor = 'auto'; }}
                onClick={(e) => {
                    e.stopPropagation();
                    onSelect({ name, lat, lon });
                }}
            >
                <sphereGeometry args={[0.2, 16, 16]} />
                <meshBasicMaterial transparent opacity={0} depthWrite={false} />
            </mesh>

            <Html center distanceFactor={10}>
                <AnimatePresence>
                    {(hovered || active) && (
                        <motion.div
                            initial={{ scale: 0, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0, opacity: 0 }}
                            style={{
                                background: active ? 'rgba(255, 62, 62, 0.15)' : 'rgba(0, 243, 255, 0.15)',
                                color: active ? '#ff3e3e' : '#00f3ff',
                                padding: '4px 12px',
                                borderRadius: '20px',
                                fontSize: '10px',
                                fontWeight: 'bold',
                                border: `1px solid ${active ? '#ff3e3e' : '#00f3ff'}`,
                                whiteSpace: 'nowrap',
                                pointerEvents: 'none',
                                textShadow: `0 0 10px ${active ? '#ff3e3e' : '#00f3ff'}`,
                                backdropFilter: 'blur(10px)'
                            }}
                        >
                            {active ? 'TARGET SECTOR: ' : ''}{name.toUpperCase()}
                        </motion.div>
                    )}
                </AnimatePresence>
            </Html>
        </group>
    );
}

function SelectionMarker({ lat, lon, name }) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    const radius = 2.06;

    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const z = (radius * Math.sin(phi) * Math.sin(theta));
    const y = (radius * Math.cos(phi));

    return (
        <group position={[x, y, z]}>
            <mesh>
                <sphereGeometry args={[0.05, 16, 16]} />
                <meshBasicMaterial color="#ff3e3e" />
            </mesh>
            <mesh rotation={[Math.PI / 2, 0, 0]}>
                <ringGeometry args={[0.08, 0.1, 32]} />
                <meshBasicMaterial color="#ff3e3e" transparent opacity={0.6} side={THREE.DoubleSide} />
            </mesh>
            <Html center distanceFactor={10}>
                <div style={{
                    background: 'rgba(255, 62, 62, 0.1)',
                    color: '#ff3e3e',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '11px',
                    fontWeight: 'bold',
                    border: '1px solid #ff3e3e',
                    whiteSpace: 'nowrap',
                    backdropFilter: 'blur(10px)',
                    textShadow: '0 0 10px #ff3e3e'
                }}>
                    LOCKED // {name.toUpperCase()}
                </div>
            </Html>
        </group>
    );
}

function EarthContent({ onCountrySelect, targetLocation }) {
    const globeRef = useRef();
    const cloudsRef = useRef();
    const controlsRef = useRef();
    const { camera } = useThree();

    const textures = useTexture({
        dayMap: EARTH_TEXTURE_URL,
        nightMap: NIGHT_TEXTURE_URL,
        cloudsMap: CLOUDS_URL,
        bumpMap: BUMP_URL
    });

    // Camera Flight Logic
    useEffect(() => {
        if (targetLocation && controlsRef.current) {
            const { lat, lon } = targetLocation;
            const phi = (90 - lat) * (Math.PI / 180);
            const theta = (lon + 180) * (Math.PI / 180);
            const radius = 4.5; // Dist for zoom

            const x = -(radius * Math.sin(phi) * Math.cos(theta));
            const z = (radius * Math.sin(phi) * Math.sin(theta));
            const y = (radius * Math.cos(phi));

            const startPos = camera.position.clone();
            const endPos = new THREE.Vector3(x, y, z);

            let progress = 0;
            const animate = () => {
                progress += 0.04;
                if (progress <= 1) {
                    camera.position.lerpVectors(startPos, endPos, progress);
                    requestAnimationFrame(animate);
                }
            };
            animate();
        }
    }, [targetLocation, camera]);

    useFrame(({ clock }) => {
        const elapsed = clock.getElapsedTime();
        if (globeRef.current && !targetLocation) {
            globeRef.current.rotation.y = elapsed * 0.01;
        }
        if (cloudsRef.current) cloudsRef.current.rotation.y = elapsed * 0.012;
    });

    const handleGlobeClick = async (e) => {
        e.stopPropagation();
        const point = e.point;
        const radius = 2; // Earth radius in our scene
        const normalized = point.clone().normalize();

        const lat = Math.asin(normalized.y) * (180 / Math.PI);
        const lon = Math.atan2(normalized.z, -normalized.x) * (180 / Math.PI);

        // Fetch display name from Nominatim
        try {
            const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=3`);
            const data = await res.json();
            const name = data.address.country || data.address.state || "International Sector";
            onCountrySelect({ name, lat, lon });
        } catch (err) {
            onCountrySelect({ name: "Unidentified Sector", lat, lon });
        }
    };

    const isPredefined = targetLocation && regions.some(r => r.name === targetLocation.name);

    return (
        <group>
            <OrbitControls
                ref={controlsRef}
                enablePan={false}
                minDistance={3}
                maxDistance={12}
                enableZoom={true}
                autoRotate={!targetLocation}
                autoRotateSpeed={0.3}
            />

            <color attach="background" args={["#000000"]} />

            <Stars
                radius={300}
                depth={60}
                count={12000}
                factor={4}
                saturation={0}
                fade={true}
                speed={1}
            />

            <Sparkles
                count={100}
                scale={50}
                size={1.5}
                speed={0.2}
                opacity={0.15}
                color="#00f3ff"
            />

            <mesh position={[20, 15, 10]}>
                <sphereGeometry args={[2, 32, 32]} />
                <meshBasicMaterial color="#ffffff" />
                <pointLight intensity={10} distance={100} color="#ffaa00" />
            </mesh>

            <directionalLight position={[20, 15, 10]} intensity={4} color="#ffffff" />
            <pointLight position={[20, 15, 10]} intensity={3} color="#FFF4D6" distance={70} decay={1.5} />

            <group ref={globeRef}>
                <mesh onClick={handleGlobeClick}>
                    <sphereGeometry args={[2.001, 64, 64]} />
                    <meshStandardMaterial
                        map={textures.dayMap}
                        emissiveMap={textures.nightMap}
                        emissive={new THREE.Color("#ffffaa")}
                        emissiveIntensity={1.5}
                        bumpMap={textures.bumpMap}
                        bumpScale={0.15}
                        roughness={0.7}
                        metalness={0.2}
                    />
                </mesh>

                {regions.map((region, idx) => (
                    <RegionMarker
                        key={idx}
                        {...region}
                        active={targetLocation?.name === region.name}
                        onSelect={onCountrySelect}
                    />
                ))}

                {targetLocation && !isPredefined && (
                    <SelectionMarker {...targetLocation} />
                )}
            </group>

            <mesh ref={cloudsRef} pointerEvents="none">
                <sphereGeometry args={[2.02, 64, 64]} />
                <meshStandardMaterial
                    map={textures.cloudsMap}
                    transparent
                    opacity={0.3}
                    blending={THREE.AdditiveBlending}
                />
            </mesh>

            <EffectComposer multisampling={0} disableNormalPass>
                <Bloom intensity={1.5} luminanceThreshold={0.5} radius={0.6} />
            </EffectComposer>
        </group>
    );
}

const Globe = ({ onCountrySelect, targetLocation }) => {
    return (
        <Suspense fallback={null}>
            <EarthContent onCountrySelect={onCountrySelect} targetLocation={targetLocation} />
        </Suspense>
    );
};

export default Globe;
