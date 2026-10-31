# Add fallback bargaining to the existing Kantamal project

This package adds a **separate Gandak subbasin-prioritization module**. It does not change the streamflow forecasting notebooks or models.

## Windows / VS Code installation

1. Open your existing `kantamal-streamflow-forecasting` folder in VS Code.
2. Extract the ZIP **into that folder**, not into a new nested `gandak_integration` folder. The existing `src/`, `data/`, `results/` and other project folders should remain intact.
3. Open the VS Code terminal and activate your existing environment (if it is not already active):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Make sure pandas and NumPy are installed:

   ```powershell
   python -m pip install pandas numpy
   ```

5. Run the tests:

   ```powershell
   python -m unittest discover -s tests -p "test_fallback_bargaining.py" -v
   ```

6. Try the **illustrative example** (NOT real Gandak data):

   ```powershell
   python -m src.fallback_bargaining --input examples/illustrative_subbasins.csv --output results/example_fallback_ranking.csv
   ```

   Expected: `k = 2`, accepted subbasin `A`.

7. When you receive the real CSV, save it as `data/gandak/gandak_gspi_subbasin.csv`, then run:

   ```powershell
   python -m src.fallback_bargaining --input data/gandak/gandak_gspi_subbasin.csv --output results/gandak_fallback_ranking.csv
   ```

## Optional Git steps (after checking results)

```powershell
git switch -c feature/gandak-fallback-bargaining
git status
git add src/fallback_bargaining.py tests/test_fallback_bargaining.py docs/fallback_bargaining.md data/gandak/README.md examples/illustrative_subbasins.csv INTEGRATION_README.md
git commit -m "Add Gandak fallback bargaining research module"
git push origin HEAD
```

- `git switch -c feature/gandak-fallback-bargaining`: creates and enters a new branch so the main branch is not changed immediately.
- `git status`: shows what changed, so you can review before saving.
- `git add`: selects exactly these new files for the next commit.
- `git commit`: saves a named snapshot of the changes locally.
- `git push origin HEAD`: sends your current branch to GitHub. The commands above create a feature branch first, so this pushes that branch for a reviewable pull request.

**Research note:** Do not present the illustrative data as real observations. The real CSV and scientific definition of `bd34_pct` are still needed for actual Gandak results. Kantamal subbasin prioritization would require its own subbasin indicators.
