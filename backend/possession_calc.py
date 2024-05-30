class PossessionCalculator:
    def __init__(self):
        self.current_possessing_team = None
        self.team1_possession = 50
        self.team2_possession = 50

    def update_possession(self, possession_team):
        if possession_team == self.current_possessing_team:
            if possession_team == 'Team 1':
                self.team1_possession += 1
            elif possession_team == 'Team 2':
                self.team2_possession += 1
        else:
            self.current_possessing_team = possession_team

    def get_possession_stats(self, total_frames):
        team1_percentage = (self.team1_possession / total_frames) * 100
        team2_percentage = (self.team2_possession / total_frames) * 100
        return team1_percentage, team2_percentage
