-- ============================================================
-- CORN PATHOLOGY AI
-- PLANT HEALTH KNOWLEDGE BASE
-- SEED DATA
-- ============================================================

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;


-- ============================================================
-- 1. PLANTS
-- ============================================================

INSERT INTO plants (
    plant_id,
    common_name,
    genus,
    family
)
VALUES
(
    'PLANT_MAIZE',
    'Maize',
    'Zea',
    'Poaceae'
),
(
    'PLANT_TEA',
    'Tea',
    'Camellia',
    'Theaceae'
),
(
    'PLANT_COFFEE',
    'Coffee',
    'Coffea',
    'Rubiaceae'
),
(
    'PLANT_POTATO',
    'Potato',
    'Solanum',
    'Solanaceae'
);


-- ============================================================
-- 2. SPECIES
-- ============================================================

INSERT INTO species (
    species_id,
    plant_id,
    scientific_name,
    common_name
)
VALUES
(
    'SPECIES_MAIZE',
    'PLANT_MAIZE',
    'Zea mays',
    'Maize'
),
(
    'SPECIES_TEA',
    'PLANT_TEA',
    'Camellia sinensis',
    'Tea'
),
(
    'SPECIES_COFFEE_ARABICA',
    'PLANT_COFFEE',
    'Coffea arabica',
    'Arabica coffee'
),
(
    'SPECIES_COFFEE_CANEphora',
    'PLANT_COFFEE',
    'Coffea canephora',
    'Robusta coffee'
),
(
    'SPECIES_POTATO',
    'PLANT_POTATO',
    'Solanum tuberosum',
    'Potato'
);


-- ============================================================
-- 3. HEALTH PROBLEMS
-- ============================================================

INSERT INTO health_problems (
    health_problem_id,
    plant_id,
    name,
    type,
    description
)
VALUES
(
    'HP_MAIZE_MLN',
    'PLANT_MAIZE',
    'Maize Lethal Necrosis',
    'viral',
    'A serious viral disease of maize associated with co-infection by maize chlorotic mottle virus and a virus from the Potyviridae family.'
),
(
    'HP_TEA_BLISTER_BLIGHT',
    'PLANT_TEA',
    'Tea Blister Blight',
    'fungal',
    'A serious foliar disease of tea caused by the obligate biotrophic fungus Exobasidium vexans, mainly affecting young succulent leaves and shoots.'
),
(
    'HP_COFFEE_BERRY_DISEASE',
    'PLANT_COFFEE',
    'Coffee Berry Disease',
    'fungal',
    'A fungal disease of Arabica coffee caused by Colletotrichum kahawae, characterized by dark sunken lesions and progressive rotting of coffee berries.'
),
(
    'HP_POTATO_BACTERIAL_WILT',
    'PLANT_POTATO',
    'Potato Bacterial Wilt',
    'bacterial',
    'A serious soil-borne bacterial disease of potato caused by Ralstonia solanacearum and associated with wilting, yellowing and tuber symptoms.'
);


-- ============================================================
-- 4. PATHOGENS
-- ============================================================

-- ----------------------------
-- Maize Lethal Necrosis
-- ----------------------------

INSERT INTO pathogens (
    pathogen_id,
    health_problem_id,
    scientific_name,
    type,
    role
)
VALUES
(
    'PATHOGEN_MCMV',
    'HP_MAIZE_MLN',
    'Maize chlorotic mottle virus',
    'virus',
    'Co-infecting virus associated with Maize Lethal Necrosis'
),
(
    'PATHOGEN_SCMV',
    'HP_MAIZE_MLN',
    'Sugarcane mosaic virus',
    'virus',
    'Potyvirus that can co-infect maize with MCMV and contribute to MLN'
),
(
    'PATHOGEN_MDMV',
    'HP_MAIZE_MLN',
    'Maize dwarf mosaic virus',
    'virus',
    'Potyvirus that can occur as the cereal-virus component of MLN'
);


-- ----------------------------
-- Tea Blister Blight
-- ----------------------------

INSERT INTO pathogens (
    pathogen_id,
    health_problem_id,
    scientific_name,
    type,
    role
)
VALUES
(
    'PATHOGEN_EXOBASIDIUM_VEXANS',
    'HP_TEA_BLISTER_BLIGHT',
    'Exobasidium vexans',
    'fungus',
    'Causal organism of tea blister blight'
);


-- ----------------------------
-- Coffee Berry Disease
-- ----------------------------

INSERT INTO pathogens (
    pathogen_id,
    health_problem_id,
    scientific_name,
    type,
    role
)
VALUES
(
    'PATHOGEN_COLLETOTRICHUM_KAHAWAE',
    'HP_COFFEE_BERRY_DISEASE',
    'Colletotrichum kahawae',
    'fungus',
    'Causal organism of coffee berry disease'
);


-- ----------------------------
-- Potato Bacterial Wilt
-- ----------------------------

INSERT INTO pathogens (
    pathogen_id,
    health_problem_id,
    scientific_name,
    type,
    role
)
VALUES
(
    'PATHOGEN_RALSTONIA_SOLANACEARUM',
    'HP_POTATO_BACTERIAL_WILT',
    'Ralstonia solanacearum',
    'bacterium',
    'Soil-borne bacterium responsible for bacterial wilt of potato'
);


-- ============================================================
-- 5. SYMPTOMS
-- ============================================================

-- ----------------------------
-- Maize Lethal Necrosis
-- ----------------------------

INSERT INTO symptoms (
    symptom_id,
    health_problem_id,
    category,
    description
)
VALUES
(
    'SYM_MLN_001',
    'HP_MAIZE_MLN',
    'early',
    'Long yellow stripes appear on maize leaves.'
),
(
    'SYM_MLN_002',
    'HP_MAIZE_MLN',
    'progression',
    'Leaves become yellow and dry from the outer edges toward the midrib.'
),
(
    'SYM_MLN_003',
    'HP_MAIZE_MLN',
    'plant',
    'Plants may become dwarfed and show premature aging.'
),
(
    'SYM_MLN_004',
    'HP_MAIZE_MLN',
    'advanced',
    'The entire plant may dry out and die.'
),
(
    'SYM_MLN_005',
    'HP_MAIZE_MLN',
    'reproductive',
    'Late-infected plants may fail to tassel and produce poorly filled cobs.'
);


-- ----------------------------
-- Tea Blister Blight
-- ----------------------------

INSERT INTO symptoms (
    symptom_id,
    health_problem_id,
    category,
    description
)
VALUES
(
    'SYM_TEA_001',
    'HP_TEA_BLISTER_BLIGHT',
    'early',
    'Small pinhole-sized spots appear on young leaves.'
),
(
    'SYM_TEA_002',
    'HP_TEA_BLISTER_BLIGHT',
    'leaf',
    'Spots enlarge and become transparent, light brown or pinkish translucent areas.'
),
(
    'SYM_TEA_003',
    'HP_TEA_BLISTER_BLIGHT',
    'leaf',
    'White and velvety blister-like lesions develop on the lower leaf surface.'
),
(
    'SYM_TEA_004',
    'HP_TEA_BLISTER_BLIGHT',
    'advanced',
    'Blister lesions become brown and infected leaf tissue may become necrotic.'
),
(
    'SYM_TEA_005',
    'HP_TEA_BLISTER_BLIGHT',
    'shoot',
    'Young infected stems may become bent, distorted, break off or die.'
);


-- ----------------------------
-- Coffee Berry Disease
-- ----------------------------

INSERT INTO symptoms (
    symptom_id,
    health_problem_id,
    category,
    description
)
VALUES
(
    'SYM_COFFEE_001',
    'HP_COFFEE_BERRY_DISEASE',
    'berry',
    'Small water-soaked lesions appear on young expanding coffee berries.'
),
(
    'SYM_COFFEE_002',
    'HP_COFFEE_BERRY_DISEASE',
    'berry',
    'Lesions rapidly become dark, sunken and progressively enlarge.'
),
(
    'SYM_COFFEE_003',
    'HP_COFFEE_BERRY_DISEASE',
    'berry',
    'The affected berry may eventually rot completely.'
),
(
    'SYM_COFFEE_004',
    'HP_COFFEE_BERRY_DISEASE',
    'sporulation',
    'Pink spore masses may become visible on lesions under humid conditions.'
),
(
    'SYM_COFFEE_005',
    'HP_COFFEE_BERRY_DISEASE',
    'fruit_drop',
    'Affected berries may drop from the branch early.'
),
(
    'SYM_COFFEE_006',
    'HP_COFFEE_BERRY_DISEASE',
    'flower',
    'Under very wet conditions, flowers may develop brown lesions on the petals.'
);


-- ----------------------------
-- Potato Bacterial Wilt
-- ----------------------------

INSERT INTO symptoms (
    symptom_id,
    health_problem_id,
    category,
    description
)
VALUES
(
    'SYM_POTATO_001',
    'HP_POTATO_BACTERIAL_WILT',
    'plant',
    'Wilting may begin with drooping of the tips of lower leaves.'
),
(
    'SYM_POTATO_002',
    'HP_POTATO_BACTERIAL_WILT',
    'leaf',
    'Leaves may yellow and roll upward and inward from the margins.'
),
(
    'SYM_POTATO_003',
    'HP_POTATO_BACTERIAL_WILT',
    'plant',
    'Plants may become stunted and experience die-back.'
),
(
    'SYM_POTATO_004',
    'HP_POTATO_BACTERIAL_WILT',
    'tuber',
    'Brownish-grey areas may appear on the outside of infected tubers, especially near the stolon attachment.'
),
(
    'SYM_POTATO_005',
    'HP_POTATO_BACTERIAL_WILT',
    'tuber',
    'Bacterial ooze may emerge through the eyes of infected tubers.'
),
(
    'SYM_POTATO_006',
    'HP_POTATO_BACTERIAL_WILT',
    'vascular',
    'Cut infected tubers may show browning of vascular tissue and bacterial discharge.'
);


-- ============================================================
-- 6. TRANSMISSION
-- ============================================================

-- ----------------------------
-- Maize Lethal Necrosis
-- ----------------------------

INSERT INTO transmission (
    transmission_id,
    health_problem_id,
    method,
    description
)
VALUES
(
    'TRANS_MLN_001',
    'HP_MAIZE_MLN',
    'insect_vectors',
    'The disease-causing viruses can be transmitted by insect vectors including thrips, aphids, leafhoppers and beetles.'
),
(
    'TRANS_MLN_002',
    'HP_MAIZE_MLN',
    'seed',
    'Seed can contribute to transmission of the viruses, particularly MCMV.'
);


-- ----------------------------
-- Tea Blister Blight
-- ----------------------------

INSERT INTO transmission (
    transmission_id,
    health_problem_id,
    method,
    description
)
VALUES
(
    'TRANS_TEA_001',
    'HP_TEA_BLISTER_BLIGHT',
    'wind',
    'Basidiospores are readily dispersed by wind.'
),
(
    'TRANS_TEA_002',
    'HP_TEA_BLISTER_BLIGHT',
    'water',
    'Moisture on susceptible leaves facilitates spore germination and infection.'
);


-- ----------------------------
-- Coffee Berry Disease
-- ----------------------------

INSERT INTO transmission (
    transmission_id,
    health_problem_id,
    method,
    description
)
VALUES
(
    'TRANS_COFFEE_001',
    'HP_COFFEE_BERRY_DISEASE',
    'rain_splash',
    'Spores are dispersed within the coffee tree by rain splash.'
),
(
    'TRANS_COFFEE_002',
    'HP_COFFEE_BERRY_DISEASE',
    'human_activity',
    'The disease can spread between trees and farms through coffee pickers.'
),
(
    'TRANS_COFFEE_003',
    'HP_COFFEE_BERRY_DISEASE',
    'plant_material',
    'Infected seedlings can contribute to disease spread.'
),
(
    'TRANS_COFFEE_004',
    'HP_COFFEE_BERRY_DISEASE',
    'animals',
    'Birds may contribute to spread between plants or farms.'
);


-- ----------------------------
-- Potato Bacterial Wilt
-- ----------------------------

INSERT INTO transmission (
    transmission_id,
    health_problem_id,
    method,
    description
)
VALUES
(
    'TRANS_POTATO_001',
    'HP_POTATO_BACTERIAL_WILT',
    'water',
    'Irrigation water and flood waters can spread the bacterium.'
),
(
    'TRANS_POTATO_002',
    'HP_POTATO_BACTERIAL_WILT',
    'soil',
    'Contaminated soil can spread the disease.'
),
(
    'TRANS_POTATO_003',
    'HP_POTATO_BACTERIAL_WILT',
    'equipment',
    'Contaminated farm equipment, seed cutters, bags and containers can spread the bacterium.'
),
(
    'TRANS_POTATO_004',
    'HP_POTATO_BACTERIAL_WILT',
    'seed',
    'Infected seed potatoes are an important method of dissemination.'
);


-- ============================================================
-- 7. CONDITIONS
-- ============================================================

-- ----------------------------
-- Maize Lethal Necrosis
-- ----------------------------

INSERT INTO conditions (
    condition_id,
    health_problem_id,
    factor,
    value,
    description
)
VALUES
(
    'COND_MLN_001',
    'HP_MAIZE_MLN',
    'cropping_pattern',
    'continuous maize',
    'Continuous maize production can favor disease persistence and spread.'
),
(
    'COND_MLN_002',
    'HP_MAIZE_MLN',
    'vector_movement',
    'wind',
    'Insect vectors can be carried by wind over long distances.'
);


-- ----------------------------
-- Tea Blister Blight
-- ----------------------------

INSERT INTO conditions (
    condition_id,
    health_problem_id,
    factor,
    value,
    description
)
VALUES
(
    'COND_TEA_001',
    'HP_TEA_BLISTER_BLIGHT',
    'relative_humidity',
    '>80%',
    'High relative humidity favors infection and disease development.'
),
(
    'COND_TEA_002',
    'HP_TEA_BLISTER_BLIGHT',
    'temperature',
    '20-25 C',
    'The source reports approximately 20-25 C as an optimal growth temperature range.'
),
(
    'COND_TEA_003',
    'HP_TEA_BLISTER_BLIGHT',
    'leaf_wetness',
    'prolonged moisture',
    'Availability of water on the leaf surface facilitates infection.'
);


-- ----------------------------
-- Coffee Berry Disease
-- ----------------------------

INSERT INTO conditions (
    condition_id,
    health_problem_id,
    factor,
    value,
    description
)
VALUES
(
    'COND_COFFEE_001',
    'HP_COFFEE_BERRY_DISEASE',
    'humidity',
    'wet conditions',
    'Wet conditions favor disease development.'
),
(
    'COND_COFFEE_002',
    'HP_COFFEE_BERRY_DISEASE',
    'temperature',
    '15-27.7 C',
    'Disease development is favored by temperatures between approximately 15 and 27.7 C.'
);


-- ----------------------------
-- Potato Bacterial Wilt
-- ----------------------------

INSERT INTO conditions (
    condition_id,
    health_problem_id,
    factor,
    value,
    description
)
VALUES
(
    'COND_POTATO_001',
    'HP_POTATO_BACTERIAL_WILT',
    'temperature',
    '25-37 C',
    'Bacterial wilt is generally favored by temperatures between approximately 25 and 37 C.'
),
(
    'COND_POTATO_002',
    'HP_POTATO_BACTERIAL_WILT',
    'soil_moisture',
    'wet soil',
    'Wet soil favors infection.'
),
(
    'COND_POTATO_003',
    'HP_POTATO_BACTERIAL_WILT',
    'soil_temperature',
    'below 15 C',
    'The disease generally causes fewer problems where mean soil temperature is below 15 C.'
);


-- ============================================================
-- 8. MANAGEMENT
-- ============================================================

-- ----------------------------
-- Maize Lethal Necrosis
-- ----------------------------

INSERT INTO management (
    management_id,
    health_problem_id,
    category,
    action
)
VALUES
(
    'MGMT_MLN_001',
    'HP_MAIZE_MLN',
    'crop_rotation',
    'Avoid continuous maize production and rotate with other crops.'
),
(
    'MGMT_MLN_002',
    'HP_MAIZE_MLN',
    'crop_diversification',
    'Diversify the farm enterprise to interrupt the disease cycle.'
),
(
    'MGMT_MLN_003',
    'HP_MAIZE_MLN',
    'field_selection',
    'Avoid planting a new maize crop close to an infected field.'
),
(
    'MGMT_MLN_004',
    'HP_MAIZE_MLN',
    'field_hygiene',
    'Remove diseased maize plants promptly.'
),
(
    'MGMT_MLN_005',
    'HP_MAIZE_MLN',
    'variety_selection',
    'Use maize varieties with resistance to MLN where suitable resistant varieties are available.'
);


-- ----------------------------
-- Tea Blister Blight
-- ----------------------------

INSERT INTO management (
    management_id,
    health_problem_id,
    category,
    action
)
VALUES
(
    'MGMT_TEA_001',
    'HP_TEA_BLISTER_BLIGHT',
    'pruning',
    'Remove affected leaves and shoots by pruning and destroy the affected material.'
),
(
    'MGMT_TEA_002',
    'HP_TEA_BLISTER_BLIGHT',
    'fungicide',
    'Use recommended copper-based fungicide treatments according to local agricultural guidance.'
);


-- ----------------------------
-- Coffee Berry Disease
-- ----------------------------

INSERT INTO management (
    management_id,
    health_problem_id,
    category,
    action
)
VALUES
(
    'MGMT_COFFEE_001',
    'HP_COFFEE_BERRY_DISEASE',
    'variety_selection',
    'Plant resistant varieties where coffee berry disease is endemic.'
),
(
    'MGMT_COFFEE_002',
    'HP_COFFEE_BERRY_DISEASE',
    'pruning',
    'Prune coffee trees after harvest.'
),
(
    'MGMT_COFFEE_003',
    'HP_COFFEE_BERRY_DISEASE',
    'sanitation',
    'Strip off diseased berries.'
),
(
    'MGMT_COFFEE_004',
    'HP_COFFEE_BERRY_DISEASE',
    'canopy_management',
    'Remove old stems and thin out branches.'
),
(
    'MGMT_COFFEE_005',
    'HP_COFFEE_BERRY_DISEASE',
    'fungicide',
    'Apply copper fungicide in a timely manner according to local recommendations.'
);


-- ----------------------------
-- Potato Bacterial Wilt
-- ----------------------------

INSERT INTO management (
    management_id,
    health_problem_id,
    category,
    action
)
VALUES
(
    'MGMT_POTATO_001',
    'HP_POTATO_BACTERIAL_WILT',
    'crop_rotation',
    'Rotate with pastures, cereals and other non-solanaceous crops for more than five years where appropriate.'
),
(
    'MGMT_POTATO_002',
    'HP_POTATO_BACTERIAL_WILT',
    'seed',
    'Use certified seed from reliable sources.'
),
(
    'MGMT_POTATO_003',
    'HP_POTATO_BACTERIAL_WILT',
    'field_selection',
    'Plant potatoes in areas where bacterial wilt has not previously occurred.'
),
(
    'MGMT_POTATO_004',
    'HP_POTATO_BACTERIAL_WILT',
    'weed_control',
    'Control weed hosts such as nightshade and thorn apple.'
),
(
    'MGMT_POTATO_005',
    'HP_POTATO_BACTERIAL_WILT',
    'water_management',
    'Prevent contaminated irrigation water from moving freely across potato production areas.'
),
(
    'MGMT_POTATO_006',
    'HP_POTATO_BACTERIAL_WILT',
    'sanitation',
    'Remove and destroy diseased plants, tubers and immediate neighbours.'
),
(
    'MGMT_POTATO_007',
    'HP_POTATO_BACTERIAL_WILT',
    'equipment_hygiene',
    'Clean and disinfect machinery, bags, bins and other equipment that may carry contaminated soil.'
),
(
    'MGMT_POTATO_008',
    'HP_POTATO_BACTERIAL_WILT',
    'seed_hygiene',
    'Do not retain produce from a diseased crop as seed.'
);


-- ============================================================
-- 9. SOURCES
-- ============================================================

-- ----------------------------
-- Maize
-- ----------------------------

INSERT INTO sources (
    source_id,
    health_problem_id,
    organization,
    title,
    url,
    accessed_date
)
VALUES
(
    'SRC_MLN_001',
    'HP_MAIZE_MLN',
    'Plantwise Plus',
    'Prevention and detection of Maize Lethal Necrosis Disease',
    'https://plantwiseplusknowledgebank.org/doi/full/10.1079/pwkb.20157800329',
    '2026-08-25'
),
(
    'SRC_MLN_002',
    'HP_MAIZE_MLN',
    'Infonet Biovision',
    'Maize lethal necrosis (MLN)',
    'https://infonet-biovision.org/PlantHealth/MinorPests/maize-lethal-necrosis-mln',
    '2026-08-25'
);


-- ----------------------------
-- Tea
-- ----------------------------

INSERT INTO sources (
    source_id,
    health_problem_id,
    organization,
    title,
    url,
    accessed_date
)
VALUES
(
    'SRC_TEA_001',
    'HP_TEA_BLISTER_BLIGHT',
    'Tamil Nadu Agricultural University',
    'Tea - Blister blight',
    'https://agritech.tnau.ac.in/crop_protection/tea_diseases_3.html',
    '2026-08-25'
),
(
    'SRC_TEA_002',
    'HP_TEA_BLISTER_BLIGHT',
    'IntechOpen',
    'Blister Blight Disease of Tea: An Enigma',
    'https://www.intechopen.com/chapters/74600',
    '2026-08-25'
);


-- ----------------------------
-- Coffee
-- ----------------------------

INSERT INTO sources (
    source_id,
    health_problem_id,
    organization,
    title,
    url,
    accessed_date
)
VALUES
(
    'SRC_COFFEE_001',
    'HP_COFFEE_BERRY_DISEASE',
    'Greenlife Crop Protection Africa',
    'Understanding Coffee Berry Disease',
    'https://www.greenlife.co.ke/understanding-coffee-berry-disease/',
    '2026-08-25'
),
(
    'SRC_COFFEE_002',
    'HP_COFFEE_BERRY_DISEASE',
    'Infonet Biovision',
    'Coffee berry disease',
    'https://infonet-biovision.org/PlantHealth/MinorPests/coffee-berry-disease',
    '2026-08-25'
);


-- ----------------------------
-- Potato
-- ----------------------------

INSERT INTO sources (
    source_id,
    health_problem_id,
    organization,
    title,
    url,
    accessed_date
)
VALUES
(
    'SRC_POTATO_001',
    'HP_POTATO_BACTERIAL_WILT',
    'National Potato Council of Kenya',
    'Managing Potato Diseases: Common Issues and Solutions',
    'https://npck.org/managing-potato-diseases-common-issues-and-solutions/',
    '2026-08-25'
),
(
    'SRC_POTATO_002',
    'HP_POTATO_BACTERIAL_WILT',
    'Agriculture Victoria',
    'Bacterial wilt of potatoes',
    'https://agriculture.vic.gov.au/biosecurity/plant-diseases/vegetable-diseases/bacterial-wilt-of-potatoes',
    '2026-08-25'
);


-- ============================================================
-- COMPLETE TRANSACTION
-- ============================================================

COMMIT;

-- ============================================================
-- SEED DATA COMPLETE
-- ============================================================