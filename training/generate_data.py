import random
import numpy as np
import pandas as pd
from pathlib import Path

random.seed(42)
np.random.seed(42)

n = 1000

sizes = ['S', 'M', 'L', 'XL', 'XXL']
topsheet_materials = ['Nonwoven', 'Spunlace', 'Airlaid', 'Composite']
sap_types = ['SuperAbsorbent', 'Hybrid', 'HighFlux']
pulp_types = ['SoftPulp', 'RefinedPulp', 'BleachedPulp']
additives_list = ['NoAdditives', 'Softener', 'OdorControl', 'Barrier']
suppliers = ['SupplierA', 'SupplierB', 'SupplierC', 'SupplierD']
core_shapes = ['Round', 'Oval', 'Rectangular']

rows = []
for _ in range(n):
    size = random.choice(sizes)
    topsheet = random.choice(topsheet_materials)
    sap_type = random.choice(sap_types)
    pulp_type = random.choice(pulp_types)
    additives = random.choice(additives_list)
    supplier = random.choice(suppliers)
    core_shape = random.choice(core_shapes)

    sap_ratio = round(np.clip(np.random.normal(0.24, 0.05), 0.10, 0.40), 3)
    core_gsm = int(np.clip(np.random.normal(220, 25), 160, 320))
    hydro_score = round(np.clip(np.random.normal(8.5, 1.1), 4.0, 12.0), 2)
    channels = int(np.clip(np.random.normal(3.2, 0.8), 1, 6))

    size_factor = {'S': 0.06, 'M': 0.03, 'L': 0.0, 'XL': -0.02, 'XXL': -0.04}[size]
    topsheet_factor = {'Nonwoven': 0.01, 'Spunlace': 0.02, 'Airlaid': 0.03, 'Composite': 0.04}[topsheet]
    sap_factor = {'SuperAbsorbent': 0.05, 'Hybrid': 0.03, 'HighFlux': 0.02}[sap_type]
    pulp_factor = {'SoftPulp': 0.01, 'RefinedPulp': 0.02, 'BleachedPulp': 0.03}[pulp_type]
    additive_factor = {'NoAdditives': 0.0, 'Softener': 0.01, 'OdorControl': 0.02, 'Barrier': 0.03}[additives]
    supplier_factor = {'SupplierA': 0.0, 'SupplierB': 0.01, 'SupplierC': 0.015, 'SupplierD': 0.02}[supplier]
    shape_factor = {'Round': 0.0, 'Oval': 0.01, 'Rectangular': 0.015}[core_shape]

    material_cost = round(max(0.12, 0.16 + size_factor + topsheet_factor + sap_factor + pulp_factor + additive_factor + supplier_factor + shape_factor + (sap_ratio - 0.24) * 0.4 + (core_gsm - 220) * 0.0003 + (hydro_score - 8.5) * 0.004), 3)
    absorption = int(round(max(3000, 4800 + (sap_ratio * 10000) + (hydro_score * 180) + (core_gsm * 5) + channels * 150 + size_factor * 800 + topsheet_factor * 300 + sap_factor * 500 + pulp_factor * 250 + additive_factor * 200 + supplier_factor * 120 + shape_factor * 150)))

    rows.append({
        'diaperSize': size,
        'topsheetMaterial': topsheet,
        'sapType': sap_type,
        'pulpType': pulp_type,
        'additives': additives,
        'supplier': supplier,
        'sapRatio': sap_ratio,
        'coreGsm': core_gsm,
        'hydroScore': hydro_score,
        'channels': channels,
        'coreShaping': core_shape,
        'materialCost': material_cost,
        'absorption': absorption,
    })

frame = pd.DataFrame(rows)
output_path = Path('dataset/diaper_training_data.csv')
output_path.parent.mkdir(parents=True, exist_ok=True)
frame.to_csv(output_path, index=False)
print(f'Wrote {len(frame)} rows to {output_path}')
