public class Main {
    
}
import React, { useState, useMemo } from 'react';
import { RefreshCcw, Zap, DollarSign, Target, Ruler } from 'lucide-react';

// --- System Constants for Water and DHN Design ---
const WATER_DENSITY_KG_M3 = 1000; // kg/m3 (approx at DHN temps)
const WATER_SPECIFIC_HEAT_J_KG_K = 4186; // J/kg·K
const PUMP_EFFICIENCY = 0.75; // 75% efficiency (typical for pumps)

// Standard Commercial Pipe Sizes (Diameter in meters) and Estimated Installed Cost (£/m)
const PIPE_SIZES = [
    { dn: 50, diameter: 0.05, costPerMeter: 150 },
    { dn: 80, diameter: 0.08, costPerMeter: 250 },
    { dn: 100, diameter: 0.10, costPerMeter: 350 },
    { dn: 125, diameter: 0.125, costPerMeter: 500 },
    { dn: 150, diameter: 0.15, costPerMeter: 700 },
    { dn: 200, diameter: 0.20, costPerMeter: 1200 },
    { dn: 250, diameter: 0.25, costPerMeter: 2000 },
];

// --- DHN Velocity Optimizer Component ---
const App = () => {
    // Initial State based on user's previous data and common defaults
    const [inputs, setInputs] = useState({
        heatLoadKw: 9.6, // kW to be removed
        tempDropDegC: 15, // Design delta T (T_supply - T_return)
        pipeLengthM: 500, // Total DHN length
        lifetimeYears: 20,
        opHoursYear: 8000, // Annual Operating Hours
        elecCostPoundKwh: 0.20, // £/kWh
        pumpStationCost: 50000, // CAPEX cost per intermediate station
        numPumpStations: 1, // Start with 1 primary station
    });

    const [results, setResults] = useState([]);
    const [optimalResult, setOptimalResult] = useState(null);

    const handleChange = (e) => {
        const { name, value, type } = e.target;
        setInputs(prev => ({
            ...prev,
            [name]: type === 'number' ? parseFloat(value) || 0 : value,
        }));
    };

    // Calculate the Volumetric Flow Rate (VFR) which is constant for all velocities
    const volumetricFlowRate = useMemo(() => {
        if (inputs.heatLoadKw === 0 || inputs.tempDropDegC === 0) return 0;
        // Q (W) = VFR (m3/s) * rho * Cp * deltaT (K)
        const Q_W = inputs.heatLoadKw * 1000;
        return Q_W / (WATER_DENSITY_KG_M3 * WATER_SPECIFIC_HEAT_J_KG_K * inputs.tempDropDegC);
    }, [inputs.heatLoadKw, inputs.tempDropDegC]);

    // Simplified Pressure Drop Calculation (using Darcy-Weisbach approximation for friction)
    const calculatePressureDrop = (v, D, L) => {
        // Simplified friction factor (f) approximation based on pipe size and flow
        // The pressure drop is proportional to v^2 and inversely proportional to D^5
        // Using a standard head loss formula proxy:
        const f = 0.02 * Math.pow(D, -0.25); // Rough proxy for typical DHN pipe friction
        const dynamicPressure = 0.5 * WATER_DENSITY_KG_M3 * Math.pow(v, 2);
        const deltaP = f * (L / D) * dynamicPressure;

        // Add 20% for minor losses (bends, valves, fittings)
        return deltaP * 1.2; // Pressure Drop in Pascals (Pa)
    };

    const calculateCosts = () => {
        if (volumetricFlowRate === 0) {
            setResults([]);
            setOptimalResult(null);
            return;
        }

        let bestResult = null;
        let minTotalCost = Infinity;
        const analysis = [];

        // Iterate through velocity range (0.5 m/s to 4.0 m/s)
        for (let v = 0.5; v <= 4.0; v += 0.1) {
            const velocity = parseFloat(v.toFixed(1));

            // 1. Determine Required Diameter and CAPEX
            const area = volumetricFlowRate / velocity; // m^2
            const requiredDiameter = Math.sqrt((4 * area) / Math.PI); // m

            // Snap to nearest commercial size (select the size that meets or exceeds the required diameter)
            const pipeSelection = PIPE_SIZES.find(pipe => pipe.diameter >= requiredDiameter);

            if (!pipeSelection) continue; // Skip if diameter is too large

            // Pipe CAPEX
            const pipeCapex = pipeSelection.costPerMeter * inputs.pipeLengthM;
            // Pumping Station CAPEX (including intermediate stations)
            const pumpCapex = inputs.pumpStationCost * inputs.numPumpStations;
            const totalCapex = pipeCapex + pumpCapex;

            // 2. Calculate OPEX based on Pressure Drop and Pumping Power
            const deltaP = calculatePressureDrop(velocity, pipeSelection.diameter, inputs.pipeLengthM); // Pa

            // Pumping Power (W) = VFR * DeltaP / Efficiency
            const pumpingPowerW = (volumetricFlowRate * deltaP) / PUMP_EFFICIENCY;
            const pumpingPowerKw = pumpingPowerW / 1000;

            // Annual OPEX (£)
            const annualOpex = pumpingPowerKw * inputs.opHoursYear * inputs.elecCostPoundKwh;

            // Total Lifetime Cost (£)
            const totalOpexLifetime = annualOpex * inputs.lifetimeYears;
            const totalCost = totalCapex + totalOpexLifetime;

            const currentResult = {
                velocity,
                dn: pipeSelection.dn,
                totalCapex: Math.round(totalCapex),
                annualOpex: Math.round(annualOpex),
                totalCost: Math.round(totalCost),
                pumpingPowerKw: pumpingPowerKw.toFixed(2),
                deltaPPa: Math.round(deltaP),
            };

            analysis.push(currentResult);

            if (totalCost < minTotalCost) {
                minTotalCost = totalCost;
                bestResult = currentResult;
            }
        }

        setResults(analysis);
        setOptimalResult(bestResult);
    };

    // Run calculation when component mounts and whenever inputs change
    React.useEffect(() => {
        calculateCosts();
    }, [inputs, volumetricFlowRate]);

    // Helper for input components
    const Input = ({ label, name, value, unit, icon: Icon, step = 1 }) => (
        <div className="flex flex-col space-y-1">
            <label htmlFor={name} className="text-sm font-medium text-gray-700 flex items-center">
                <Icon className="w-4 h-4 mr-1 text-indigo-500" /> {label} ({unit})
            </label>
            <input
                id={name}
                name={name}
                type="number"
                step={step}
                min="0"
                value={value}
                onChange={handleChange}
                className="p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-50 p-4 sm:p-8 font-sans">
            <script src="https://cdn.tailwindcss.com"></script>
            <div className="max-w-7xl mx-auto bg-white p-6 rounded-xl shadow-2xl">
                <h1 className="text-3xl font-extrabold text-indigo-700 mb-6 border-b pb-2">
                    DHN Velocity and Cost Optimizer
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 p-4 bg-indigo-50 rounded-lg border-l-4 border-indigo-400">
                    <Input label="Heat Load" name="heatLoadKw" unit="kW" icon={Zap} step={0.1} value={inputs.heatLoadKw} />
                    <Input label="Design Temp Drop" name="tempDropDegC" unit="°C" icon={Target} value={inputs.tempDropDegC} />
                    {/* ICON CHANGE: Using Ruler for Pipe Length due to lucide-react export issue. */}
                    <Input label="Pipe Length" name="pipeLengthM" unit="m" icon={Ruler} value={inputs.pipeLengthM} />
                    <Input label="System Lifetime" name="lifetimeYears" unit="Years" icon={RefreshCcw} value={inputs.lifetimeYears} />

                    <div className="md:col-span-4 h-px bg-indigo-200 my-2"></div>

                    <Input label="Electricity Cost" name="elecCostPoundKwh" unit="£/kWh" icon={DollarSign} step={0.01} value={inputs.elecCostPoundKwh} />
                    <Input label="Operating Hours" name="opHoursYear" unit="h/year" icon={RefreshCcw} value={inputs.opHoursYear} />
                    <Input label="Pump Station Cost" name="pumpStationCost" unit="£" icon={DollarSign} value={inputs.pumpStationCost} />
                    <Input label="Number of Pump Stations" name="numPumpStations" unit="Units" icon={Zap} value={inputs.numPumpStations} />
                </div>

                {volumetricFlowRate > 0 && (
                    <div className="mb-8 text-center bg-gray-100 p-4 rounded-lg">
                        <p className="text-lg font-semibold text-gray-800">
                            Required Volumetric Flow Rate (VFR) is: <span className="text-xl text-indigo-600 font-bold">{volumetricFlowRate.toFixed(4)} m³/s</span>
                        </p>
                    </div>
                )}

                {optimalResult && (
                    <div className="p-6 mb-8 border-4 border-green-500 bg-green-50 rounded-xl shadow-lg">
                        <h2 className="text-2xl font-bold text-green-700 mb-4 flex items-center">
                            <Target className="w-6 h-6 mr-2" /> Optimal Velocity Found
                        </h2>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
                            <div className="p-3 bg-white rounded-lg shadow">
                                <p className="text-sm text-gray-500">Optimum Velocity</p>
                                <p className="text-2xl font-extrabold text-green-600">{optimalResult.velocity} m/s</p>
                            </div>
                            <div className="p-3 bg-white rounded-lg shadow">
                                <p className="text-sm text-gray-500">Pipe Size (DN)</p>
                                <p className="text-2xl font-extrabold text-green-600">DN{optimalResult.dn}</p>
                            </div>
                            <div className="p-3 bg-white rounded-lg shadow">
                                <p className="text-sm text-gray-500">Total CAPEX (Est.)</p>
                                <p className="text-2xl font-extrabold text-green-600">£{optimalResult.totalCapex.toLocaleString()}</p>
                            </div>
                            <div className="p-3 bg-white rounded-lg shadow">
                                <p className="text-sm text-gray-500">Total Lifetime Cost</p>
                                <p className="text-2xl font-extrabold text-green-600">£{optimalResult.totalCost.toLocaleString()}</p>
                            </div>
                        </div>
                        <div className="mt-4 text-sm text-gray-700">
                            <p>Annual Operating Cost (OPEX): **£{optimalResult.annualOpex.toLocaleString()}**</p>
                            <p>Required Pumping Power: **{optimalResult.pumpingPowerKw} kW**</p>
                            <p>Total Pressure Drop: **{optimalResult.deltaPPa.toLocaleString()} Pa**</p>
                        </div>
                    </div>
                )}

                <h2 className="text-2xl font-bold text-gray-800 mb-4">Detailed Analysis Table</h2>
                <div className="overflow-x-auto rounded-lg shadow-md">
                    <table className="min-w-full divide-y divide-gray-300">
                        <thead className="bg-gray-200">
                            <tr>
                                <th className="p-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Velocity (m/s)</th>
                                <th className="p-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Pipe Size (DN)</th>
                                <th className="p-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">CAPEX (£)</th>
                                <th className="p-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">Annual OPEX (£)</th>
                                <th className="p-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">Total Lifetime Cost (£)</th>
                                <th className="p-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">Pumping Power (kW)</th>
                                <th className="p-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">∆P (Pa)</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {results.map((result, index) => (
                                <tr key={index} className={result === optimalResult ? 'bg-green-100 font-semibold' : 'hover:bg-gray-50'}>
                                    <td className="p-3 whitespace-nowrap">{result.velocity.toFixed(1)}</td>
                                    <td className="p-3 whitespace-nowrap">DN{result.dn}</td>
                                    <td className="p-3 whitespace-nowrap text-right">{result.totalCapex.toLocaleString()}</td>
                                    <td className="p-3 whitespace-nowrap text-right">{result.annualOpex.toLocaleString()}</td>
                                    <td className="p-3 whitespace-nowrap text-right">{result.totalCost.toLocaleString()}</td>
                                    <td className="p-3 whitespace-nowrap text-right">{result.pumpingPowerKw}</td>
                                    <td className="p-3 whitespace-nowrap text-right">{result.deltaPPa.toLocaleString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <style>{`
                    /* Hide scrollbar for inputs */
                    input[type="number"]::-webkit-outer-spin-button,
                    input[type="number"]::-webkit-inner-spin-button {
                        -webkit-appearance: none;
                        margin: 0;
                    }
                    input[type="number"] {
                        -moz-appearance: textfield;
                    }
                `}</style>

            </div>
        </div>
    );
};

export default App;
