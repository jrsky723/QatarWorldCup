import vo
from dao_db import Dao

class Team:
  def __init__(self,dao:Dao, country_name:str):
    self.dao = dao
    self.country_name = country_name
    self.team_id = self.dao.team_id_by_country(country_name)
    self.match_no = 0
    self.opponent_id = 0
    self.player_status = ['E' for _ in range(27)]
    self.player_num = self.dao.get_count('Player', {'team_id' : str(self.team_id)})
    self.cap = 0
    self.result = 'D'
    self.goals = 0
    self.opponent_goals = 0
    self.shots = 0
    self.shots_on_target = 0
    self.penalty_shootout = 'N'
    self.penalty_score = 0
    self.group_position = 0

  def inputTeam(self, match_no, opponent_id):
    self.match_no, self.opponent_id = match_no, opponent_id
    print(f'==== [{self.country_name}] ====')
    # starting players
    s = input(f'Starting players list\n').split()
    for n in s : self.player_status[int(n)] = 'S'
    # bench players
    s = input(f'Bench players list\n').split()
    for n in s : self.player_status[int(n)] = 'B'
    for i in range(1, self.player_num + 1):
      PM = vo.Player_match(match_no = match_no,team_id =self.team_id,player_status= self.player_status[i])
      PM.player_id = self.dao.select_by_val('Player',{'team_id' : self.team_id, 'number' : i})[0][0]
      self.dao.insert_no_id(PM)

    self.cap = input(f'Captain Player: ')
    C  = vo.Player_cap(match_no=self.match_no,team_id=self.team_id)
    C.player_id = self.dao.select_by_val('Player', {'team_id' : self.team_id, 'number' : self.cap})[0][0]
    self.dao.insert_no_id(C)
    
  def inputShots(self):
    print(f'Shots by [{self.country_name}]')
    self.shots = input('Total Shots: ')
    self.shots_on_target = input('Total Shots on target: ')

  def updateGroupPosition(self):
    print(f'Group position by [{self.country_name}]')
    self.group_position = input('Group Position after Game: ')
    self.dao.update_by_val('Team',{'group_position' : self.group_position}, {'team_id' : self.team_id})


  def updateTeam(self):
    self.dao.update_by_val('Team',{'match_played' : 'match_played + 1'}, {'team_id' : self.team_id})
    if self.result == 'W':
      self.dao.update_by_val('Team',{'won' : 'won + 1'}, {'team_id' : self.team_id})
    elif self.result == 'D':
      self.dao.update_by_val('Team',{'draw' : 'draw + 1'}, {'team_id' : self.team_id})
    else:
      self.dao.update_by_val('Team',{'lost' : 'lost + 1'}, {'team_id' : self.team_id})
    self.dao.update_by_val('Team',{'goal_for' : f'goal_for + {self.goals}', 'goal_agnst':f'goal_agnst + {self.opponent_goals}', 'goal_diff' : 'goal_for - goal_agnst'},{'team_id' : self.team_id})
    
  def insertMatchTeam(self):
    MT = vo.Match_team(self.match_no, self.team_id,self.opponent_id,self.result,self.goals,self.shots,self.shots_on_target,self.penalty_shootout,self.penalty_score)
    self.dao.insert_no_id(MT)



class Service:
  def __init__(self):
    self.dao = Dao()

  def inputMatchMask(self):
    M = vo.Match()
    M.play_stage = input('(G : Group | R : Round of 16 | Q : Quarter final | S : Semi Final | F : Final)\nStage : ')
    M.play_date = input('Match Date(YYYY-MM-DD hh:mm:ss) : ')
    M.audience = input('Audience: ')
    s = input('Stadium: ')
    M.stadium_id = self.dao.select_by_val('Stadium',{'stadium_name' : f'"{s}"'})[0][0]
    s = input('Referee: ')
    M.referee_id = self.dao.select_by_val('Referee',{'referee_name' : f'"{s}"'})[0][0]
    s = input('Assistant Referees 1: ')
    M.asst_ref1_id =  self.dao.select_by_val('Asst_ref',{'asst_ref_name' : f'"{s}"'})[0][0]
    s = input('Assistant Referees 2: ')
    M.asst_ref2_id =  self.dao.select_by_val('Asst_ref',{'asst_ref_name' : f'"{s}"'})[0][0]
    s = input('Four Off Referee: ')
    M.four_off_ref_id = self.dao.select_by_val('Referee',{'referee_name' : f'"{s}"'})[0][0]
    self.dao.insert_by_id(M)
    return M

  def inputGoal(self,match_no,game_schedule, game_half):
    G = vo.Goal(match_no=match_no, game_schedule=game_schedule, game_half=game_half)
    goal_info = input('Goal Time | Country | Player Number | Goal Type(N, O, P)\n').split(', ')
    G.goal_time = int(goal_info[0])
    G.team_id = self.dao.team_id_by_country(goal_info[1])
    G.player_id = self.dao.select_by_val('Player',{'team_id' : G.team_id, 'number' : goal_info[2]})[0][0]
    G.goal_type = goal_info[3]
    self.dao.insert_by_id(G)

  def inputCard(self,match_no,game_schedule,game_half):
    C = vo.Player_card(match_no=match_no, game_schedule=game_schedule,game_half=game_half)
    card_info = input('Card Time | Country | Player Number | Card Color (Y/R)\n').split(', ')
    C.card_time = int(card_info[0])
    C.team_id = self.dao.team_id_by_country(card_info[1])
    C.player_id = self.dao.select_by_val('Player',{'team_id' : C.team_id, 'number' : card_info[2]})[0][0]
    if card_info[3] == 'R': C.sent_off = 'Y'
    self.dao.insert_no_id(C)

  def inputInOut(self,match_no, game_schedule, game_half):
    I = vo.Player_in_out(match_no=match_no,game_schedule=game_schedule,game_half=game_half,in_out='I')
    O = vo.Player_in_out(match_no=match_no,game_schedule=game_schedule,game_half=game_half,in_out='O')
    in_out_info = input('In Out Time | Country | IN Number | OUT Number\n').split(', ')
    I.in_out_time = O.in_out_time = int(in_out_info[0])
    I.team_id = O.team_id = self.dao.team_id_by_country(in_out_info[1])
    I.player_id = self.dao.select_by_val('Player',{'team_id' : I.team_id, 'number' : in_out_info[2]})[0][0]
    O.player_id = self.dao.select_by_val('Player',{'team_id' : O.team_id, 'number' : in_out_info[3]})[0][0]
    self.dao.insert_no_id(I)
    self.dao.insert_no_id(O)
  
  def inputEvent(self,match_no, game_schedule, game_half):
    while True:
      print('Input Event(1.Goal, 2.Card, 3.In_Out, 4.End Session)')
      event = input()
      if event == '1':
        self.inputGoal(match_no,game_schedule,game_half)
      elif event == '2':
        self.inputCard(match_no,game_schedule,game_half)
      elif event == '3':
        self.inputInOut(match_no,game_schedule,game_half)
      elif event == '4': break
      else: print('Wrong Event. Please Write Again')
  
  def judgeGame(self,a_score, b_score):
    if a_score > b_score: return 'W'
    elif a_score < b_score: return 'L'
    else: return 'D'

  def getResult(self,match_no:int, a:Team, b:Team):
    a.goals = self.dao.get_count('Goal', {'match_no' : match_no,'team_id' : a.team_id})
    b.goals = self.dao.get_count('Goal', {'match_no' : match_no,'team_id' : b.team_id})
    a.opponent_goals = b.goals 
    b.opponent_goals = a.goals
    if a.penalty_shootout == 'N':
      a.result = self.judgeGame(a.goals, b.goals)
      b.result = self.judgeGame(b.goals, a.goals)
    else:
      a.result = self.judgeGame(a.penalty_score, b.penalty_score)
      b.result = self.judgeGame(b.penalty_score, a.penalty_score)

  # Services
  def inputMatchInfo(self):
    print('==== Insert Match Info ====')
    M = self.inputMatchMask()
    match_no = self.dao.get_count('Match')
    print('Country A  vs Country B')
    a, b = Team(self.dao, input("A: ")), Team(self.dao, input("B: "))
    a.inputTeam(match_no, b.team_id)
    b.inputTeam(match_no, a.team_id)
    print('==== Game Info ====')
    print('== First Half ==')
    print('Play Session : Nomal Time')
    self.inputEvent(match_no,'NT','1')
    print('Play Session : Stoppage Time')
    self.inputEvent(match_no,'ST','1')
    print('== Second Half ==')
    print('Play Session : Nomal Time')
    self.inputEvent(match_no,'NT','2')
    print('Play Session : Stoppage Time')
    self.inputEvent(match_no,'ST','2')
    ET = input('Extra Time (Y/N): ')
    if ET == 'Y': 
      print('Play Session : Extra Time')
      print('== First Half ==')
      self.inputEvent(match_no,'ET','1')
      print('== Second Half ==')
      self.inputEvent(match_no,'ET','2') 
      PT = input('Penalty Shootout (Y/N): ')
      if PT == 'Y':
        a.penalty_shootout = b.penalty_shootout = 'Y'
        a.penalty_score = input(f'{a.country_name} : Penalty Score')
        b.penalty_score = input(f'{b.country_name} : Penalty Score')
    print('== Game End ==')
    self.getResult(match_no, a, b)
    a.inputShots()
    b.inputShots()
    a.insertMatchTeam()
    b.insertMatchTeam()
    a.updateTeam()
    b.updateTeam()
    if M.play_stage == 'G':
      a.updateGroupPosition()
      b.updateGroupPosition()
    print('==== Insert Match Infromation Complete!!! ====')

if __name__ =='__main__':
  service = Service()
  service.inputMatchInfo()
