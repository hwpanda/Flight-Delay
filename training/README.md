# Model training

This directory is the reproducible training workspace for the flight-delay
predictor served by the application. It intentionally keeps raw data and
generated experiment outputs out of Git; see `.gitignore`.

## Current model lineage

The application serves `model/xgb_final_model_26.pkl`. The legacy notebooks
show that it was selected as grid-search model 26 after:

1. downloading BTS on-time-performance data for 2023–2025;
2. adding airport weather and B43 aircraft attributes;
3. using 2025 May–July as a holdout sample;
4. fitting WOE maps for `Reporting_Airline`, `Origin`, and `Dest` from the
   development sample;
5. reducing variables with SHAP; and
6. selecting an XGBoost candidate using reported validation and holdout AUC.

The original exploratory notebooks are retained outside this repository at
`/Users/amandahw/Documents/GATech/CSE 6242 Data Visualization/Project/DelayLab/Final_code`.
Their execution order and migration plan are recorded in
[`notebooks/README.md`](notebooks/README.md). Do not treat the notebooks as a
fully reproducible pipeline yet: the supplied folder does not contain the
referenced `bts_data/`, `BTS_dict.csv`, `Model/`, or `Report/` inputs.

## Layout

```text
training/
├── configs/       # versioned model and data contracts
├── notebooks/     # notebook migration notes and future cleaned notebooks
├── src/           # reusable feature, training, and evaluation code
├── reports/       # local generated metrics and charts (ignored)
└── requirements.txt
```

## Rebuilding the model safely

1. Create an isolated environment and install `training/requirements.txt`.
2. Place raw and intermediate data beneath `training/data/` (ignored by Git).
3. Recreate a strict chronological split before tuning a replacement model.
4. Use `src/features.py` to fit and serialize WOE maps from the development
   data only; apply the same maps to validation, test, and application inputs.
5. Evaluate a candidate with `src/evaluate.py`, record the selected threshold
   and metrics in `training/reports/`, and promote only a versioned model plus
   its feature artifacts to `model/` and `data/`.

## Deployment contract to fix before the next promotion

The training notebooks convert `CRSDepTime` and `CRSArrTime` to hour-of-day
(0–23); the current app sends HHMM values (for example, `0930`). The notebooks
also evaluate at a 0.30 classification threshold while the application uses
0.50. A new candidate should not be promoted until its application feature
builder and threshold match its evaluated contract.

The app currently substitutes monthly weather medians and a fixed 150 seats
for live requests. That is acceptable only if the replacement model is trained
and evaluated with those same inference-time substitutes, or the application is
upgraded to supply compatible forecast and aircraft data.

## Coverage backlog

**Priority: expand the weather dataset for common airports not currently
supported, beginning with LAX.** The interface is temporarily limited to the
205 airport codes with usable weather records so it does not silently use the
generic weather fallback. Before restoring a broader airport list, collect and
validate weather coverage for the additional origins, regenerate the monthly
weather lookup, retrain or re-evaluate the model using that coverage, and add
an application test for each newly supported airport.
