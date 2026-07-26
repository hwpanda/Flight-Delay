# Flight Delay App — Project Handoff

## Purpose

This is a small web app that estimates whether a scheduled U.S. flight is
likely to arrive at least 15 minutes late. A user supplies a date, scheduled
times, airline, origin, and destination; the app returns a delay probability
and displays the route on a map.

The immediate goal is a dependable demonstration of the trained XGBoost model.
The longer-term goal is a prediction product whose inputs, model evaluation,
and user-facing claims are aligned and reproducible.

## Current state

- The Flask app starts from `app.py`, serves `GET /api/options` for UI data,
  and serves `POST /api/predict` for forecasts.
- The browser interface is a Vite + React + TypeScript app in `frontend/`.
  `npm run build` writes generated assets to `static/react/`; Flask serves a
  minimal shell from `templates/index.html`.
- `model/xgb_final_model_26.pkl` is the deployed 17-feature XGBoost binary
  classifier.
- Static data in `data/` supplies airport coordinates, 15 airline codes,
  WOE maps, and origin/month weather medians.
- The browser form offers only the **205 airport codes with usable weather
  records**. Both client and server enforce that restriction.
- `LAX` is intentionally unavailable for now because it lacks usable weather
  coverage in the supplied lookup data.
- The route map uses Leaflet/OpenStreetMap. The UI and API were smoke-tested
  using a supported ATL → BOS request; an unsupported LAX request is rejected.
- `training/` contains a versioned scaffold for future data preparation,
  feature engineering, evaluation, and model promotion.

## Important project locations

| Location | Role |
| --- | --- |
| `app.py` | Request validation, feature assembly, model response |
| `services/` | Model, airport/airline, weather, and WOE lookup services |
| `frontend/` | React + TypeScript form, API client, map, results UI, and build tooling |
| `templates/index.html` | Minimal Flask document that loads the compiled React bundle |
| `static/react/` | Generated React build assets (not committed; rebuild locally or in Docker) |
| `model/` | Deployed model artifacts |
| `data/` | Runtime lookup data |
| `training/README.md` | Reproducible-training plan and weather-coverage backlog |
| `training/configs/xgb_final_26.yaml` | Recorded model feature contract and legacy context |

## What the model uses today

The served model expects these features:

- calendar and schedule: year, quarter, month, day, weekday, departure time,
  arrival time, scheduled elapsed time;
- route: great-circle distance;
- origin weather: temperature, dew point, sea-level pressure, precipitation;
- aircraft: number of seats;
- categorical history: WOE values for airline, origin, and destination.

At application time, the weather values are historical monthly medians, seats
are fixed at 150, and unknown WOE values use a global fallback. These choices
make the app run without live external data but limit prediction fidelity.

## Priority roadmap

### 1. Align training and inference before promoting another model

This is the most important technical task.

- The legacy training notebooks convert `CRSDepTime` and `CRSArrTime` to an
  hour from 0–23, while the app currently sends HHMM values such as `0930`.
- The notebooks evaluate their final model at a 0.30 delay threshold, while the
  app displays “delayed” only above 0.50.
- Decide the desired feature representation and threshold from evaluation data,
  make the training and app implementations identical, then add automated
  contract tests before replacing the model.

### 2. Expand weather coverage, starting with LAX

The current airport restriction prevents generic weather fallbacks from being
silently used. To add an airport:

1. obtain and validate the source weather records;
2. generate complete origin/month lookup rows;
3. rerun or re-evaluate model training with the expanded coverage;
4. add the airport to a regression test; and
5. confirm it appears in the app’s supported-airport list.

Prioritize LAX, then other common origin airports missing from the 205-code
subset. Do not simply loosen the UI restriction without validating the model
inputs.

### 3. Make model training reproducible

The original training notebooks are at:

`/Users/amandahw/Documents/GATech/CSE 6242 Data Visualization/Project/DelayLab/Final_code`

They cover BTS download, weather and aircraft augmentation, WOE encoding, SHAP
feature reduction, XGBoost tuning, selection, and evaluation. They reference
data and report paths that are not included in this repository, so they cannot
currently be rerun end to end. Migrate shared notebook code into `training/src/`
and document external data acquisition rather than committing raw datasets.

### 4. Improve prediction quality and trust

- Record validation, test, calibration, precision, recall, F1, and AUC for
  every candidate model.
- Use a strictly chronological validation/test design. The legacy “OOT” sample
  is 2025 May–July, while its training set includes later 2025 months.
- Serialize the WOE maps, global fallback, feature list, and decision threshold
  with each promoted model.
- Consider a model-version and “data coverage” label in the UI so users know
  the prediction’s limitations.

### 5. Product improvements after model correctness

- Show the selected origin/destination names alongside their codes.
- Explain that the result is a probability, not a guarantee.
- Add an accessible feature/details panel only if it is useful to users; the
  README currently mentions a feature table but the page does not render one.
- Add basic automated API and browser tests to protect airport validation and
  model feature construction.

## Research questions

| Question | Why it matters |
| --- | --- |
| What weather source can reliably cover LAX and other missing airports? | Determines whether coverage can expand without generic defaults. |
| Is historic monthly-median weather appropriate for a pre-flight prediction? | It is stable and simple but misses the day’s actual or forecast conditions. |
| Which decision threshold fits the intended user action? | A 0.30 threshold favors catching more delays; 0.50 is more conservative. |
| Can aircraft seats be obtained from the submitted flight instead of fixed at 150? | The current value may misrepresent the training feature. |
| How well calibrated is the probability? | A 70% displayed probability should correspond to roughly 70% observed delays. |
| What is the cost of false positives versus false negatives? | It should guide the chosen threshold and user messaging. |

## Key trade-offs

| Decision | Benefit | Cost |
| --- | --- | --- |
| Restrict to 205 weather-covered airports | Prevents silent generic-weather inputs | Excludes common airports such as LAX for now |
| Use historical weather medians | No live weather API, simple and reproducible | Less flight-specific than forecasts or observations |
| Use WOE fallback for unknown categories | Model can return a result | Prediction is less tailored for unseen airports/airlines |
| Keep model/data artifacts in Git | Easy local deployment and review | Repository size grows; use Git LFS if future artifacts approach GitHub limits |
| Migrate notebooks into modules | Repeatable, testable workflow | Initial refactoring effort and data-source documentation required |

## Suggested working cadence

Do **not** rewrite this document every day. Update it when one of these occurs:

- a model, training data source, feature contract, threshold, or coverage set
  changes;
- a meaningful UI/API behavior changes;
- a new decision, limitation, or research result affects the roadmap; or
- before handing the project to another person or pausing work for a while.

A short review at the end of a substantial work session is enough. Keep the
document concise: mark completed items, update the next one or two priorities,
and record any decision that would otherwise be rediscovered later.

## Handoff checklist for the next contributor

1. Read this file and `training/README.md`.
2. Build the UI with `cd frontend && npm install && npm run build`, then run
   the app locally with `./venv/bin/python app.py`.
3. Confirm a supported airport route produces a prediction and an unsupported
   airport is rejected.
4. Before changing the model, inspect the feature contract in
   `training/configs/xgb_final_26.yaml`.
5. Keep raw data and generated reports under ignored `training/` directories.
6. Commit focused changes with their test evidence and update this file only
   when the project state or roadmap materially changes.
