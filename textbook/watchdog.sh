#!/bin/bash
# Watchdog: keeps enrich_chapters.py running until complete
cd "C:/Users/RyanBlumenow/Desktop/Ryan/testcanvas/textbook"

LOG="C:/Users/RyanBlumenow/Desktop/Ryan/testcanvas/textbook/.enrichment_log.txt"
PROGRESS="C:/Users/RyanBlumenow/Desktop/Ryan/testcanvas/textbook/.enrichment_progress.json"
TOTAL=3114

while true; do
    # Count completed sections
    DONE=$(python -X utf8 -c "import json; d=json.load(open('$PROGRESS',encoding='utf-8')); print(len(d))" 2>/dev/null || echo 0)

    echo "$(date): $DONE / $TOTAL done — launching enrichment..." >> "$LOG"

    if [ "$DONE" -ge "$TOTAL" ]; then
        echo "$(date): All $TOTAL sections complete. Watchdog exiting." >> "$LOG"
        break
    fi

    # Run enrichment — blocks until it exits (crash, rate limit, or completion)
    python -X utf8 -u enrich_chapters.py >> "$LOG" 2>&1

    EXIT=$?
    DONE_AFTER=$(python -X utf8 -c "import json; d=json.load(open('$PROGRESS',encoding='utf-8')); print(len(d))" 2>/dev/null || echo 0)

    if [ "$DONE_AFTER" -ge "$TOTAL" ]; then
        echo "$(date): Complete after exit (code $EXIT). Done." >> "$LOG"
        break
    fi

    echo "$(date): Exited with code $EXIT at $DONE_AFTER/$TOTAL — restarting in 30s..." >> "$LOG"
    sleep 30
done
