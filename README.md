Maternal Health Risk Classifier

A machine learning pipeline that predicts pregnancy risk level (low, mid, high) from six routine vital signs, with SHAP explanations for every prediction.

Live demo: https://maternal-health-risk-classifier.streamlit.app/

Rationale

I wanted a project that went past reporting an accuracy score. The interesting question with any clinical classifier is not how often it is right, but where it fails and whether those failures are the dangerous kind. Most of the work here is in the evaluation rather than the modelling.

The headline result is that the model reaches a macro F1 of 0.86. The more useful result is that I found a specific, reproducible failure mode using SHAP, and built a warning for it directly into the demo app.

Dataset

UCI Maternal Health Risk dataset [1], collected from hospitals, community clinics and maternal health care centres in rural Bangladesh through an IoT-based risk monitoring system. Stored and queried in SQLite.

Target variable is RiskLevel with three classes: low risk, mid risk, high risk.

Six raw features: Age (years), SystolicBP and DiastolicBP (mmHg), BS (blood sugar, mmol/L), BodyTemp (Fahrenheit), HeartRate (bpm).

The dataset is licensed CC BY 4.0 and is included in this repository under data/.

Cleaning and feature engineering

Two rows were removed for a recorded heart rate of 7 bpm, which is not physiologically possible and is commonly flagged in other analyses of this dataset [2, 3, 4]. That leaves 1010 records for modelling.

Three features were engineered in SQL:

PulsePressure, the difference between systolic and diastolic pressure
HasHypertension, a binary flag for systolic at or above 140 or diastolic at or above 90 [6]
AgeBracket, splitting age into teen (under 20), reproductive age (20 to 34) and advanced maternal age (35 and over), following the thresholds used in the obstetric literature [8, 9]

AgeBracket was one-hot encoded, giving 11 features in total. RiskLevel was label encoded, which produces the alphabetical order 0 = high risk, 1 = low risk, 2 = mid risk. Every confusion matrix in the notebooks should be read against that order.

I kept the extreme age values rather than removing them. Four records are aged 10 and five are aged 65 to 70, none of which are plausible pregnancies. No published analysis of this dataset that I could find excludes them, so removing them would have made my results harder to compare. This turned out to matter, and I come back to it under limitations.

Models

An 80/20 stratified split was used throughout, with random_state=42. Logistic regression was scaled with StandardScaler; Random Forest was left unscaled, since trees split on raw thresholds.

Model	Accuracy	Macro F1
Logistic regression (baseline)	0.61	0.60
Logistic regression (balanced class weights)	0.58	0.59
Random Forest	0.85	0.85

Class weighting made logistic regression slightly better at high and mid risk but worse overall, so I kept the unweighted baseline as the comparison point.

Random Forest improved on every class. The largest gain was in mid-risk recall, which rose from 0.36 to 0.85. Mid risk was the baseline's clear weak point, with 37 of 67 mid-risk patients misclassified as low risk. That pattern suggests the relationship between vitals and risk level is non-linear, which a single linear decision boundary cannot capture.

Cross-validation

Every result above comes from one split, so I cross-validated both models on the same five stratified folds to check whether the gap was real.

Model	Mean macro F1	Standard deviation
Random Forest	0.857	0.023
Logistic regression	0.608	0.044

The 0.249 gap matches the 0.25 seen in the single split, so the Random Forest advantage holds. Random Forest is also the more stable model, with fold scores spanning 0.830 to 0.885 against 0.559 to 0.677 for logistic regression.

The standard deviation is useful beyond confirming the result. It sets a noise floor of roughly 0.02, below which any apparent improvement from tuning would not be meaningful.

Why macro F1 rather than accuracy

The classes are imbalanced enough that accuracy can hide poor performance on a minority class, so macro F1 and per-class recall were prioritised throughout.

The errors are also not equally costly. A false negative for high risk, meaning a genuinely high-risk patient predicted as low or mid, is the most clinically dangerous outcome this model can produce. A false positive is comparatively cheap, resulting in extra monitoring rather than a missed danger. That framing shaped how I read every confusion matrix.

Feature importance

I used two methods, because impurity-based importance is biased toward continuous features and splits credit between correlated ones.

Both agree on the top three: BS, SystolicBP and Age. Blood sugar dominates. Shuffling it costs 0.30 macro F1, dropping the model from 0.86 to roughly 0.56. This is consistent with gestational diabetes being a well-established pregnancy risk factor [5].

The engineered features did not earn their place. HasHypertension and all three AgeBracket columns score at or near zero under both methods. The model extracts this information directly from raw Age and blood pressure values, and finds better thresholds than the ones I hard-coded. Pre-binning a continuous variable discarded information rather than adding it.

PulsePressure contributed modestly under impurity-based importance but scored low under permutation importance. That is a redundancy effect rather than irrelevance, and it applies to the blood pressure features generally: shuffling one leaves the others available to compensate, so no single blood pressure column looks essential even though blood pressure as a group clearly matters [11].

Explainability

SHAP values were computed on the Random Forest using TreeExplainer.

All directional relationships are clinically plausible. Higher blood sugar, blood pressure and body temperature all push toward high risk. Several features are one-sided, contributing nothing at normal values and pushing toward high risk only when abnormal, which is how clinical thresholds behave in practice.

HasHypertension illustrates the difference between the two analyses well. It scores near zero on permutation importance but shows a clear, correctly directed effect in SHAP. Both are right: the signal is real but redundant, already available through the raw blood pressure columns.

The main limitation

All five high-risk patients the model missed share a pattern. Every one has normal blood pressure, and four of the five have severely elevated blood sugar, between 15.0 and 18.0.

SHAP shows exactly why. For one of these patients, blood sugar of 18.0 contributes +0.30 toward high risk, the largest single contribution anywhere in my analysis. But the blood pressure features push back by almost the same amount, totalling -0.29. The prediction moves from a base value of 0.268 to 0.277 and the patient is classified mid risk.

The model does not ignore high blood sugar. It treats normal blood pressure as actively protective rather than neutral, and that negative contribution is enough to cancel a severely elevated glucose reading. Since poorly controlled blood sugar is a risk factor independent of blood pressure [5], this is the model's most serious weakness, and it affects the error type that matters most.

The Streamlit app carries a warning for exactly this pattern. Any real deployment would need a rule-based flag for extreme blood sugar applied alongside the classifier rather than relying on it alone.

Other limitations

All five missed cases fall in the advanced maternal age bracket, with recorded ages of 42, 60, 50, 60 and 65. Four are not plausible pregnancies, so the decision to keep extreme age values has a visible cost here. With only five cases I cannot separate genuine model weakness from unreliable records, and both explanations should be treated as open. Maternal age extremes are associated with adverse outcomes [7, 10], but not at the ages recorded in these rows.

Beyond that: the model is trained on 1010 records from a single dataset with no external validation, so performance on a different population is unknown. Threshold tuning and hyperparameter tuning were not attempted. The dataset offers no information on gestational age, parity or medical history, all of which would matter clinically.

This is a portfolio project. It is not validated for patient care and should not be used for it.

Repository structure
├── app.py                  Streamlit demo
├── clean_data.py           SQL cleaning and feature engineering
├── data/                   SQLite database
├── models/                 Exported model, encoder and feature names
├── notebooks/
│   ├── eda.ipynb           Exploratory analysis
│   └── modeling.ipynb      Modelling, cross-validation, SHAP
├── references.md           Full reference list
└── requirements.txt
Running it locally
bash
git clone https://github.com/yourusername/maternal-health-risk-classifier.git
cd maternal-health-risk-classifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

The trained model is committed to models/, so the app runs without retraining. To regenerate it, run clean_data.py and then notebooks/modeling.ipynb.

References

Full numbered reference list in references.md, Vancouver style, cited inline above by bracketed number.