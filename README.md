# Football Match Analysis

An end-to-end computer vision pipeline that analyzes football match footage: detecting and tracking players, referees, and the ball, assigning players to teams, estimating speed and distance covered, and calculating ball possession — with additional data-analysis and visualization features layered on top.

> **Note:** My background is in NLP, not Computer Vision. I cloned this project to learn how a CV pipeline is structured end-to-end, and extended it with the statistics and visualization features described below.

## Demo Output

The pipeline outputs an annotated video showing:
- Bounding ellipses around players and referees, color-coded by team
- A triangle marker above the ball
- Live ball possession percentage per team
- Speed (km/h) and distance covered (m) displayed above each player

## Architecture / Pipeline

The project follows a sequential pipeline, orchestrated in `main.py`:

```
Input Video (.mp4)
      │
      ▼
┌─────────────────────────┐
│ 1. Detection & Tracking │  trackers/tracker.py
│   YOLO + ByteTrack       │  → detects players, referees, ball
│                          │  → assigns persistent IDs across frames
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 2. Camera Movement       │  camera_movement_estimator/
│    Compensation          │  → uses Optical Flow to detect camera
│                          │    pan/movement and adjusts player
│                          │    positions accordingly
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 3. View Transformation   │  view_transformer/
│   Pixel → real-world (m) │  → perspective transform: converts
│                          │    pixel coordinates into real pitch
│                          │    coordinates (105m x 68m)
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 4. Speed & Distance      │  speed_and_distance_estimator/
│    Estimation             │  → computes each player's speed (km/h)
│                          │    and cumulative distance covered (m)
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 5. Team Assignment       │  team_assigner/
│   KMeans color clustering │  → clusters jersey colors to assign
│                          │    each player to Team 1 or Team 2
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 6. Ball Possession       │  player_ball_assigner/
│   Nearest-player logic   │  → determines which player has the
│                          │    ball based on proximity
└─────────────────────────┘
      │
      ▼
┌──────────────────────────────────────┐
│ 7. Output Generation                 │
│   ├─ Annotated video (tracker.py)    │  → output_videos/output_video.avi
│   ├─ Player stats CSV (added)        │  → output_videos/player_stats.csv
│   └─ Player heatmaps (added)         │  → output_videos/heatmap*.png
└──────────────────────────────────────┘
```

## Features I Added

The original cloned repository produced only the annotated output video. I extended it with the following features:

### 1. Player Statistics Export (`stats/stats_exporter.py`)
Aggregates the per-frame tracking data into per-player summary statistics and exports them to a CSV file:
- Total distance covered (m)
- Average speed (km/h)
- Number of frames in ball possession

Output: `output_videos/player_stats.csv`

### 2. Player Heatmaps (`stats/heatmap_generator.py`)
Uses each player's real-world (transformed) position across all frames to generate a 2D density heatmap showing where on the pitch they spent most of their time. Available for:
- A single player (`generate_player_heatmap`)
- All players combined (`generate_all_players_heatmap`)

Output: `output_videos/heatmap.png`, `output_videos/heatmap_all_players.png`

Built using `matplotlib.pyplot.hist2d`.

## Tech Stack

| Component | Technology |
|---|---|
| Object Detection | YOLO (Ultralytics) |
| Multi-object Tracking | ByteTrack (via `supervision`) |
| Team Classification | K-Means Clustering (scikit-learn) |
| Camera Motion Estimation | Optical Flow (OpenCV) |
| Perspective Transform | OpenCV |
| Data Processing | pandas, NumPy |
| Visualization | Matplotlib, OpenCV |

## Project Structure

```
football_analysis/
├── main.py                          # Pipeline entry point
├── trackers/                        # YOLO detection + ByteTrack tracking
├── team_assigner/                   # KMeans-based team color classification
├── camera_movement_estimator/       # Optical flow camera compensation
├── view_transformer/                # Pixel-to-meter perspective transform
├── speed_and_distance_estimator/    # Speed/distance calculation
├── player_ball_assigner/            # Ball possession logic
├── stats/                           # Added: CSV export + heatmap generation
│   ├── stats_exporter.py
│   └── heatmap_generator.py
├── utils/                           # Shared helper functions
├── models/                          # Trained YOLO weights (best.pt)
├── input_videos/                    # Source footage
├── output_videos/                   # Generated video, CSV, and heatmap outputs
└── stubs/                           # Cached tracking results (for faster re-runs)
```

## Setup & Usage

1. Create a virtual environment and install dependencies:
```bash
pip install ultralytics supervision opencv-python pandas numpy matplotlib
```

2. Place a trained YOLO model at `models/best.pt` and a source video in `input_videos/`.

3. Run the pipeline:
```bash
python main.py
```

4. Outputs will be generated in `output_videos/`:
   - `output_video.avi` — annotated video
   - `player_stats.csv` — per-player statistics
   - `heatmap.png`, `heatmap_all_players.png` — positional heatmaps

## Future Improvements

- **Pass Accuracy Tracking** — estimate completed vs. failed passes based on ball possession transitions between players (in progress; intentionally left as a future iteration to keep the current feature set well-understood and reliable)
- Support for exporting a short automated text summary of the match statistics
- Team formation snapshot visualization

## Credits

Base pipeline structure adapted from an open-source football analysis tutorial project. Statistics export and heatmap visualization features were added independently.