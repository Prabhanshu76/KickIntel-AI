import configparser

config_file = "config.ini"
config = configparser.ConfigParser()
config.read(config_file)

class PassTracker:
    def __init__(self):
        self.possession_team = None
        self.last_possession_team = None
        self.last_team1_possession_track_id = None
        self.last_team2_possession_track_id = None
        self.team1_passes = 0
        self.team2_passes = 0
        self.frames_with_team1_possession = 0  # Counter for frames with Team 1 possession
        self.frames_with_team2_possession = 0  # Counter for frames with Team 2 possession
        self.min_frames = int(config['MINIMUMFRAMES']['min_frames'])  # Minimum frames required for a pass

    def update_pass(self, possession_team, player_in_possession_track_id):
        if possession_team != self.last_possession_team:
            self.last_possession_team = possession_team
            self.frames_with_team1_possession = 0  # Reset the frame counter when possession changes for Team 1
            self.frames_with_team2_possession = 0  # Reset the frame counter when possession changes for Team 2

        if possession_team == 'Team 1':
            if (
                player_in_possession_track_id is not None
                and player_in_possession_track_id != self.last_team1_possession_track_id
                and self.last_possession_team == 'Team 1'
            ):
                if self.frames_with_team1_possession > self.min_frames:  # Use the class attribute for the threshold
                    self.team1_passes += 1
                self.last_team1_possession_track_id = player_in_possession_track_id

            self.frames_with_team1_possession += 1  # Increment the frame counter for Team 1

        elif possession_team == 'Team 2':
            if (
                player_in_possession_track_id is not None
                and player_in_possession_track_id != self.last_team2_possession_track_id
                and self.last_possession_team == 'Team 2'
            ):
                if self.frames_with_team2_possession > self.min_frames:  # Use the class attribute for the threshold
                    self.team2_passes += 1
                self.last_team2_possession_track_id = player_in_possession_track_id

            self.frames_with_team2_possession += 1  # Increment the frame counter for Team 2

    def get_passes(self):
        return self.team1_passes, self.team2_passes

    def reset(self):
        self.possession_team = None
        self.last_possession_team = None
        self.last_team1_possession_track_id = None
        self.last_team2_possession_track_id = None
        self.team1_passes = 0
        self.team2_passes = 0
        self.frames_with_team1_possession = 0  # Reset frame counter for Team 1 on reset
        self.frames_with_team2_possession = 0  # Reset frame counter for Team 2 on reset








# class PassTracker:
#     def __init__(self):
#         self.possession_team = None
#         self.last_possession_team = None
#         self.last_team1_possession_track_id = None
#         self.last_team2_possession_track_id = None
#         self.team1_passes = 0
#         self.team2_passes = 0

#     def update_pass(self, possession_team, player_in_possession_track_id):
#         if possession_team != self.last_possession_team:
#             self.last_possession_team = possession_team

#         if possession_team == 'Team 1':
#             if (
#                 player_in_possession_track_id is not None
#                 and player_in_possession_track_id != self.last_team1_possession_track_id
#                 and self.last_possession_team == 'Team 1'
#             ):
#                 self.team1_passes += 1
#                 self.last_team1_possession_track_id = player_in_possession_track_id

#         elif possession_team == 'Team 2':
#             if (
#                 player_in_possession_track_id is not None
#                 and player_in_possession_track_id != self.last_team2_possession_track_id
#                 and self.last_possession_team == 'Team 2'
#             ):
#                 self.team2_passes += 1
#                 self.last_team2_possession_track_id = player_in_possession_track_id

#     def get_passes(self):
#         return self.team1_passes, self.team2_passes

#     def reset(self):
#         self.possession_team = None
#         self.last_possession_team = None
#         self.last_team1_possession_track_id = None
#         self.last_team2_possession_track_id = None
#         self.team1_passes = 0
#         self.team2_passes = 0
        
