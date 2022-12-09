class Match:
  def __init__ (self, play_stage = 'G', play_date ='0000-00-00',
  audience = 0, stadium_id = 0, referee_id = 0, asst_ref1_id = 0, asst_ref2_id = 0, four_off_ref_id = 0):
    self.play_stage = play_stage
    self.play_date = play_date
    self.audience = audience
    self.stadium_id = stadium_id
    self.referee_id = referee_id
    self.asst_ref1_id = asst_ref1_id
    self.asst_ref2_id = asst_ref2_id
    self.four_off_ref_id = four_off_ref_id

class Match_team:
  def __init__ (self, match_no = 0, team_id = 0,opponent_id = 0, result = 'D', goals = 0, shots = 0, shots_on_target = 0, penalty_shootout = 'N', penalty_score = 0):
    self.match_no = match_no
    self.team_id = team_id
    self.opponent_id = opponent_id
    self.result = result
    self.goals = goals
    self.shots = shots
    self.shots_on_target = shots_on_target
    self.penalty_shootout = penalty_shootout
    self.penalty_score = penalty_score

class Player_match:
  def __init__ (self,match_no = 0,team_id = 0, player_id = 0, player_status = 'S'):
    self.match_no = match_no
    self.team_id = team_id
    self.player_id = player_id
    self.player_status = player_status

class Player_in_out:
  def __init__ (self,match_no = 0, team_id =0, player_id = 0, in_out = 'I', in_out_time = 0, game_schedule = 'NT',game_half = '1'):
    self.match_no = match_no
    self.team_id = team_id
    self.player_id = player_id
    self.in_out = in_out
    self.in_out_time = in_out_time
    self.game_schedule = game_schedule
    self.game_half = game_half

class Player_card:
  def __init__ (self,match_no = 0, team_id =0, player_id = 0, card_time = 0,sent_off = 'N',game_schedule = 'NT', game_half = '1'):
    self.match_no = match_no
    self.team_id = team_id
    self.player_id = player_id
    self.card_time = card_time
    self.sent_off = sent_off
    self.game_schedule = game_schedule
    self.game_half = game_half

class Player_cap:
  def __init__ (self, match_no = 0, team_id = 0, player_id = 0):
    self.match_no = match_no
    self.team_id = team_id
    self.player_id = player_id

class Goal:
  def __init__ (self, match_no = 0, player_id = 0, team_id = 0, goal_type = 'N', goal_time = 0, game_schedule = 'NT', game_half = '1'):
    self.match_no = match_no
    self.player_id = player_id
    self.team_id = team_id
    self.goal_type = goal_type
    self.goal_time = goal_time
    self.game_schedule = game_schedule
    self.game_half = game_half

if __name__ == '__main__':
  a = Match()
  values = 'NULL,' + ','.join(str(x) for x in vars(a).values())
  print(values)