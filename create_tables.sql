-- Active: 1670163483948@@127.0.0.1@3306@mydata

CREATE TABLE `Country` (
  `country_code` char(3) NOT NULL PRIMARY KEY,
  `country_name` varchar(40) NOT NULL
);
CREATE TABLE `Team` (
  `team_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `team_group` CHAR(1) NOT NULL,
  `country_code` CHAR(3) NOT NULL,
  `match_played` INT NOT NULL,
  `won` INT NOT NULL,
  `draw` INT NOT NULL,
  `lost` INT NOT NULL,
  `goal_for` INT NOT NULL,
  `goal_agnst` INT NOt NULL,
  `goal_diff` INT NOT NULL,
  `group_position` INT NOT NULL,
  FOREIGN KEY (`country_code`) REFERENCES `Country`(`country_code`)
);

CREATE TABLE `Position` (
  `position_code` char(2) NOT NULL PRIMARY KEY,
  `position_desc` varchar(10) NOT NULL
);

ALTER TABLE player AUTO_INCREMENT = 1001; 

CREATE TABLE `Player` (
  `player_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `team_id` INT NOT NULL,
  `number` INT NOT NULL,
  `position` char(2) NOT NULL,
  `player_name` varchar(40) NOT NULL,
  `first_name` varchar(40) NOT NULL,
  `last_name` varchar(40) NOT NULL,
  `name_on_shirt` varchar(20) NOT NULL,
  `DOB` datetime NOT NULL,
  `club` varchar(40) NOT NULL,
  `height` INT NOT NULL,
  `caps` INT NOT NULL,
  `goals` INT NOT NULL,
  FOREIGN KEY (`team_id`) REFERENCES `Team` (`team_id`),
  FOREIGN KEY (`position`) REFERENCES `Position` (`position_code`)
);

ALTER TABLE Coach AUTO_INCREMENT = 2001; 
CREATE TABLE `Coach` (
  `coach_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `team_id` INT NOT NULL,
  `coach_role` VARCHAR(20) NOT NULL,
  `coach_name` VARCHAR(40) NOT NULL,
  `first_name` VARCHAR(40) NOT NULL,
  `last_name` VARCHAR(40) NOT NULL,
  `nationality` CHAR(3) NOT NULL,
  FOREIGN KEY (`nationality`) REFERENCES `Country`(`country_code`),
  FOREIGN KEY (`team_id`) REFERENCES `Team`(`team_id`)
);

ALTER TABLE Referee AUTO_INCREMENT = 3001;
CREATE TABLE `Referee` (
  `referee_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `referee_name` VARCHAR(40) NOT NULL
);

ALTER TABLE asst_ref AUTO_INCREMENT = 4001;
CREATE TABLE `Asst_ref` (
  `asst_ref_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `asst_ref_name` VARCHAR(40) NOT NULL
);

CREATE TABLE `Stadium` (
  `stadium_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `stadium_name` VARCHAR(40) NOT NULL,
  `city` VARCHAR(20) NOT NULL,
  `capacity` INT NOT NULL 
);

-- after game

CREATE TABLE `Match` (
  `match_no` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `play_stage` CHAR(1) NOt NULL,
  `play_date` DATETIME NOt NULL,
  `audience` INT NOT NULL,
  `stadium_id` INT NOT NULL,
  `referee_id` INT NOT NULL,
  `asst_ref1_id` INT NOT NULL,
  `asst_ref2_id` INT NOT NULL,
  `four_off_ref_id` INT NOT NULL,
  `penalty_shootout` CHAR(1),
  FOREIGN KEY (`stadium_id`) REFERENCES `Stadium` (`stadium_id`),
  FOREIGN KEY (`referee_id`) REFERENCES `Referee` (`referee_id`),
  FOREIGN KEY (`asst_ref1_id`) REFERENCES `Asst_Ref` (`asst_ref_id`),
  FOREIGN KEY (`asst_ref2_id`) REFERENCES `Asst_Ref` (`asst_ref_id`),
  FOREIGN KEY (`four_off_ref_id`) REFERENCES `Referee` (`referee_id`)
);

CREATE TABLE `Match_team` (
  `match_no` INT NOT NULL,
  `team_id` INT NOT NULL,
  `result` CHAR(1),
  `goals` INT NOT NULL,
  `shots` INT NOT NULL,
  `shots_on_target` INT NOT NULL,
  PRIMARY KEY (`match_no`,`team_id`),
  FOREIGN KEY (`match_no`) REFERENCES `Match`(`match_no`),
  FOREIGN KEY (`team_id`) REFERENCES `Team`(`team_id`)
);

CREATE TABLE `Player_starting` (
  `match_no` INT NOT NULL,
  `team_id` INT NOT NULL, 
  `player_id` INT NOT NULL,
  PRIMARY KEY (`match_no`,`player_id`),
  FOREIGN KEY (`match_no`) REFERENCES `Match` (`match_no`),
  FOREIGN KEY (`team_id`) REFERENCES `Team` (`team_id`),
  FOREIGN KEY (`player_id`) REFERENCES `Player` (`player_id`)
);
CREATE TABLE `Player_bench` (
  `match_no` INT NOT NULL,
  `team_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  PRIMARY KEY (`match_no`,`player_id`),
  FOREIGN KEY (`match_no`) REFERENCES `Match` (`match_no`),
  FOREIGN KEY (`team_id`) REFERENCES `Team` (`team_id`),
  FOREIGN KEY (`player_id`) REFERENCES `Player` (`player_id`)
);
CREATE TABLE `Player_in_out` (
  `match_no` INT NOT NULL,
  `team_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `in_out` CHAR(1) NOT NULL,
  `in_out_time` INT NOT NULL,
  `in_out_schedule` CHAR(2) NOT NULL,
  `in_out_half` CHAR(1) NOT NULL,
  PRIMARY KEY (`match_no`,`player_id`),
  FOREIGN KEY (`match_no`) REFERENCES `Match` (`match_no`),
  FOREIGN KEY (`team_id`) REFERENCES `Team` (`team_id`),
  FOREIGN KEY (`player_id`) REFERENCES `Player` (`player_id`)
);
CREATE TABLE `Player_card` (
  `match_no` INT NOT NULL,
  `team_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `card_color` CHAR(1) NOT NULL,
  `card_time` INT NOT NULL,
  `card_schedule` CHAR(2) NOT NULL,
  `card_half` cHAR(1),
  PRIMARY KEY (`match_no`,`player_id`,`card_color`),
  FOREIGN KEY (`match_no`) REFERENCES `Match` (`match_no`),
  FOREIGN KEY (`team_id`) REFERENCES `Team` (`team_id`),
  FOREIGN KEY (`player_id`) REFERENCES `Player` (`player_id`)
);
CREATE TABLE `Player_cap` (
  `match_no` INT NOT NULL,
  `team_id` INT NOT NULL, 
  `player_id` INT NOT NULL,
  PRIMARY KEY (`match_no`,`player_id`),
  FOREIGN KEY (`match_no`) REFERENCES `Match` (`match_no`),
  FOREIGN KEY (`team_id`) REFERENCES `Team` (`team_id`),
  FOREIGN KEY (`player_id`) REFERENCES `Player` (`player_id`)
);

CREATE TABLE `Goal` (
  `goal_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `match_no` INT NOT NULL,
  `player_id` INT NOt NULL,
  `team_id` INT NOt NULL,
  `goal_type` CHAR(1),
  `goal_time` INT NOT NULL,
  `goal_schedule` CHAR(2),
  `goal_half` CHAR(1),
  FOREIGN KEY (`match_no`) REFERENCES `Match` (`match_no`),
  FOREIGN KEY (`player_id`) REFERENCES `Player` (`player_id`),
  FOREIGN KEY (`team_id`) REFERENCES `Team` (`team_id`)
);


