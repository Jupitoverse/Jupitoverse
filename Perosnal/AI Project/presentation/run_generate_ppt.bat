@echo off
cd /d "%~dp0"
echo Installing python-pptx if needed...
pip install -r requirements.txt -q
echo Generating Phase 1 presentation...
python generate_phase1_presentation.py
if exist "Phase1_Data_Annotation_Platform.pptx" (
    echo.
    echo Done. Open: Phase1_Data_Annotation_Platform.pptx
    start "" "Phase1_Data_Annotation_Platform.pptx"
) else (
    echo Script may have failed. Check errors above.
)
pause
