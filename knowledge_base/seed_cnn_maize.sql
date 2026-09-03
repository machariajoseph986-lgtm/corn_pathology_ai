-- ============================================================
-- CNN-SUPPORTED MAIZE DISEASES
-- ============================================================
-- Adds structured knowledge for the three disease classes
-- currently predicted by the trained maize CNN:
--
-- 0 = Blight
-- 1 = Common_Rust
-- 2 = Gray_Leaf_Spot
-- 3 = Healthy
--
-- NOTE:
-- The dataset uses the generic class name "Blight".
-- It is intentionally stored as "Maize Blight" here rather
-- than being assumed to mean Northern Corn Leaf Blight.
-- ============================================================


-- ============================================================
-- MAIZE BLIGHT
-- ============================================================

INSERT OR IGNORE INTO health_problems (
    health_problem_id,
    plant_id,
    name,
    type,
    description
)
VALUES (
    'HP_MAIZE_BLIGHT',
    'PLANT_MAIZE',
    'Maize Blight',
    'fungal',
    'A fungal leaf disease class represented as Blight in the maize CNN dataset. The current dataset label does not by itself establish a specific blight species, so the knowledge profile is intentionally kept at the generic maize blight level.'
);


INSERT OR IGNORE INTO symptoms (
    symptom_id,
    health_problem_id,
    category,
    description
)
VALUES
(
    'SYM_MAIZE_BLIGHT_01',
    'HP_MAIZE_BLIGHT',
    'leaf',
    'Leaf lesions or necrotic areas may develop on maize foliage.'
),
(
    'SYM_MAIZE_BLIGHT_02',
    'HP_MAIZE_BLIGHT',
    'foliar',
    'Affected leaf tissue may progressively lose its normal green colour.'
),
(
    'SYM_MAIZE_BLIGHT_03',
    'HP_MAIZE_BLIGHT',
    'severity',
    'Severe foliar infection can reduce functional leaf area and plant performance.'
);


INSERT OR IGNORE INTO transmission (
    transmission_id,
    health_problem_id,
    method,
    description
)
VALUES
(
    'TRANS_MAIZE_BLIGHT_01',
    'HP_MAIZE_BLIGHT',
    'airborne_spores',
    'Fungal foliar pathogens may spread through airborne spores from infected plant material.'
),
(
    'TRANS_MAIZE_BLIGHT_02',
    'HP_MAIZE_BLIGHT',
    'infected_residue',
    'Some maize blight pathogens can survive in infected crop residue and produce inoculum for subsequent crops.'
);


INSERT OR IGNORE INTO conditions (
    condition_id,
    health_problem_id,
    factor,
    value,
    description
)
VALUES
(
    'COND_MAIZE_BLIGHT_01',
    'HP_MAIZE_BLIGHT',
    'moisture',
    'high',
    'Extended leaf wetness and humid conditions can favour fungal foliar disease development.'
),
(
    'COND_MAIZE_BLIGHT_02',
    'HP_MAIZE_BLIGHT',
    'crop_residue',
    'infected',
    'Infected maize residue can provide a source of inoculum for some maize blight pathogens.'
);


INSERT OR IGNORE INTO management (
    management_id,
    health_problem_id,
    category,
    action
)
VALUES
(
    'MGMT_MAIZE_BLIGHT_01',
    'HP_MAIZE_BLIGHT',
    'resistance',
    'Use maize hybrids with appropriate resistance to important foliar blight diseases.'
),
(
    'MGMT_MAIZE_BLIGHT_02',
    'HP_MAIZE_BLIGHT',
    'crop_rotation',
    'Use crop rotation where appropriate to reduce disease pressure from pathogens that survive in crop residue.'
),
(
    'MGMT_MAIZE_BLIGHT_03',
    'HP_MAIZE_BLIGHT',
    'residue_management',
    'Manage infected maize residue to reduce potential sources of fungal inoculum.'
);


INSERT OR IGNORE INTO sources (
    source_id,
    health_problem_id,
    organization,
    title,
    url,
    accessed_date
)
VALUES
(
    'SRC_MAIZE_BLIGHT_01',
    'HP_MAIZE_BLIGHT',
    'University of Delaware Cooperative Extension',
    'Northern Corn Leaf Blight',
    'https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/northern-corn-leaf-blight/',
    '2026-08-25'
),
(
    'SRC_MAIZE_BLIGHT_02',
    'HP_MAIZE_BLIGHT',
    'Cornell University',
    'Northern Corn Leaf Blight',
    'https://cals.cornell.edu/field-crops/corn/diseases-of-corn/northern-corn-leaf-blight',
    '2026-08-25'
);


-- ============================================================
-- MAIZE COMMON RUST
-- ============================================================

INSERT OR IGNORE INTO health_problems (
    health_problem_id,
    plant_id,
    name,
    type,
    description
)
VALUES (
    'HP_MAIZE_COMMON_RUST',
    'PLANT_MAIZE',
    'Maize Common Rust',
    'fungal',
    'A fungal disease of maize caused by Puccinia sorghi. It produces characteristic rust-coloured pustules on above-ground plant tissues, especially leaves.'
);


INSERT OR IGNORE INTO species (
    species_id,
    plant_id,
    scientific_name,
    common_name
)
VALUES (
    'SP_MAIZE_ZEA_MAYS',
    'PLANT_MAIZE',
    'Zea mays',
    'Maize'
);


INSERT OR IGNORE INTO pathogens (
    pathogen_id,
    health_problem_id,
    scientific_name,
    type,
    role
)
VALUES (
    'PATH_MAIZE_COMMON_RUST_01',
    'HP_MAIZE_COMMON_RUST',
    'Puccinia sorghi',
    'fungus',
    'Causal pathogen of maize common rust.'
);


INSERT OR IGNORE INTO symptoms (
    symptom_id,
    health_problem_id,
    category,
    description
)
VALUES
(
    'SYM_MAIZE_COMMON_RUST_01',
    'HP_MAIZE_COMMON_RUST',
    'early',
    'Small flecks may appear on maize leaves.'
),
(
    'SYM_MAIZE_COMMON_RUST_02',
    'HP_MAIZE_COMMON_RUST',
    'pustules',
    'Circular to elongated brown, cinnamon-brown or rust-coloured pustules develop on leaf surfaces.'
),
(
    'SYM_MAIZE_COMMON_RUST_03',
    'HP_MAIZE_COMMON_RUST',
    'mature',
    'Pustules become darker as fungal spores mature.'
),
(
    'SYM_MAIZE_COMMON_RUST_04',
    'HP_MAIZE_COMMON_RUST',
    'severe',
    'Severe infection may cause leaf yellowing and premature death.'
);


INSERT OR IGNORE INTO transmission (
    transmission_id,
    health_problem_id,
    method,
    description
)
VALUES
(
    'TRANS_MAIZE_COMMON_RUST_01',
    'HP_MAIZE_COMMON_RUST',
    'wind',
    'Windborne spores can spread the pathogen between plants and fields.'
),
(
    'TRANS_MAIZE_COMMON_RUST_02',
    'HP_MAIZE_COMMON_RUST',
    'airborne_spores',
    'Urediniospores can be carried through the air and initiate new infections.'
);


INSERT OR IGNORE INTO conditions (
    condition_id,
    health_problem_id,
    factor,
    value,
    description
)
VALUES
(
    'COND_MAIZE_COMMON_RUST_01',
    'HP_MAIZE_COMMON_RUST',
    'temperature',
    'cool',
    'Cool temperatures favour common rust development.'
),
(
    'COND_MAIZE_COMMON_RUST_02',
    'HP_MAIZE_COMMON_RUST',
    'humidity',
    'high',
    'High relative humidity and prolonged leaf wetness favour infection and disease development.'
);


INSERT OR IGNORE INTO management (
    management_id,
    health_problem_id,
    category,
    action
)
VALUES
(
    'MGMT_MAIZE_COMMON_RUST_01',
    'HP_MAIZE_COMMON_RUST',
    'resistance',
    'Use resistant maize hybrids where available.'
),
(
    'MGMT_MAIZE_COMMON_RUST_02',
    'HP_MAIZE_COMMON_RUST',
    'monitoring',
    'Monitor maize fields for rust-coloured pustules, especially during cool and humid conditions.'
),
(
    'MGMT_MAIZE_COMMON_RUST_03',
    'HP_MAIZE_COMMON_RUST',
    'irrigation',
    'Where irrigation is necessary, practices that reduce prolonged leaf wetness can help reduce infection risk.'
);


INSERT OR IGNORE INTO sources (
    source_id,
    health_problem_id,
    organization,
    title,
    url,
    accessed_date
)
VALUES
(
    'SRC_MAIZE_COMMON_RUST_01',
    'HP_MAIZE_COMMON_RUST',
    'Cornell University',
    'Common Rust',
    'https://cals.cornell.edu/field-crops/corn/diseases-of-corn/common-rust',
    '2026-08-25'
),
(
    'SRC_MAIZE_COMMON_RUST_02',
    'HP_MAIZE_COMMON_RUST',
    'UC Statewide Integrated Pest Management Program',
    'Common Rust - Corn',
    'https://ipm.ucanr.edu/agriculture/corn/common-rust/',
    '2026-08-25'
);


-- ============================================================
-- MAIZE GRAY LEAF SPOT
-- ============================================================

INSERT OR IGNORE INTO health_problems (
    health_problem_id,
    plant_id,
    name,
    type,
    description
)
VALUES (
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'PLANT_MAIZE',
    'Maize Gray Leaf Spot',
    'fungal',
    'A fungal disease of maize caused by Cercospora zeae-maydis. The disease produces characteristic rectangular gray lesions on leaves and can cause substantial loss of functional leaf area.'
);


INSERT OR IGNORE INTO pathogens (
    pathogen_id,
    health_problem_id,
    scientific_name,
    type,
    role
)
VALUES (
    'PATH_MAIZE_GRAY_LEAF_SPOT_01',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'Cercospora zeae-maydis',
    'fungus',
    'Causal pathogen of maize gray leaf spot.'
);


INSERT OR IGNORE INTO symptoms (
    symptom_id,
    health_problem_id,
    category,
    description
)
VALUES
(
    'SYM_MAIZE_GRAY_LEAF_SPOT_01',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'early',
    'Small brown lesions may first appear on lower maize leaves.'
),
(
    'SYM_MAIZE_GRAY_LEAF_SPOT_02',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'lesion',
    'Lesions elongate and become limited by leaf veins, producing a characteristic rectangular shape.'
),
(
    'SYM_MAIZE_GRAY_LEAF_SPOT_03',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'colour',
    'Lesions become gray or gray-brown as disease develops and sporulation occurs.'
),
(
    'SYM_MAIZE_GRAY_LEAF_SPOT_04',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'severity',
    'Lesions can coalesce and kill substantial areas of leaf tissue.'
);


INSERT OR IGNORE INTO transmission (
    transmission_id,
    health_problem_id,
    method,
    description
)
VALUES
(
    'TRANS_MAIZE_GRAY_LEAF_SPOT_01',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'airborne_spores',
    'Fungal spores can be dispersed by wind from infected maize residue to susceptible plants.'
),
(
    'TRANS_MAIZE_GRAY_LEAF_SPOT_02',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'crop_residue',
    'The pathogen can survive in infected maize crop residue and produce inoculum for new infections.'
);


INSERT OR IGNORE INTO conditions (
    condition_id,
    health_problem_id,
    factor,
    value,
    description
)
VALUES
(
    'COND_MAIZE_GRAY_LEAF_SPOT_01',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'temperature',
    'warm',
    'Warm temperatures favour gray leaf spot development.'
),
(
    'COND_MAIZE_GRAY_LEAF_SPOT_02',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'humidity',
    'high',
    'Extended periods of high humidity and leaf wetness favour disease development.'
),
(
    'COND_MAIZE_GRAY_LEAF_SPOT_03',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'cropping_pattern',
    'continuous maize',
    'Continuous maize production and reduced residue decomposition can increase disease risk.'
);


INSERT OR IGNORE INTO management (
    management_id,
    health_problem_id,
    category,
    action
)
VALUES
(
    'MGMT_MAIZE_GRAY_LEAF_SPOT_01',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'resistance',
    'Use maize hybrids with resistance or tolerance to gray leaf spot where available.'
),
(
    'MGMT_MAIZE_GRAY_LEAF_SPOT_02',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'crop_rotation',
    'Rotate maize with other crops where practical to reduce disease pressure.'
),
(
    'MGMT_MAIZE_GRAY_LEAF_SPOT_03',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'residue_management',
    'Use appropriate tillage or residue-management practices to reduce infected residue and inoculum.'
),
(
    'MGMT_MAIZE_GRAY_LEAF_SPOT_04',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'monitoring',
    'Monitor lower leaves and the crop canopy for developing rectangular gray lesions.'
);


INSERT OR IGNORE INTO sources (
    source_id,
    health_problem_id,
    organization,
    title,
    url,
    accessed_date
)
VALUES
(
    'SRC_MAIZE_GRAY_LEAF_SPOT_01',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'University of Delaware Cooperative Extension',
    'Gray Leaf Spot',
    'https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/gray-leaf-spot/',
    '2026-08-25'
),
(
    'SRC_MAIZE_GRAY_LEAF_SPOT_02',
    'HP_MAIZE_GRAY_LEAF_SPOT',
    'Cornell University',
    'Gray Leaf Spot',
    'https://cals.cornell.edu/field-crops/corn/diseases-of-corn/gray-leaf-spot',
    '2026-08-25'
);


-- ============================================================
-- END OF CNN-SUPPORTED MAIZE DISEASES
-- ============================================================