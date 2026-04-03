SignaX data pack

Files:
1. google_trends_regions_clean.csv
   - Cleaned regional Google Trends export
   - Columns:
     region, freelance_interest, delivery_interest, bahr_interest, khamsat_interest, mostaql_interest, source, granularity

2. khamsat_projects_clean.csv
   - Cleaned raw Khamsat project list
   - Columns:
     project_name, category, date, time, source, platform

3. khamsat_daily_summary.csv
   - Daily count of Khamsat projects by category
   - Best file for quick dashboard metrics

4. khamsat_category_summary.csv
   - Total project count by category

5. merged_signals.csv
   - Unified format for direct use in Python/SignaX
   - Columns:
     date, city, source, platform, category, metric_name, metric_value

Recommended project folder:
SignaX/
  data/
    google_trends_regions_clean.csv
    khamsat_projects_clean.csv
    khamsat_daily_summary.csv
    khamsat_category_summary.csv
    merged_signals.csv

Important note:
- Google Trends file is regional (province-level)
- Khamsat file does not include city, so it is stored as city = saudi_general in merged_signals.csv
- If you later add city tags to Khamsat rows, the merged file can drive city-level density more accurately
