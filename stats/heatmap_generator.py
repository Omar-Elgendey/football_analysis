import matplotlib.pyplot as plt
import numpy as np

def generate_player_heatmap(tracks, player_id, output_path='output_videos/heatmap.png'):
    """
    Generates a heatmap showing where a specific player spent most
    of their time on the pitch, based on their transformed (real-world)
    positions across all frames.
    """
    # We'll collect all (x, y) positions of this player here
    x_positions = []
    y_positions = []

    # Loop through every frame and grab this player's position (if they appear)
    for frame_num, player_track in enumerate(tracks['players']):
        if player_id in player_track:
            position = player_track[player_id].get('position_transformed')

            # Some frames might have None if the player was off-screen or not tracked
            if position is not None:  
                x_positions.append(position[0])
                y_positions.append(position[1])

    # If we never found this player, stop here
    if len(x_positions) == 0:
        print(f"No position data found for player {player_id}")
        return

    # --- Draw the heatmap ---
    # Standard football pitch dimensions in meters (length x width)
    pitch_length = 105
    pitch_width = 68

    fig, ax = plt.subplots(figsize=(10.5, 6.8))

    # This is the core heatmap: it builds a 2D histogram of positions
    # and displays it as a color-coded density map
    heatmap = ax.hist2d(
        x_positions,
        y_positions,
        bins=(30, 20),          # how many "cells" to divide the pitch into
        range=[[0, pitch_length], [0, pitch_width]],
        cmap='hot'               # color scheme: black -> red -> yellow (hot = more time spent)
    )

    plt.colorbar(heatmap[3], ax=ax, label='Time spent (relative)')
    ax.set_title(f'Player {player_id} - Heatmap')
    ax.set_xlabel('Pitch Length (m)')
    ax.set_ylabel('Pitch Width (m)')

    plt.savefig(output_path)
    plt.close(fig)

    print(f"Heatmap saved to: {output_path}")

    return x_positions, y_positions
  
  
  
def generate_all_players_heatmap(tracks, output_path='output_videos/heatmap_all_players.png'):
    """
    Generates a heatmap showing where ALL players spent their time
    on the pitch combined. Useful for sanity-checking whether the
    action was concentrated in one area (e.g. short clip) or spread out.
    """
    x_positions = []
    y_positions = []

    # Loop through every frame, and every player in that frame
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track_info in player_track.items():
            position = track_info.get('position_transformed')
            if position is not None:
                x_positions.append(position[0])
                y_positions.append(position[1])

    if len(x_positions) == 0:
        print("No position data found for any player")
        return

    pitch_length = 105
    pitch_width = 68

    fig, ax = plt.subplots(figsize=(10.5, 6.8))

    heatmap = ax.hist2d(
        x_positions,
        y_positions,
        bins=(30, 20),
        range=[[0, pitch_length], [0, pitch_width]],
        cmap='hot'
    )

    plt.colorbar(heatmap[3], ax=ax, label='Time spent (relative)')
    ax.set_title('All Players - Combined Heatmap')
    ax.set_xlabel('Pitch Length (m)')
    ax.set_ylabel('Pitch Width (m)')

    plt.savefig(output_path)
    plt.close(fig)

    print(f"Combined heatmap saved to: {output_path}")