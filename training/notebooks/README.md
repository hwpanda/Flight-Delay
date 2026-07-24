# Legacy notebook migration

The original notebooks remain in the Georgia Tech project directory until their
raw inputs and outputs are catalogued. Copying them directly would preserve
hard-coded paths and large notebook outputs without making the training process
reproducible.

Use this order when migrating them into this repository as cleaned notebooks:

1. `00_BTS_otp_data_download.ipynb`
2. `01a_prepare_on_time_data.ipynb`
3. `01b_Weather_data_augmentation.zip` (extract its scripts into `src/`)
4. `01c_add_weather_and_aircraft_info_and_split_sample.ipynb`
5. `03_Xgboost_final_model_variable_reduction_SHAP_woe.ipynb`
6. `04a`, `04b`, and `04c` XGBoost grid-search notebooks
7. `05_Xgboost_final_model_selection.ipynb`
8. `06_Xgboost_model_perf_eval.ipynb`

The CatBoost and random-forest notebooks are useful baselines but are not part
of the deployed model lineage. EDA notebooks belong in a future `eda/` folder,
not in the repeatable training path.

Before importing a notebook, replace its `./bts_data`, `./Model`, and
`./Report` paths with paths under `training/`, clear execution outputs, and move
shared logic into `training/src/`.
