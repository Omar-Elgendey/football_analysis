import csv

def export_player_stats(tracks, output_path='output_videos/player_stats.csv'):
    """
    Takes the tracks dictionary and produces a CSV file
    with summary stats for each player.
    """
    # We'll build a dictionary here to hold each player's aggregated stats
    player_data = {}

    # Loop through every frame in tracks["players"]
    # frame_num = the frame index, player_track = dict of players in that frame
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track_info in player_track.items():

            # If this is the first time we see this player, create their entry
            if player_id not in player_data:
                player_data[player_id] = {
                    'team': track_info.get('team', 'N/A'),
                    'total_distance': 0.0,
                    'speed_sum': 0.0,
                    'speed_count': 0,
                    'ball_possession_frames': 0
                }

            # Add this frame's distance to the running total (if it exists)
            if 'distance' in track_info:
                player_data[player_id]['total_distance'] = track_info['distance']

            # Add this frame's speed to compute an average later
            if 'speed' in track_info:
                player_data[player_id]['speed_sum'] += track_info['speed']
                player_data[player_id]['speed_count'] += 1

            # Count frames where this player had the ball
            if track_info.get('has_ball', False):
                player_data[player_id]['ball_possession_frames'] += 1

    # --- Compute averages and write everything to a CSV file ---
    with open(output_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow(['player_id', 'team', 'total_distance_m', 'avg_speed_kmh', 'ball_possession_frames'])

        # Write one row per player
        for player_id, data in player_data.items():
            if data['speed_count'] > 0:
                avg_speed = data['speed_sum'] / data['speed_count']
            else:
                avg_speed = 0.0

            writer.writerow([
                player_id,
                data['team'],
                round(data['total_distance'], 2),
                round(avg_speed, 2),
                data['ball_possession_frames']
            ])

    print(f"Player stats exported to: {output_path}")
    return player_data