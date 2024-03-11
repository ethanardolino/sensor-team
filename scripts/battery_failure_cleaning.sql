WITH clean AS (
    SELECT
        CAST(`Baseline-Total-Energy-Yield-kJ` as REAL) as released_energy,
        CAST(`Avg-Cell-Temp-At-Trigger-degC` as REAL) as cell_temp,
        `Cell-Description` as battery, 
        `Cell-Format` as format,
        `Trigger-Mechanism` as trigger,
        CAST(`Pre-Test-Cell-Mass-g` as REAL) as mass,
        CAST(`Cell-Capacity-Ah` as REAL) as capacity,
        CAST(`Cell-Energy-Wh` as REAL) as full_charge_energy,
        CAST(`Pre-Test-Cell-Open-Circuit-Voltage-V` as REAL) as full_charge_voltage,
        CAST(`Energy-Applied-to-Trigger-kJ` as REAL) as trigger_energy,
        CAST(`Heater-Power-W` as REAL) as heater_power,
        CAST(`Conductive-Heat-Loss-Rate-kJs-1` as REAL) as heat_loss
    FROM
        battery
)
SELECT
    MAX(cell_temp) as max_cell_temp, trigger, format, heat_loss, capacity
FROM
    clean
GROUP BY capacity;

    