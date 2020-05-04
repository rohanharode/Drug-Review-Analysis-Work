# Drug matcher
import pandas as pd
import pathlib

from ETL.Data_Preprocessing.data_manipulation import set_age_range, webmd_rating_average



def match_and_replace(df, filetype, word_list):
    if filetype == 'webmd' or filetype == 'druglib':
        df['Condition'] = df.Condition.astype(str)
        df['Condition'] = df['Condition'].str.strip()
    elif filetype == 'drugs_com':
        df['condition'] = df.condition.astype(str)
        df['condition'] = df['condition'].str.strip()

    for i in range(0, len(word_list)):
        c, d = str(word_list[i][0]), str(word_list[i][1])
        print('Changing: ', c)
        print('With: ', d)
        if filetype == 'webmd' or filetype == 'druglib':
            df = df.replace({'Condition': c}, d)
        elif filetype == 'drugs_com':
            df = df.replace({'condition': c}, d)
    print(f'Total {len(word_list)} conditions filtered')
    return df

def word_filtering(df, filetype='webmd'):
    word_replace_webmd = [ \
        ['Abnormally Long or Heavy Periods', 'Menorrhagia'], \
        ['A Severe Skin Infection - Ecthyma', 'Skin Infection'], \
        ['Abnormal Bleeding from the Uterus', 'Abnormal Uterine Bleeding'], \
        ['Acute Repetitive Seizures', 'Seizures'], \
        ['Abnormal Heart Rhythm', 'Arrhythmia'], \
        ['Acute Pain', 'Pain'], \
        ['Acute Infection of the Nose, Throat or Sinus', 'Sinus Symptoms'], \
        ['Acute Maxillary Sinus S. Pneumoniae Bacteria Infection', 'Sinusitis'], \
        ['Acute Maxillary Sinus H. Influenzae Bacteria Infection', 'Sinusitis'], \
        ['Acute Inflammation of the Maxillary Sinus', 'Sinusitis'], \
        ['Acute Thromboembolic Stroke', 'Thromboembolic Stroke Prophylaxis'], \
        ['Advanced Form of Prostate Cancer', 'Prostate Cancer'], \
        ['Additional Medications to Treat Depression', 'Depression'], \
        ['Additional Medication for Tonic-Clonic Epilepsy', 'Epilepsy'], \
        ['Additional Medication for Myoclonic Epilepsy', 'Epilepsy'], \
        ['Additional Medication to Treat Partial Seizures', 'Seizures'], \
        ['Additional Treatment for Thyroid Cancer', 'Thyroid Cancer'], \
        ['Advanced Breast Cancer Progression Post - Antiestrogen Therapy', 'Breast Cancer'], \
        ['Adjunct Treatment of Obesity in a Comprehensive Weight Reduction Regimen', 'Obesity'], \
        ['Agitation associated with Bipolar Mania', 'Agitation'], \
        ['Agitation associated with Schizophrenia', 'Agitation'], \
        ['Allergic Reaction caused by a Drug', 'Allergic Reactions'], \
        ['Anxious', 'Anxiety'], \
        ['Anxiousness associated with Depression', 'Anxiety'], \
        ['Anxiety without Psychosis', 'Anxiety'], \
        ['Anemia from Inadequate Iron', 'Iron Deficiency Anemia'], \
        ['Anemia from Chemotherapy', 'Anemia'], \
        ['Arthritis in Lyme Disease', 'arthritis'],\
        ['Arthritis Pain','Arthritis'],\
        ['Aspiration Pneumonia Prevention', 'Aspiration Pneumonia'], \
        ['Attention Deficit Disorder with Hyperactivity', 'ADHD'], \
        ['Asthma Prevention', 'Asthma'], \
        ['ALK Positive Non-Small Cell Lung Cancer', 'Non-Small Cell Lung Cancer'], \
        ['Backache', 'Back Pain'], \
        ['Bacterial Skin Infection - Yaws', 'Bacterial Skin Infection'], \
        ['Bacterial Pneumonia caused by Staphylococcus Aureus', 'Bacterial Pneumonia'], \
        ['Bacterial Pneumonia caused by Streptococcus pneumoniae', 'Bacterial Pneumonia'], \
        ['Bacterial Pneumonia caused by Haemophilus Influenzae', 'Bacterial Pneumonia'], \
        ['Bacterial Pneumonia caused by Klebsiella', 'Bacterial Pneumonia'], \
        ['Bacterial Pneumonia caused by Staphylococcus', 'Bacterial Pneumonia'], \
        ['Bacterial Pneumonia caused by Streptococcus', 'Bacterial Pneumonia'], \
        ['Blood Clot in Lung', 'Pulmonary Embolism'], \
        ['Bladder Infection caused by E. Coli', 'Bladder Infection'], \
        ['Bladder Infection caused by Enterobacter', 'Bladder Infection'], \
        ['Bladder Infection caused by Staphylococcus', 'Bladder Infection'], \
        ['Blood Clot Prevention Following Percutaneous Coronary Intervention',
         'Percutaneous Coronary Intervention'], \
        ['Blood Clot with Heparin-Induced Thrombocytopenia during Percutaneous Coronary Intervention',
         'Percutaneous Coronary Intervention'], \
        ['Blood Clot in the Brain', 'Thromboembolic Stroke Prophylaxis'], \
        ['Bipolar Disorder in Remission', 'Bipolar Disorder'], \
        ['Bipolar I Disorder with Most Recent Episode Mixed', 'Bipolar Disorder'], \
        ['Bronchitis caused by the Bacteria Haemophilus Influenzae', 'Bronchitis'], \
        ['Bronchitis caused by Haemophilus Parainfluenzae Bacteria', 'Bronchitis'], \
        ['Bronchitis caused by the Bacteria Streptococcus Pneumoniae', 'Bronchitis'], \
        ['Bronchitis caused by Haemophilus Parainfluenzae Bacteria', 'Bronchitis'], \
        ['Bronchitis caused by the Bacteria Staphylococcus Aureus', 'Bronchitis'], \
        ['Bronchitis caused by the Bacteria Moraxella Catarrhalis', 'Bronchitis'], \
        ['Bone Infection caused by Bacteroides', 'Bone Infection'], \
        ['Bone Infection caused by Enterobacter', 'Bone Infection'], \
        ['Breast Cancer that has Spread to Another Part of the Body', 'Breast Cancer'], \
        ['Chronic Bronchitis caused by Haemophilus Influenzae', 'Bronchitis'], \
        ['Chronic Bronchitis caused by Streptococcus Pneumoniae', 'Bronchitis'], \
        ['chronic lymphoid leukemia', 'chronic lymphocytic leukemia'],\
        ['Chronic Obstructive Asthma', 'asthma'],\
        ['Chronic Stable Angina', 'angina'],\
        ['Cancer of the Prostate Gland', 'Prostate Cancer'], \
        ['Cancer of the Pancreas', 'Pancreatic Cancer'], \
        ['Cancer of the Ovary', 'Ovarian Cancer'], \
        ['Cancer of Prostate that has Spread to Other Part of Body', 'Prostate Cancer'], \
        ['Candida Fungus Infection of Mouth, Skin, Nails or Vagina', 'Systemic Candidiasis'], \
        ['Candida Species Yeast Infection of Abdominal Cavity Lining', 'Systemic Candidiasis'], \
        ['Candidiasis Yeast Infection that Spreads Throughout Body', 'Systemic Candidiasis'], \
        ['Chronic Trouble Sleeping', 'Insomnia'], \
        ['Chronic Pain with Narcotic Drug Tolerance', 'Chronic Pain'], \
        ['Chronic Heart Failure', 'Heart Failure'], \
        ['Chronic Post Traumatic Stress Disorder with Trauma-related Nightmares', 'Post Traumatic Stress Disorder'], \
        ['Chronic Pulmonary Hypertension After Pulmonary Embolism', 'Pulmonary Hypertension'], \
        ['Complicated Skin Infection due to Staphyloccus Aureus Bacteria', 'Bacterial Skin Infection'], \
        ['Complicated Skin Infection', 'skin infection'],\
        ['Complicated Urinary Tract Infection caused by E. Coli', 'Bacterial Urinary Tract Infection'], \
        ['Convulsive Seizures', 'Seizures'], \
        ['Conjunctivitis, Bacterial', 'Conjunctivitis'], \
        ['Condition in which Stomach Acid is Pushed Into the Esophagus', 'Erosive Esophagitis'], \
        ['Condition in which Stomach Acid is Pushed Into the Esophagus', 'Erosive Esophagitis'], \
        ['Colon and Rectal Cancer that has Spread to Another Area', 'Colorectal Cancer'], \
        ['Crohn\'s Disease Maintenance of Remission', 'Crohn\'s Disease'], \
        ['Cluster Headache', 'Cluster Headaches'], \
        ['Diabetic Complication causing Injury to some Body Nerves', 'Diabetic Peripheral Neuropathy'], \
        ['Diarrhea caused by Chemotherapy', 'Diarrhea'], \
        ['Diarrhea Predominant Irritable Colon', 'Irritable Bowel Syndrome'], \
        ['Deficiency of the Vitamin Niacin', 'Niacin Deficiency'], \
        ['Difficulty Falling Asleep', 'Insomnia'], \
        ['Diabetes Insipidus with Kidney Complications', 'Diabetes Insipidus'], \
        ['Deep Vein Thrombosis Prevention', 'Deep Vein Thrombosis'], \
        ['Deep Vein Thrombosis Prevention in Hip Surgery', 'Deep Vein Thrombosis'], \
        ['Deep Vein Thrombosis Prevention in Knee Replacement', 'Deep Vein Thrombosis'], \
        ['Deep Vein Thrombosis Prophylaxis after Hip Replacement Surgery', 'Deep Vein Thrombosis'], \
        ['Deep Vein Thrombosis, First Event', 'Deep Vein Thrombosis'], \
        ['Disease of Ovaries with Cysts', 'Ovarian Cysts'], \
        ['Disorder characterized by Stiff, Tender & Painful Muscles', 'Stiff Person Syndrome'], \
        ['Disease of the Nails caused by Candida Species Fungus', 'Onychomycosis, Fingernail'], \
        ['Disease of the Nails caused by Trichophyton Fungus', 'Onychomycosis, Fingernail'], \
        ['Depression following Delivery of Baby', 'Postpartum Depression'], \
        ['Dry Mouth Secondary to Sjogren\'s Syndrome', 'Dry Mouth'], \
        ['Kidney Disease from Diabetes', 'Diabetic Kidney Disease'], \
        ['Drying and Inflammation of Cornea and Conjunctiva of Eyes', 'Conjunctivitis'], \
        ['Eczema Skin Condition Resisting Treatment', 'Eczema'], \
        ['Enlarged Prostate with Urination Problems', 'Prostate Cancer'], \
        ['Enlarged Prostate', 'Prostate Cancer'], \
        ['Enlarged Prostate with Urination Problems', 'Prostate Cancer'], \
        ['Epilepsy of the Lennox Gastaut Syndrome', 'Epilepsy'], \
        ['Epileptic Seizure', 'Seizures'], \
        ['Emptying of the Bowel', 'Constipation'], \
        ['Estrogen Receptor (ER)-Positive, HER2-Negative Postmenopausal Advanced Breast Cancer', 'Breast Cancer'], \
        ['Epidermal Growth Factor Receptor Positive Non-Small Cell Lung Cancer', 'Non-Small Cell Lung Cancer'], \
        ['Extremely High Blood Pressure', 'high blood pressure'],\
        ['Facial Nerve Pain', 'Trigeminal Neuralgia'], \
        ['Fine Wrinkling', 'Facial Wrinkles'], \
        ['Fine Wrinkling of the Face', 'Facial Wrinkles'], \
        ['Fungal Infection of the Esophagus', 'Esophageal Candidiasis'], \
        ['Fungal Infection of Toenails', 'Onychomycosis, Toenail'], \
        ['Fungal Disease of the Nails', 'Onychomycosis, Fingernail'], \
        ['Fungal Infection of the Skin with Yellow Patches', 'Cutaneous Candidiasis'], \
        ['Fungal Meningitis caused by Cryptococcus', 'Fungal Infection'], \
        ['Fatigue associated with Multiple Sclerosis', 'Fatigue'], \
        ['Glucocorticoid-Induced Osteoporosis Prevention', 'Osteoporosis'], \
        ['Heartburn', 'GERD'], \
        ['Heart Failure After a Heart Attack', 'Heart Failure'], \
        ['HER2 Positive Breast Cancer', 'Breast Cancer'], \
        ['Herpes Simplex Infection', 'herpes simplex'],\
        ['HIV', 'HIV Infection'], \
        ['Hormone Receptor Positive Breast Cancer', 'Breast Cancer'], \
        ['Hormone Receptor Positive Postmenopausal Advanced Breast Cancer', 'Breast Cancer'], \
        ['Hormone Receptor Positive Postmenopausal Early Breast Cancer', 'Breast Cancer'], \
        ['Hormone Receptor Positive, HER2 Positive Metastatic Breast Cancer', 'Breast Cancer, Metastatic'], \
        ['Hormone Receptor(HR) - Positive, HER2 - Negative Advanced Breast Cancer in Woman', 'Breast Cancer'], \
        ['Hormone Receptor Positive Postmenopausal Early Breast Cancer After Adjuvant Tamoxifen', 'Breast Cancer'], \
        ['Heterozygous Inherited High Blood Cholesterol', 'High Cholesterol, Familial Heterozygous'], \
        ['Homozygous Inherited High Blood Cholesterol', 'High Cholesterol, Familial Homozygous'], \
        ['Head Pain', 'Headache'], \
        ['Hives', 'Urticaria'], \
        ['Inability to have an Erection', 'Erectile Dysfunction'], \
        ['Inability of Body to Handle Lactose or Milk Sugar', 'Lactose Intolerance'], \
        ['Increased Pressure of Pulmonary Circulation', 'Pulmonary Hypertension'], \
        ['Incomplete or Infrequent Bowel Movements', 'Irritable Bowel Syndrome'], \
        ['Inflammation of the Esophagus with Erosion', 'Erosive Esophagitis'], \
        ['infection caused by bacteria', 'Bacterial Infection'], \
        ['Infection of Bone', 'Bone Infection'], \
        ['Infection of a Joint', 'Joint Infection'], \
        ['Infection of the Bladder', 'Bladder Infection'], \
        ['Infectious Diarrhea', 'Diarrhea'], \
        ['Infection of Urinary Tract with Complications', 'Urinary Tract Infection'], \
        ['Infection of Urinary Tract due to Pseudomonas Aeruginosa', 'Urinary Tract Infection'], \
        ['Infection of Genitals or Urinary Tract', 'Urinary Tract Infection'], \
        ['Infection of Genitals or Urinary Tract due to Enterococcus', 'Urinary Tract Infection'], \
        ['Infection of Genitals or Urinary Tract due to Proteus', 'Urinary Tract Infection'], \
        ['Infection of the Genital and Urinary Tract due to E. Coli', 'Urinary Tract Infection'], \
        ['Infection of Urinary Tract due to Providencia Species', 'Urinary Tract Infection'], \
        ['Infection of Urinary Tract due to Pseudomonas Aeruginosa', 'Urinary Tract Infection'], \
        ['Insomnia with Middle of the Night Awakening and 4 Hours Sleep Time Remaining', 'Insomnia'], \
        ['Infection of Urinary Tract due to Enterobacter Cloacae', 'Bacterial Urinary Tract Infection'], \
        ['Intraductal Breast Cancer', 'Breast Cancer'], \
        ['Influenza Prevention', 'Influenza'], \
        ['Iron Deficiency Anemia','Anemia'],\
        ['Inflammation of the External Ear Resembling Eczema', 'Eczema'], \
        ['Inflammation of the Esophagus with Erosion', 'Erosive Esophagitis'], \
        ['Joint Damage causing Pain and Loss of Function', 'Joint Pain'], \
        ['Low Estrogen After Operation to Remove Ovaries', 'Oophorectomy'], \
        ['Lack in Vitamins', 'Vitamin Deficiency'], \
        ['Lung Infection caused by Coccidioides Fungus', 'Lung Infection'], \
        ['Late Onset Asthma', 'asthma'],\
        ['Mania associated with Bipolar Disorder', 'Bipolar Disorder'], \
        ['Migraine Prevention', 'Migraine'], \
        ['Mania associated with Bipolar Disorder, Adjunct Treatment', 'Bipolar Disorder'], \
        ['Manic-Depression', 'Bipolar Disorder'], \
        ['Moderate to Severe Plaque Psoriasis', 'Plaque Psoriasis'], \
        ['Mycobacterium Avium Bacteria Infection', 'Bacterial Infection'], \
        ['Migraine Headache', 'Migraine'], \
        ['Mild to Moderate Alzheimer\'s Type Dementia', 'Alzheimer\'s Disease'], \
        ['Moderate to Severe Alzheimer\'s Type Dementia', 'Alzheimer\'s Disease'], \
        ['Mitral Valve Prolapse Syndrome', 'Mitral Valve Prolapse'], \
        ['Nerve Pain', 'Neuropathic Pain'], \
        ['Nerve Pain from Spinal Cord Injury', 'Neuropathic Pain'],
        ['Nerve Pain after Herpes', 'Neuropathic Pain'], \
        ['non-metastatic castration-resistant prostate cancer', 'Prostate Cancer'], \
        ['Nonsquamous Non-Small Cell Lung Cancer', 'non-small cell lung cancer'], \
        ['Nausea and Vomiting', 'Nausea/Vomiting'], \
        ['Nausea and Vomiting of Pregnancy', 'Nausea/Vomiting of Pregnancy'], \
        ['Non-Small Cell Lung Cancer with EGFR T790M Gene Mutation', 'Non-Small Cell Lung Cancer'], \
        ['Non-Seasonal Allergic Runny Nose','Allergic Rhinitis'],\
        ['Obstructive Pulmonary Disease', 'COPD'], \
        ['osteoporosis in postmenopausal woman at high risk for fracture', 'Osteoporosis'], \
        ['Osteoporosis caused by Glucocorticoid Drugs', 'Osteoporosis'], \
        ['Osteoporosis caused by Anti-Androgen Drugs', 'Osteoporosis'], \
        ['Osteoporosis in Male Patient', 'Osteoporosis'], \
        ['Osteoporosis in Men due to Deficient Function of Testis', 'Osteoporosis'], \
        ['Painful Periods', 'Endometriosis'], \
        ['Pink Eye from Bacterial Infection', 'Conjunctivitis'], \
        ['Pneumonia Acquired from Being Treated In a Hospital', 'Pneumonia'], \
        ['Pneumonia with High Amount of Eosinophil White Blood Cells', 'Pneumonia'], \
        ['Pneumonia caused by Acinetobacter Bacteria', 'Bacterial Pneumonia'], \
        ['Pneumonia caused by the Bacteria Bacteroides', 'Bacterial Pneumonia'], \
        ['Pneumonia caused by Bacteria', 'Bacterial Pneumonia'], \
        ['Pneumonia caused by Gram - Negative Bacteria', 'Bacterial Pneumonia'], \
        ['Pneumonia caused by the Bacteria Anthrax', 'Bacterial Pneumonia'], \
        ['Pneumonia caused by Mycoplasma Pneumoniae', 'Mycoplasma Pneumonia'], \
        ['Pneumonia due to Methicillin-Sensitive Staphylococcus Aureus Acquired in Hospital',
         'Bacterial Pneumonia'], \
        ['Pneumonia due to the Bacteria Haemophilus Parainfluenzae', 'Bacterial Pneumonia'], \
        ['Pneumonia caused by a Fungus', 'Fungal Pneumonia'], \
        ['Pneumonia caused by the Bacteria Chlamydia', 'Bacterial Pneumonia'], \
        ['Pneumonia caused by Pneumocystis Jirovecii Organism', 'Fungal Pneumonia'], \
        ['Post-Menopausal Osteoporosis Prevention', 'Osteoporosis'], \
        ['Posttraumatic Stress Syndrome', 'Post Traumatic Stress Disorder'], \
        ['Psoriasis of Scalp', 'Psoriasis'], \
        ['Psoriasis associated with Arthritis', 'Psoriasis'], \
        ['Pulmonary Arterial Hypertension', 'Pulmonary Hypertension'], \
        ['Petit Mal Epilepsy with Multiple Seizure Types', 'Epilepsy'], \
        ['Petit Mal Seizures', 'Seizures'], \
        ['Presence of Head Lice', 'Head Lice'], \
        ['Premature Ejection of Semen', 'Premature Ejaculation'], \
        ['Presence of Body Lice', 'Body Lice'], \
        ['Pain associated with Arthritis', 'Arthritis Pain'], \
        ['Prevent Nausea and Vomiting After Surgery', 'Nausea/Vomiting Postoperative'], \
        ['Prevent Nausea and Vomiting from Cancer Chemotherapy', 'Nausea/Vomiting, Chemotherapy Induced'], \
        ['Prevention for a Blood Clot going to the Brain', 'Atrial Fibrillation'], \
        ['Prevent Recurrent Herpes Simplex Infection', 'Herpes Simplex'], \
        ['Prevention of Transient Ischemic Attacks', 'Ischemic Stroke'], \
        ['Prevention of Streptococcus Pneumoniae Infection', 'Pneumonia'], \
        ['Prevention of Recurrent Atrial Fibrillation', 'Atrial Fibrillation'], \
        ['Prevention of Osteoporosis', 'Osteoporosis'], \
        ['Prevention of Type 2 Diabetes Mellitus', 'Type 2 Diabetes Mellitus'], \
        ['Prevention of Motion Sickness', 'Motion Sickness'], \
        ['Prevention of Vitamin D Deficiency', 'Vitamin D Deficiency'], \
        ['Prevention of Vitamin B12 Deficiency', 'Vitamin B12 Deficiency'], \
        ['Prevent Radiation-Induced Nausea and Vomiting', 'Nausea/Vomiting, Radiation Induced'], \
        ['Paroxysmal Supraventricular Tachycardia', 'Ventricular Tachycardia'], \
        ['Repeated Episodes of Anxiety', 'Anxiety'], \
        ['Repeated Seizures with Unconsciousness Between Episodes', 'Seizures'], \
        ['Recurrent Genital Herpes', 'Herpes'], \
        ['Runny Nose', 'Allergic Rhinitis'], \
        ['Recurrent Genital Herpes', 'Genital Herpes'], \
        ['renal cell carcinoma adjuvant therapy following nephrectomy', 'Renal Cell Carcinoma'], \
        ['ROS1 Positive Non-Small Cell Lung Cancer', 'Non-Small Cell Lung Cancer'], \
        ['Recurrent Cold Sore', 'Cold Sores'], \
        ['Scattered Infection caused by Coccidioides Fungus', 'Fungal Infection'], \
        ['Seasonal Runny Nose', 'Allergic Rhinitis'], \
        ['Staphylococcus Saprophyticus Infection of Urinary Tract', 'Urinary Tract Infection'], \
        ['Seizures with Breaks in Consciousness & Other Symptoms', 'Seizures'], \
        ['Seizure with Loss of Normal Tone or Strength', 'Seizures'], \
        ['Seizures with Irregular Muscle Contractions', 'Seizures'], \
        ['Seizure Occurring during Neurosurgery', 'Seizures'], \
        ['Severe Psoriasis that is Resistant to Treatment', 'Psoriasis'], \
        ['Simple Partial Seizures', 'Seizures'], \
        ['Skin Infection due to Staphylococcus Aureus Bacteria', 'Bacterial Skin Infection'], \
        ['Skin Infection due to Streptococcus Pyogenes Bacteria', 'Bacterial Skin Infection'], \
        ['Skin Condition', 'skin infection'],\
        ['Small Cell Cancer of the Lung', 'Lung Cancer'], \
        ['Sneezing', 'Allergic Rhinitis'], \
        ['Stop Smoking', 'Smoking Cessation'], \
        ['Stuffy Nose', 'Allergic Rhinitis'], \
        ['Sickle Cell Anemia', 'Anemia'], \
        ['Stones in the Urinary Tract', 'Urinary Tract Stones'], \
        ['Supraventricular Cardiac Arrhythmia', 'Ventricular Tachycardia'], \
        ['Severe Sinusitis caused by Haemophilus Influenzae', 'Sinusitis'], \
        ['Skin Infection due to Anaerobic Bacteria', 'Bacterial Skin Infection'], \
        ['Skin Rash', 'Rash'], \
        ['Skin Rash with Sloughing', 'Rash'], \
        ['Strep Throat and Tonsillitis', 'Strep Throat'], \
        ['Severe Pain', 'Pain'], \
        ['Severe Uncontrolled High Blood Pressure', 'High Blood Pressure'], \
        ['Tonic-Clonic Epilepsy', 'Epilepsy'], \
        ['Treatment to Prevent a Blood Clot in the Lung', 'Pulmonary Embolism'], \
        ['Transient Ischemic Attack', 'Ischemic Stroke'], \
        ['Treatment to Prevent Blood Clots in Chronic Atrial Fibrillation', 'Atrial Fibrillation'], \
        ['Treatment To Prevent Vitamin Deficiency', 'Vitamin Deficiency'], \
        ['Urinary Tract Infection due to E. Coli Bacteria', 'Bacterial Urinary Tract Infection'], \
        ['Urinary Tract Infection caused by Staphylococcus Aureus', 'Urinary Tract Infection'], \
        ['Urinary Tract Infection due to Staphylococcus Epidermidis', 'Urinary Tract Infection'], \
        ['Urinary Tract Infection caused by Citrobacter', 'Bacterial Urinary Tract Infection'], \
        ['Urinary Tract Infection caused by Klebsiella Bacteria', 'Bacterial Urinary Tract Infection'], \
        ['Urinary Tract Infection caused by Morganella Morganii', 'Bacterial Urinary Tract Infection'], \
        ['Urinary Tract Infection due to Candida Albicans Fungus', 'Urinary Tract Infection'], \
        ['Ulcer of Duodenum caused by Bacteria Helicobacter Pylori', 'Helicobacter Pylori Infection'], \
        ['Urinary Tract Infection Prevention', 'Urinary Tract Infection'], \
        ['Ulcerative Colitis currently Without Symptoms', 'Ulcerative Colitis'], \
        ['Ventricular Rate Control in Atrial Fibrillation', 'Ventricular Tachycardia'], \
        ['Weight Loss Management for Overweight Person with BMI 27 to 29 and Weight-Related Comorbidity',
         'Obesity'], \
        ['Vitamin D Deficiency (High Dose Therapy)', 'Vitamin D Deficiency'], \
        ['Weight Loss Management for an Obese Person', 'Obesity'], \
        ['Worsening of Asthma', 'Asthma'], \
        ['Yeast Infection of Vagina and Vulva', 'Vaginal Yeast Infection'] \
        ]

    word_replace_drugs_com = [ \
        ['acial Lipoatrophy', 'Facial Lipoatrophy'], \
        ['acial Wrinkles', 'Facial Wrinkles'], \
        ['Aggressive Behavi', 'Aggressive Behaviour'], \
        ['ailure to Thrive', 'Failure to Thrive'], \
        ['amilial Cold Autoinflammatory Syndrome', 'Familial Cold Autoinflammatory Syndrome'], \
        ['amilial Mediterranean Feve', 'Familial Mediterranean Fever'], \
        ['Aphthous Ulce', 'Aphthous Ulcer'], \
        ['atigue', 'Fatigue'], \
        ['Auditory Processing Disorde', 'Auditory Processing Disorder'], \
        ['Asthma, Maintenance', 'Asthma'], \
        ['Asthma, acute', 'Asthma'], \
        ['Binge Eating Disorde', 'Binge Eating Disorder'], \
        ['Bipolar Disorde', 'Bipolar Disorder'], \
        ['Bleeding Disorde', 'Bleeding Disorder'], \
        ['Body Dysmorphic Disorde', 'Body Dysmorphic Disorder'], \
        ['Borderline Personality Disorde', 'Borderline Personality Disorder'], \
        ['Brain Tum', 'Brain Tumor'], \
        ['Breast Cance', 'Breast Cancer'], \
        ['Breast Cancer, Adjuvant', 'Breast Cancer'], \
        ['Breast Cancer, Metastatic', 'Breast Cancer'], \
        ['Breast Cancer, Prevention', 'Breast Cancer'], \
        ['Breakthrough Pain', 'Chronic Pain'], \
        ['B12 Nutritional Deficiency', 'Vitamin B12 Deficiency'], \
        ['cal Segmental Glomerulosclerosis', 'Focal Segmental Glomerulosclerosis'], \
        ['Cance', 'Cancer'], \
        ['Colorectal Cance', 'Colorectal Cancer'], \
        ['Corneal Ulce', 'Corneal Ulcer'], \
        ['COPD, Maintenance', 'COPD'], \
        ['COPD, Acute', 'COPD'], \
        ['Conjunctivitis, Allergic', 'Conjunctivitis'], \
        ['Coronary Artery Disease', 'Coronary Artery Diseaser'], \
        ['Crohn\'s Disease, Maintenance', 'Crohn\'s Disease'], \
        ['Candida Urinary Tract Infection', 'Urinary Tract Infection'], \
        ['Dermatitis Herpeti', 'Dermatitis Herpetiformis'], \
        ['Diabetes, Type 1', 'Type 1 Diabetes Mellitus'], \
        ['Diabetes, Type 2', 'Type 2 Diabetes Mellitus'], \
        ['Dissociative Identity Disorde', 'Dissociative Identity Disorder'], \
        ['Duodenal Ulce', 'Duodenal Ulcer'], \
        ['emale Infertility', 'Female Infertility'], \
        ['Emergency Contraception', 'Birth Control'], \
        ['Endometrial Cance', 'Endometrial Cancer'], \
        ['Endometrial Hyperplasia, Prophylaxis', 'Endometrial Hyperplasia'], \
        ['Eye Redness/Itching', 'Eye Redness'], \
        ['Gastric Cance', 'Gastric Cancer'], \
        ['Generalized Anxiety Disorde', 'Generalized Anxiety Disorder'], \
        ['Glioblastoma Multi', 'Glioblastoma Multiforme'], \
        ['Gout, Acute', 'Gout'], \
        ['Gout, Prophylaxis', 'Gout'], \
        ['Head and Neck Cance', 'Head and Neck Cancer'], \
        ['Herpes Zoste', 'Herpes'], \
        ['Herpes Zoster, Prophylaxis', 'Herpes'], \
        ['Herpes Simplex, Mucocutaneous / Immunocompetent Host', 'herpes simplex'],\
        ['Herpes Simplex, Mucocutaneous / Immunocompromised Host', 'herpes simplex'],\
        ['Human Papillomavirus Prophylaxis', 'Human Papillomavirus'], \
        ['Hypoactive Sexual Desire Disorde', 'Hypoactive Sexual Desire Disorder'], \
        ['Hyperparathyroidism Secondary to Renal Impairment', 'Hyperthyroidism'], \
        ['Hypothyroidism, After Thyroid Removal', 'Hypothyroidism'], \
        ['Herpes Simplex, Suppression', 'Herpes'], \
        ['Herpes Simplex', 'Herpes'], \
        ['ibrocystic Breast Disease', 'Fibrocystic Breast Disease'], \
        ['ibromyalgia', 'Fibromyalgia'], \
        ['Impetig', 'Impetigo'], \
        ['Intermittent Explosive Disorde', 'Intermittent Explosive Disorder'], \
        ['Iron Deficiency Anemia', 'anemia'],\
        ['Juvenile Rheumatoid Arthritis', 'Rheumatoid Arthritis'], \
        ['m Pain Disorde', 'm Pain Disorder'], \
        ['Major Depressive Disorde', 'Major Depressive Disorder'], \
        ['Migraine Prevention', 'Migraine'], \
        ['Melanoma, Metastatic', 'Melanoma'], \
        ['mance Anxiety', 'Performance Anxiety'], \
        ['Malaria Prevention', 'Malaria'], \
        ['Metastatic Castration-Resistant Prostate Cancer', 'Prostate Cancer'], \
        ['Non - Small Cell Lung Cance', 'Non - Small Cell Lung Cancer'], \
        ['Non-Small Cell Lung Cance', 'Non-Small Cell Lung Cancer'], \
        ['NSAID - Induced Gastric Ulce', 'NSAID - Induced Gastric Ulcer'], \
        ['Nausea/Vomiting, Postoperative', 'Nausea/Vomiting'], \
        ['Obsessive Compulsive Disorde', 'Obsessive Compulsive Disorder'], \
        ['Oppositional Defiant Disorde', 'Oppositional Defiant Disorder'], \
        ['Ovarian Cance', 'Ovarian Cancer'], \
        ['Overactive Bladde', 'Overactive Bladder'], \
        ['Ocular Rosacea', 'Rosacea'], \
        ['Osteolytic Bone Lesions of Multiple Myeloma', 'Multiple Myeloma'], \
        ['Osteolytic Bone Metastases of Solid Tumors', 'Multiple Myeloma'], \
        ['Pain/Feve', 'Pain/Fever'], \
        ['Pancreatic Cance', 'Pancreatic Cancer'], \
        ['Panic Disorde', 'Panic Disorder'], \
        ['Paranoid Disorde', 'Paranoid Disorder'], \
        ['Peptic Ulce', 'Peptic Ulcer'], \
        ['Periodic Limb Movement Disorde', 'Periodic Limb Movement Disorder'], \
        ['Persistent Depressive Disorde', 'Persistent Depressive Disorder'], \
        ['Post Traumatic Stress Disorde', 'Post Traumatic Stress Disorder'], \
        ['Premenstrual Dysphoric Disorde', 'Premenstrual Dysphoric Disorder'], \
        ['Prostate Cance', 'Prostate Cancer'], \
        ['Prevention of Bladder Infection', 'Bladder Infection'], \
        ['Prevention of Osteoporosis', 'Osteoporosis'], \
        ['Prevention of Bladder infection', 'Bladder Infection'], \
        ['Prevention of Dental Caries', 'Dental Caries'], \
        ['Pinworm Infection (Enterobius vermicularis)', 'Pinworm Infection'], \
        ['Q Feve', 'Q Fever'], \
        ['Rat-bite Feve', 'Rat-bite Fever'], \
        ['Rhinitis', 'Allergic Rhinitis'], \
        ['Salivary Gland Cance', 'Salivary Gland Cancer'], \
        ['Schizoaffective Disorde', 'Schizoaffective Disorder'], \
        ['Seasonal Affective Disorde', 'Seasonal Affective Disorder'], \
        ['Shift Work Sleep Disorde', 'Shift Work Sleep Disorder'], \
        ['Sinus Symptoms', 'sinusitis'],\
        ['Skin Cance', 'Skin Cancer'], \
        ['Skin Rash', 'rash'],\
        ['Seizure prevention', 'Seizures'], \
        ['Social Anxiety Disorde', 'Social Anxiety Disorder'], \
        ['Somatoform Pain Disorde', 'Somatoform Pain Disorder'], \
        ['Shift Work Sleep Disorde', 'Shift Work Sleep Disorder'], \
        ['Skin Cance', 'Skin Cancer'], \
        ['Skin or Soft Tissue Infection', 'Skin Infection'], \
        ['Skin and Structure Infection', 'Skin Infection'], \
        ['Social Anxiety Disorde', 'Social Anxiety Disorder'], \
        ['Somatoform Pain Disorde', 'Somatoform Pain Disorder'], \
        ['Stomach Cance', 'Stomach Cancer'], \
        ['Stomach Ulce', 'Stomach Ulcer'], \
        ['Seizure Prevention', 'Seizures'], \
        ['Anemia, Sickle Cell', 'Anemia'], \
        ['Anemia, Chemotherapy Induced', 'Anemia'], \
        ['t Pac with Cyclobenzaprine (cyclobenzaprine)', 'Comfort Pac with Cyclobenzaprine (cyclobenzaprine)'], \
        ['Temporomandibular Joint Disorde', 'Temporomandibular Joint Disorder'], \
        ['Testicular Cance', 'Testicular Cancer'], \
        ['Thyroid Cance', 'Thyroid Cancer'], \
        ['tic (mycophenolic acid)', 'Myfortic (mycophenolic acid)'], \
        ['Tic Disorde', 'Tic Disorder'], \
        ['Typhoid Feve', 'Typhoid Fever'], \
        ['Tuberculosis, Prophylaxis', 'Tuberculosis'], \
        ['Tuberculosis, Active', 'Tuberculosis'], \
        ['Tuberculosis, Latent', 'Tuberculosis'], \
        ['unctional Gastric Disorde', 'Functional Gastric Disorder'], \
        ['ungal Infection Prophylaxis', 'Fungal Infection Prophylaxis'], \
        ['ungal Pneumonia', 'Fungal Pneumonia'], \
        ['Ulcerative Colitis, Active', 'Ulcerative Colitis'], \
        ['Ulcerative Colitis, Maintenance', 'Ulcerative Colitis'], \
        ['Varicella-Zoste', 'Varicella-Zoster'], \
        ['Vertig', 'Vertigo'], \
        ['zen Shoulde', 'Zen Shoulder'] \
        ]

    word_replace_druglib = [ \
        ['? \'heart failure\'', 'heart failure'], \
        ['acid reflux', 'gerd'], \
        ['acne vulgaris', 'acne'], \
        ['acne, birth control', 'acne'], \
        ['severe acne', 'acne'], \
        ['acne/oily skin', 'acne'], \
        ['acne and wrinkles', 'acne'], \
        ['acne, anti-aging', 'acne'], \
        ['acne/dull skin', 'acne'], \
        ['acne/wrinkles', 'acne'], \
        ['acne, aging', 'acne'], \
        ['acne, photoaging', 'acne'], \
        ['acne/anti-agin', 'acne'], \
        ['adult acne/wrinkles', 'acne'], \
        ['adult onset acne', 'acne'], \
        ['facial acne', 'acne'], \
        ['acne - blackheads and acne scars', 'acne'], \
        ['acne cysts', 'acne'], \
        ['acne/wrinkles', 'acne'], \
        ['clearing skin', 'acne'], \
        ['mild acne', 'acne'], \
        ['acne and sun damage', 'acne'], \
        ['acid reflux, gerd', 'gerd'], \
        ['acute sinusitis/bronchitis', 'sinusitis'], \
        ['add/adhd', 'adhd'], \
        ['add', 'adhd'], \
        ['add management', 'adhd'], \
        ['adha', 'adhd'], \
        ['adhd (attention deficit hyperactive disorder)', 'adhd'], \
        ['adhd (predominantly inattentive)', 'adhd'], \
        ['adhd, depression / anxiety', 'adhd'], \
        ['adhd, inattentive type', 'adhd'], \
        ['addh', 'adhd'], \
        ['adhd, depression/anxiety', 'adhd'], \
        ['adhd', 'adhd'], \
        ['adult adhd', 'adhd'], \
        ['attention deficit disorder', 'adhd'], \
        ['add, depression', 'adhd'], \
        ['adult add', 'adhd'], \
        ['adult acne', 'acne'], \
        ['acne  and scarring', 'acne'], \
        ['alergies', 'allergies'], \
        ['alergy', 'allergies'], \
        ['allergies', 'allergies'], \
        ['allegry', 'allergies'], \
        ['allergy', 'allergies'], \
        ['allergy reaction on the face incl swollen face', 'allergies'], \
        ['alzheimer\'s', 'alzheimer\'s disease'], \
        ['alzheimers', 'alzheimer\'s disease'], \
        ['aging skin', 'anti ageing'], \
        ['aging', 'anti ageing'], \
        ['acne problem', 'acne'], \
        ['anti aging', 'anti ageing'], \
        ['anti-Aging', 'anti ageing'], \
        ['anti-aging prophilatic', 'anti ageing'], \
        ['anti-aging, acne', 'anti ageing'], \
        ['antiaging', 'anti ageing'], \
        ['antianxiety/depression', 'anxiety and depression'], \
        ['anxeity', 'anxiety'], \
        ['anxiety, mild depression', 'anxiety and depression'], \
        ['anxiety/panic attacks', 'panic disorder'], \
        ['anxiety, panic disorder', 'panic disorder'], \
        ['anxiety/ ocpd /depression', 'anxiety and depression'], \
        ['anxiety/ mild depression', 'anxiety and depression'], \
        ['arthritis in lyme disease', 'arthritis'], \
        ['asthma/allergies', 'asthma and allergic rhinitis'], \
        ['asthma \ allergies', 'asthma and allergic rhinitis'], \
        ['asthma, allergies', 'asthma and allergic rhinitis'], \
        ['asthma, emphysema', 'asthma'], \
        ['asthmas/ rhinitis', 'asthma and allergic rhinitis'], \
        ['anxety / depression', 'anxiety and depression'], \
        ['anxiety/ panic attacks', 'panic disorder'], \
        ['anxiety/panic attacks/', 'panic disorder'], \
        ['anxety / depression', 'anxiety and depression'], \
        ['anxiety/trouble sleeping', 'anxiety'], \
        ['anxety & depression', 'anxiety and depression'], \
        ['anxiety induced palpitations', 'anxiety'], \
        ['airplane flight anxiety', 'anxiety'], \
        ['anxiety/ depreesion', 'anxiety and depression'], \
        ['anxiety, depresion', 'anxiety and depression'], \
        ['anxiety, depression', 'anxiety and depression'], \
        ['anxiety/depression', 'anxiety and depression'], \
        ['anxiety rapid onset', 'anxiety'], \
        ['anxiety related to severe pms', 'anxiety'], \
        ['anti-inflammatory/pain', 'inflammatory conditions'], \
        ['alcohol addiction', 'alcohol withdrawal'], \
        ['arthritis pain', 'arthritis'],\
        ['asthmatic bronchitis', 'bronchitis'], \
        ['astham', 'asthma'], \
        ['anxiety, panic attck, nervousness', 'anxiety'], \
        ['back acne', 'acne'], \
        ['birth control/ regular periods.', 'birth control'], \
        ['b.p.p.v.(benign proxysmal positional vertigo)', 'vertigo'], \
        ['bi-polar', 'bipolar disorder'], \
        ['bipolar mania', 'bipolar disorder'], \
        ['bronkitis', 'bronchitis'], \
        ['birth prevention', 'birth control'], \
        ['bi-polar disorder', 'bipolar disorder'], \
        ['bipolar', 'bipolar disorder'], \
        ['bipolar disorder 2', 'bipolar disorder'], \
        ['bipolar ii', 'bipolar disorder'], \
        ['bipolar/raciness/insomnia', 'insomnia'], \
        ['bipolar disorder/panic attacks', 'panic disorder'], \
        ['back', 'back pain'], \
        ['back stiffness', 'back pain'], \
        ['back pain; restlessness', 'back pain'], \
        ['birth control, menstrual cramps', 'birth control'], \
        ['birth control. prevention of pregnacy', 'birth control'], \
        ['birth control/control of menstrual cycle', 'birth control'], \
        ['back pain slipped disk', 'back pain'], \
        ['bladder control', 'urinary incontinence'], \
        ['birth control/period regularity', 'birth control'], \
        ['chronic hepatitis c', 'hepatitis c'], \
        ['chronic lymphoid leukemia', 'chronic lymphocytic leukemia'], \
        ['chonic pain', 'chronic pain'], \
        ['cluster headache', 'cluster headaches'], \
        ['complicated skin infection', 'skin infection'], \
        ['colitis', 'ulcerative colitis'], \
        ['cure for acne', 'acne'], \
        ['contraceptive', 'birth control'], \
        ['chronic bronch/asthma', 'bronchitis'], \
        ['colestrol', 'cholesterol'], \
        ['cholesterol/high blood pressure', 'high blood pressure'], \
        ['contraception', 'birth control'], \
        ['cystic acne', 'acne'], \
        ['cancer prevention', 'cancer'], \
        ['chronic regional pain syndrome', 'chronic pain'], \
        ['chronic "atypical" depression', 'depression'], \
        ['chronic back pain/depression/anxiety', 'depression'], \
        ['chronic tension headache', 'headache'], \
        ['congestive heart failure and edema', 'heart failure'], \
        ['chronic severe insomnia', 'insomnia'], \
        ['copd', 'copd'], \
        ['can\'t sleep', 'insomnia'], \
        ['cancer related pain', 'pain'], \
        ['cancer/constant pain', 'pain'], \
        ['cholesterol problems', 'high cholesterol'], \
        ['cold sores/fever blisters', 'cold sores'], \
        ['depression, anxiety & pain', 'depression'], \
        ['depression, anxiety, ocd', 'depression'], \
        ['depression, social anxiety disorder', 'social anxiety disorder'], \
        ['depression/difficulty sleeping', 'insomnia'], \
        ['depression/post-partum', 'postpartum depression'], \
        ['depression, rumination, anxiety', 'depression'], \
        ['depression not resolved with antidepressant drugs', 'depression'], \
        ['depression & anxiety', 'anxiety and depression'], \
        ['depression and anxiety', 'anxiety and depression'], \
        ['depression/anxiety/ptsd', 'anxiety and depression'], \
        ['depression, ptsd fatigue', 'depression'], \
        ['depression, clinical level', 'depression'], \
        ['severe clinical depression', 'depression'], \
        ['dizzyness,, vertigo, nausea,', 'vertigo'], \
        ['depression and anxiety.', 'anxiety and depression'], \
        ['depression and generalized anxiety', 'anxiety and depression'], \
        ['depression anxiety', 'anxiety and depression'], \
        ['depression not resolved with antidepressant drugs', 'anxiety and depression'], \
        ['depression with anxiety', 'anxiety and depression'], \
        ['depression-anxiety', 'anxiety and depression'], \
        ['depression, anixety?', 'anxiety and depression'], \
        ['depression, anxiety', 'anxiety and depression'], \
        ['depression, axiety', 'anxiety and depression'], \
        ['depression/ anxiety', 'anxiety and depression'], \
        ['depression -- anxiety -- insominia', 'anxiety and depression'], \
        ['depression/anxiety', 'anxiety and depression'], \
        ['depression, fatigue', 'depression'], \
        ['depression, tension headache', 'depression'], \
        ['depression; intrusive suicidal impulses', 'depression'], \
        ['depression/add', 'depression'], \
        ['depression / bipolar', 'bipolar disorder'], \
        ['depression, irritability', 'depression'], \
        ['difficulty getting/holding erection', 'erectile dysfunction'], \
        ['diabetes type 2', 'type 2 diabetes mellitus'], \
        ['diabetes type ii', 'type 2 diabetes mellitus'], \
        ['diet', 'obesity'], \
        ['excessive fatigue', 'fatigue'], \
        ['ed', 'erectile dysfunction'], \
        ['erectile disfunction', 'erectile dysfunction'], \
        ['extremely dry skin', 'dry skin'], \
        ['EXTREMELY SEVERE ANXIETY', 'anxiety'],\
        ['eostrogen-positive breast cancer', 'breast cancer'], \
        ['difficulty sleeping', 'insomnia'], \
        ['fingernail fungus', 'onychomycosis, fingernail'], \
        ['fibromyalgia pain', 'fibromyalgia'], \
        ['flu symptoms', 'flu'],\
        ['for  back pain', 'back pain'], \
        ['facial herpes simplex', 'herpes'], \
        ['fatigue associated with multiple sclerosis', 'fatigue'], \
        ['fibromyalgia and depression', 'fibromyalgia'], \
        ['fungus', 'fungal infection prophylaxis'], \
        ['gerd', 'gerd'], \
        ['gerd/acid reflux', 'gerd'], \
        ['grand mal seizures', 'seizures'], \
        ['gad', 'generalized anxiety disorder'], \
        ['general depression/perimenopause', 'depression'], \
        ['high blood pressure and', 'high blood pressure'], \
        ['hiv', 'hiv infection'], \
        ['high c', 'high cholesterol'], \
        ['heart', 'heart failure'], \
        ['hypothyroid - hashimoto\'s disease', 'hashimoto\'s disease'], \
        ['hypothyriodism--hashimoto\'s thyroiditis', 'hashimoto\'s disease'], \
        ['hypothyroidism after thyroidectomy', 'hypothyroidism'], \
        ['hypertension (high blood pressure)', 'pulmonary hypertension'], \
        ['hypertension/high blood pressure', 'pulmonary hypertension'], \
        ['hyhpothyroidism', 'hypothyroidism'], \
        ['hypothyroid', 'hypothyroidism'], \
        ['high ldl', 'high cholesterol'], \
        ['high lpa', 'high cholesterol'], \
        ['heartburn/gerd', 'gerd'],
        ['high blood pressure & left ventricular hypertrophy', 'high blood pressure'], \
        ['hypothryroid', 'hypothyroidism'], \
        ['hormonal acne', 'acne'], \
        ['heavy menstrual bleeding', 'polycystic ovary syndrome'], \
        ['high  cholesterol', 'high cholesterol'], \
        ['hives', 'urticaria'], \
        ['heavy periods', 'polycystic ovary syndrome'], \
        ['high level anxiety/depression', 'anxiety'], \
        ['hyperpigmentation', 'acne'], \
        ['insomia', 'insomnia'], \
        ['irritable bowel syndrome-diarrhea', 'irritable bowel syndrome'], \
        ['insomnia, chronic pain', 'insomnia'], \
        ['insomnia, headaches', 'insomnia'], \
        ['insomnia - early awakening', 'insomnia'], \
        ['insomnia, migraines', 'insomnia'], \
        ['insomnia and anxiety', 'insomnia'], \
        ['insomnia/difficulty sleeping', 'insomnia'], \
        ['irregular periods', 'polycystic ovary syndrome'], \
        ['klebsiella pneumonia infection', 'pneumonia'], \
        ['knee pain/inflamation', 'knee pain'], \
        ['lyme ? or unknown', 'lyme'], \
        ['lose weight', 'weight loss'], \
        ['localized acne', 'acne'], \
        ['lack of attention for studying/school', 'adhd'], \
        ['loose weight', 'weight loss'], \
        ['low energy and depression', 'depression'], \
        ['lower back pain and migraine', 'back pain'], \
        ['low thyroid', 'hypothyroidism'],
        ['lyme', 'lyme disease'], \
        ['moderate persisting acne', 'acne'], \
        ['mild acne', 'acne'], \
        ['minor acne', 'acne'], \
        ['major chronic depressive disorder', 'major depressive disorder'], \
        ['major depressive disorder/ anxiety', 'major depressive disorder'], \
        ['major depression/anxiety', 'major depressive disorder'], \
        ['major depressive disorder/anxiety', 'major depressive disorder'], \
        ['mild to moderate depression', 'depression'], \
        ['malaria prevention', 'malaria'], \
        ['moderately severe acne', 'acne'], \
        ['muscular pain - arm', 'pain'], \
        ['mrsa', 'methicillin-resistant staphylococcus aureus infection'], \
        ['m.r.s.a.', 'methicillin-resistant staphylococcus aureus infection'], \
        ['mrsa infected hip resurfacing.', 'methicillin-resistant staphylococcus aureus infection'], \
        ['migraine + birth control', 'migraine and birth control'], \
        ['musculoskeletal pain; nerve pain', 'neuropathic pain'], \
        ['mild depression and anxiety', 'anxiety and depression'], \
        ['migraines', 'migrane'], \
        ['migraine headaches', 'migraine'], \
        ['migraine headache', 'migraine'], \
        ['migraine prevention', 'migraine'], \
        ['menopausal', 'menopausal disorders'], \
        ['menopause', 'menopausal disorders'], \
        ['mitral  valve prolapse', 'mitral valve prolapse'], \
        ['mitral valve prolapse syndrome', 'mitral valve prolapse'], \
        ['ms-related fatigue', 'fatigue'], \
        ['neural pain', 'neuropathic pain'], \
        ['nummular eczema', 'eczema'], \
        ['nodular acne', 'acne'], \
        ['neuropathy back pain', 'neuropathic pain'], \
        ['non-small cell lung cance', 'non-small cell lung cancer'], \
        ['nightly leg pain', 'leg pain'], \
        ['juvenile idiopathic arthritis', 'arthritis'], \
        ['over weight', 'obesity'], \
        ['overweight', 'obesity'], \
        ['ocd', 'obsessive compulsive disorder'], \
        ['ocd, bipolor disease', 'obsessive compulsive disorder'], \
        ['ocd/depression', 'obsessive compulsive disorder'], \
        ['osteroporosis', 'osteoporosis'], \
        ['osteo-arthritis', 'osteoarthritis'], \
        ['osteoporsis', 'osteoporosis'], \
        ['osteopenia and osteoporosis', 'osteoporosis'], \
        ['ovarian cysts.', 'ovarian cysts'], \
        ['period pain', 'endometriosis'], \
        ['ptsd', 'post traumatic stress disorder'], \
        ['opiate dependency', 'opiate dependence'], \
        ['opiate addiction', 'opiate withdrawal'], \
        ['pain management', 'pain'], \
        ['post trauma depression', 'post traumatic stress disorder'], \
        ['panic attacks, depression', 'panic disorder'], \
        ['panic attack and anxiety', 'panic disorder'], \
        ['pain in legs (diagnosis restless leg syndrome)', 'restless legs syndrome'], \
        ['pain after minor surgery', 'postoperative pain'], \
        ['pain relief', 'pain'], \
        ['pain relief - toothache', 'pain'], \
        ['pain after surgery', 'postoperative pain'], \
        ['post-op pain', 'postoperative pain'], \
        ['post surgical pain', 'postoperative pain'], \
        ['post-surgical pain', 'postoperative pain'], \
        ['pain control', 'pain'], \
        ['pain/headaches', 'pain'], \
        ['pain, muscle strain', 'muscle pain'], \
        ['pain/arthritis', 'arthritis pain'], \
        ['pain/fever', 'pain'], \
        ['performance anxiety', 'anxiety'], \
        ['preventing malaria', 'malaria'], \
        ['possible uti - i think?', 'urinary tract infection'], \
        ['polysistic ovarian syndrome', 'polycystic ovary syndrome'], \
        ['prevent pregnancy', 'birth control'], \
        ['pregnancy prevention', 'birth control'], \
        ['panic attack', 'panic disorder'], \
        ['pcos', 'polycystic ovary syndrome'], \
        ['pcos/ irregular periods', 'polycystic ovary syndrome'], \
        ['pms', 'premenstrual syndrome'], \
        ['perioral dermatitis', 'dermatitis'], \
        ['pmdd', 'premenstrual dysphoric disorder'], \
        ['pain - chronic panceatitis', 'chronic pancreatitis'], \
        ['post partum depression', 'postpartum depression'], \
        ['qit smoking', 'smoking cessation'],\
        ['quit smoking', 'smoking cessation'],\
        ['quitting smoking', 'smoking cessation'],\
        ['r.a.', 'rheumatoid arthritis'], \
        ['r/a', 'rheumatoid arthritis'], \
        ['rhinitis', 'allergic rhinitis'], \
        ['ra, sj√∂gren syndrome', 'rheumatoid arthritis'], \
        ['restless sleep', 'insomnia'], \
        ['root canal pain', 'postoperative pain'], \
        ['regulate periods', 'polycystic ovary syndrome'], \
        ['skin acne', 'acne'], \
        ['sleep', 'insomnia'], \
        ['seizure/migraine', 'migraine'], \
        ['seizures,migraines,fibro.', 'seizures'], \
        ['sleeping', 'insomnia'], \
        ['severe depression< agrophobia & other phobias', 'agoraphobia'], \
        ['seasonal allergies', 'allergic rhinitis'], \
        ['severe allergies', 'allergic rhinitis'], \
        ['severe pain', 'pain'], \
        ['severe and chronic back pain', 'back pain'], \
        ['sciatica and back pain', 'back pain'], \
        ['stress-related anxiety', 'anxiety and stress'], \
        ['smoking', 'smoking cessation'], \
        ['stop smoking', 'smoking cessation'], \
        ['stopping smoking', 'smoking cessation'], \
        ['shingles pain', 'pain'], \
        ['sleep disorder/anxiety', 'anxiety'], \
        ['situational anxiety', 'anxiety'], \
        ['supposed adhd', 'adhd'], \
        ['stomach nervousness', 'gerd'], \
        ['spasdic bladder', 'overactive bladder'], \
        ['bladder pressure', 'overactive bladder'], \
        ['sleeplessness', 'insomnia'], \
        ['sleeplessness - depression', 'insomnia'], \
        ['sleep disorder, insomnia', 'insomnia'], \
        ['severe knee pain', 'knee pain'], \
        ['stress/insomnia', 'insomnia'], \
        ['sleep deprivation', 'insomnia'], \
        ['sleep aid', 'insomnia'], \
        ['situational atypical depression', 'depression'], \
        ['serve acne', 'acne'], \
        ['serious acne', 'acne'], \
        ['severe nodular acne', 'acne'], \
        ['severe migraine', 'migraine'], \
        ['sciatic nerve pain', 'neuropathic pain'], \
        ['supra ventricular tachycardia', 'supraventricular tachycardia'], \
        ['stop smoking/depression', 'smoking cessation'], \
        ['strep  throat', 'strep throat'], \
        ['sinus infection, bronchitis', 'sinusitis'], \
        ['tension and anxiety', 'anxiety'], \
        ['type 2 diabetes', 'type 2 diabetes mellitus'], \
        ['type ii diabetes mellitus', 'type 2 diabetes mellitus'], \
        ['toenail fungus', 'onychomycosis, toenail'], \
        ['trouble sleeping at night, tired during day', 'insomnia'], \
        ['temporary anxiety', 'anxiety'], \
        ['toothace', 'toothache'], \
        ['tonic clonic seizures', 'seizures'], \
        ['thyroid removal', 'hyperthyroidism'], \
        ['unrestful sleep, narcolepsy?', 'narcolepsy'], \
        ['thyroid disease', 'thyroid'], \
        ['throat infection and cough', 'throat infection'], \
        ['temporomandibular joint disorder (tmj)', 'jaw pain'], \
        ['treatment of acne', 'acne'], \
        ['low thyroid', 'thyroid'], \
        ['uti', 'urinary tract infection'], \
        ['unrestful sleep narcolepsy', 'narcolepsy'], \
        ['ulcerative cholitis', 'ulcerative colitis'], \
        ['upper respiratory infection', 'upper respiratory tract infection'], \
        ['very severe acne', 'acne'], \
        ['weightloss', 'weight loss'], \
        ['wrinkles, furrows', 'wrinkles'], \
        ['whiteheads', 'acne'], \
        ]

    if filetype == 'webmd':
        revised_df = match_and_replace(df, filetype, word_replace_webmd)
    elif filetype == 'drugs_com':
        revised_df = match_and_replace(df, filetype, word_replace_drugs_com)
    elif filetype == 'druglib':
        revised_df = match_and_replace(df, filetype, word_replace_druglib)

    return revised_df


def condition_filtering(df, filetype):
    if filetype == 'webmd':
        df = df[df.Condition != 'nan']
        df = df[df.Condition != "Other"]
    elif filetype == 'drugs_com':
        df = df[df.condition != 'nan']
        df = df[df.condition.str.contains("span") == False]
        df = df[df.condition.str.contains("Not Listed") == False]
    else:
        df = df[df.Condition != 'nan']

    return df


def trim_and_lowercase(filetype, df):
    if filetype == 'webmd':
        col_list = ['Condition', 'Drug', 'Reviews', 'Sex', 'Sides']
    elif filetype == 'druglib':
        col_list = ['Drug', 'Condition', 'Sex', 'Reviews', 'Side Effect']
    else: # drugs_com
        col_list = ['drug', 'condition', 'review']

    for col in col_list:
        df[col] = df[col].str.lower()

    # To lower case column name
    # column_list = list(df.columns.values)
    # column_list_lower = map(lambda x: x.lower(), column_list)
    # df.columns = column_list_lower
    return df


def load_data(filetype='webmd'):
    filename = filetype + '.csv'
    df = pd.read_csv(filename)
    return df


def cleaning_and_filtering():
    """
        Provide USER INPUT
        File type takes the input 1) webmd 2) drugs_com 3) druglib
    """

    filetype_list = ['webmd', 'drugs_com', 'druglib']
    for filetype in filetype_list:
        df_load = load_data('./../../dataset/' + filetype + '/' + filetype)
        print('Dataset shape before filtering: ', df_load.shape)
        if filetype == 'druglib':
            df = trim_and_lowercase(filetype, df_load)
        else:
            df = df_load
        parsed_df = word_filtering(df, filetype)
        filtered_df = condition_filtering(parsed_df, filetype)

        if filetype == 'druglib':
            filtered_df['Age_Group'] = filtered_df.apply(set_age_range, axis=1)
        if filetype == 'webmd':
            filtered_df = webmd_rating_average(filtered_df)
        filtered_df = trim_and_lowercase(filetype, filtered_df)

        print('Dataset shape after filtering: ', filtered_df.shape)

        pathlib.Path('./../../dataset').mkdir(exist_ok=True)
        pathlib.Path('./../../dataset/' + filetype).mkdir(exist_ok=True)
        filtered_df.to_csv('./../../dataset/' + filetype + '/' + filetype + '_v01_processed.csv', index=False)
        print('Data written to '+filetype+' csv')

