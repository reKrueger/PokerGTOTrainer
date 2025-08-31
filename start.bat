@echo off
title Poker GTO Trainer - Position Training Mode
echo ===============================================
echo   POKER GTO TRAINER - POSITION TRAINING MODE
echo ===============================================
echo.
echo Features:
echo   * Tisch wird bei JEDER Hand neu gezeichnet
echo   * Deine Position ist IMMER rot markiert
echo   * Grosse NEUE HAND Button
echo   * Sofortiges Position-Feedback
echo   * Optimiert fuer Position-Training
echo.
echo Starting Position Training App...
echo.
echo The app will be available at:
echo   http://localhost:8501
echo.
echo ANLEITUNG:
echo   1. Klicke "NEUE HAND" Button
echo   2. Siehe deine ROTE Position am Tisch
echo   3. Schaue deine Karten an  
echo   4. Waehle deine Aktion
echo   5. Lerne aus GTO-Feedback
echo.
echo Press Ctrl+C to stop the server
echo ===============================================
echo.

REM Change to project directory
cd /d "%~dp0"

REM Start position trainer (updated version)
streamlit run streamlit_position_trainer.py --server.headless=true --browser.gatherUsageStats=false --server.port=8501

pause
