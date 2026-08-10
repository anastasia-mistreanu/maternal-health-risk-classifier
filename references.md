# References

Numbered reference list (Vancouver style). Cited inline throughout the project using the bracketed number, e.g. "...a well-established pregnancy risk factor [5]."

1. Ahmed, M., Kashem, M. A., Rahman, M., Khatun, S. (2020). Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things (IoT). *Lecture Notes in Electrical Engineering*, vol 632. https://archive.ics.uci.edu/dataset/863/maternal+health+risk

2. Predicting maternal risk level using machine learning models. *PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11657143/

3. Deep hybrid model for maternal health risk classification in pregnancy: synergy of ANN and random forest. *Frontiers in Artificial Intelligence*. https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2023.1213436/full

4. Rickens, B. Maternal Health Risk (notebook analysis). https://bryanrickens.github.io/Notebooks/maternal.html

5. Gestational Diabetes Mellitus—Recent Literature Review. *PMC*. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572242/

6. European Society of Cardiology / European Society of Hypertension. (2018). ESC-ESH Guidelines: Definition of hypertension and pressure goals during treatment. https://www.escardio.org/communities/councils/cardiology-practice/scientific-documents-and-publications/ejournal/volume-17/definition-of-hypertension-and-pressure-goals-during-treatment-esc-esh-guidelin/

7. Maternal age extremes and adverse pregnancy outcomes in low-resourced settings. *PMC*. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10715413/

8. The Definition of the Upper Limit of Adolescent Age in Terms of Adverse Pregnancy Outcomes. *PMC*. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8777262/

9. American College of Obstetricians and Gynecologists (ACOG). (2022). Pregnancy at Age 35 Years or Older: Obstetric Care Consensus. https://www.acog.org/clinical/clinical-guidance/obstetric-care-consensus/articles/2022/08/pregnancy-at-age-35-years-or-older

10. Advanced Maternal Age and Adverse Pregnancy Outcome: Evidence from a Large Contemporary Cohort. *PLOS ONE*. https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0056583

11. A Comprehensive Review of Hypertension in Pregnancy. *PMC*. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3366228/

---

## Notes / decisions not tied to a single external source

- **Extreme age values (Age < 12 or >= 65):** kept in the dataset rather than removed. 4 rows at exactly age 10 (2 exact duplicates), 5 rows aged 65-70. No published work using this dataset was found excluding age outliers (only the heart rate=7 case, sources 2-4, is commonly flagged). Documented as a known limitation.
- **Hypertension threshold choice (140/90 vs. newer 130/80 ACC/AHA):** 140/90 [6] chosen over the newer US ACC/AHA threshold as the more globally-recognized traditional cutoff, appropriate given the dataset's non-US context.

