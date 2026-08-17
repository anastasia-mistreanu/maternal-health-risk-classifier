import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
import streamlit as st

st.set_page_config(page_title="Maternal Health Risk Classifier", layout="centered")

#load the model
#cached so model isn't reloaded every time a widget changes
@st.cache_resource
def load_artifacts():
    model = joblib.load("models/rf_model.joblib")
    encoder = joblib.load("models/label_encoder.joblib")
    feature_names = joblib.load("models/feature_names.joblib")
    explainer = shap.TreeExplainer(model)
    return model, encoder, feature_names, explainer
 
 
model, encoder, feature_names, explainer = load_artifacts()

#feature engineering
#match clean_data.py so predicitons match
def build_features(age, systolic, diastolic, bs, body_temp, heart_rate):
    row = {
        "Age": age,
        "SystolicBP": systolic,
        "DiastolicBP": diastolic,
        "BS": bs,
        "BodyTemp": body_temp,
        "HeartRate": heart_rate,
        "PulsePressure": systolic - diastolic,
        "HasHypertension": int(systolic >= 140 or diastolic >= 90),
        "AgeBracket_teen": age < 20,
        "AgeBracket_reproductive_age": 20 <= age <= 34,
        "AgeBracket_advanced_maternal_age": age >= 35,
    }
    # reindex forces the saved training column order
    return pd.DataFrame([row]).reindex(columns=feature_names)

#header
st.title("Maternal Health Risk Classifier")
st.caption(
    "Portfolio demonstration built on the UCI Maternal Health Risk dataset. "
    "Not a clinical tool and not validated for patient care."
)

 #inputs
 #6 raw vitals across 2 columns
st.subheader("Patient vitals")
 
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age (years)", 10, 70, 25)
    systolic = st.number_input("Systolic BP (mmHg)", 70, 200, 120)
    diastolic = st.number_input("Diastolic BP (mmHg)", 40, 130, 80)
with col2:
    bs = st.number_input("Blood sugar (mmol/L)", 4.0, 25.0, 7.0, step=0.1)
    body_temp = st.number_input("Body temperature (F)", 95.0, 105.0, 98.0, step=0.1)
    heart_rate = st.number_input("Heart rate (bpm)", 40, 130, 75)

 #make sure no impossible reading occur
if diastolic >= systolic:
    st.error("Diastolic pressure must be lower than systolic pressure.")
    st.stop()

 #prediction
features = build_features(age, systolic, diastolic, bs, body_temp, heart_rate)
 
prediction = model.predict(features)[0]
probabilities = model.predict_proba(features)[0]
label = encoder.classes_[prediction]

#result
st.subheader("Predicted risk level")
 
colour = {"high risk": "red", "mid risk": "orange", "low risk": "green"}[label]
st.markdown(f"### :{colour}[{label.title()}]")
 
prob_df = pd.DataFrame(
    {"Probability": probabilities}, index=[c.title() for c in encoder.classes_]
).sort_values("Probability", ascending=False)
st.bar_chart(prob_df)

#known failures
#identified via SHAP:
            #normal BP produces negative contribution that's large enough
            #to cancel severely elevated BS
if bs >= 15 and systolic < 140 and diastolic < 90 and label != "high risk":
    st.warning(
        "**Known model limitation.** This patient has severely elevated blood sugar "
        "with normal blood pressure. SHAP analysis showed the model treats normal "
        "blood pressure as protective, which can cancel out a high blood sugar "
        "reading. All five high-risk patients missed in testing fitted this pattern. "
        "Treat this prediction with caution."
    )

#explanation w/ SHAP
st.subheader("Why this prediction")
st.caption(
    "Each bar shows how much that reading pushed the prediction toward or away "
    "from the predicted class, starting from the model's average output."
)
 
explanation = explainer(features)
 
fig, _ = plt.subplots()
shap.plots.waterfall(explanation[0, :, prediction], show=False)
st.pyplot(fig, bbox_inches="tight")
plt.close(fig)

 #methodology
with st.expander("Model details"):
    st.markdown(
        """
        **Model.** Random Forest (100 trees), selected over logistic regression on
        stratified 5-fold cross-validation: macro F1 0.857 (sd 0.023) versus 0.608
        (sd 0.044).
 
        **Evaluation.** Macro F1 and per-class recall were prioritised over accuracy,
        since a missed high-risk patient is the most clinically costly error.
 
        **Limitations.** Trained on 1010 records from a single dataset, with no
        external validation. The model under-flags patients with elevated blood sugar
        and normal blood pressure. Some records contain implausible age values, which
        were retained and documented during cleaning.
        """
    )
 