CREATE DATABASE IF NOT EXISTS tealdb0;

-- Use the created database
USE tealdb0;


DROP TABLE IF EXISTS x_tealalertlog;
DROP VIEW  IF EXISTS tealalertlog;

DROP TABLE IF EXISTS x_tealeventlog;
DROP VIEW  IF EXISTS tealeventlog;

DROP TABLE IF EXISTS x_tealalert2alert;
DROP VIEW  IF EXISTS tealalert2alert;

DROP TABLE IF EXISTS x_tealalert2event;
DROP VIEW  IF EXISTS tealalert2event;

DROP TABLE IF EXISTS x_tealcheckpoint;
DROP VIEW  IF EXISTS tealcheckpoint;

DROP TABLE IF EXISTS x_CNM_1_2;

CREATE TABLE x_tealalert2alert (
  assoc_id bigint(20) NOT NULL auto_increment,
  alert_recid bigint(20) NOT NULL,
  assoc_type char(1) NOT NULL,
  t_alert_recid bigint(20) default NULL,
  comments text,
  disable text,
  PRIMARY KEY  (assoc_id)
) ENGINE=InnoDB;
CREATE VIEW tealalert2alert AS SELECT * FROM x_tealalert2alert;

CREATE TABLE x_tealalert2event (
  assoc_id bigint(20) NOT NULL auto_increment,
  alert_recid bigint(20) NOT NULL,
  assoc_type char(1) NOT NULL,
  t_event_recid bigint(20) default NULL,
  comments text,
  disable text,
  PRIMARY KEY  (assoc_id)
) ENGINE=InnoDB;
CREATE VIEW tealalert2event AS SELECT * FROM x_tealalert2event;

CREATE TABLE x_tealcheckpoint (
  chkpt_id bigint(20) NOT NULL auto_increment,
  name varchar(128) NOT NULL,
  status char(1) default NULL,
  event_recid bigint(20) default NULL,
  data varchar(1024) default NULL,
  comments text,
  disable text,
  PRIMARY KEY  (chkpt_id)
) ENGINE=InnoDB;
CREATE VIEW tealcheckpoint AS SELECT * FROM x_tealcheckpoint;


CREATE TABLE x_tealalertlog (
  rec_id bigint(20) NOT NULL auto_increment,
  alert_id char(8) NOT NULL,
  creation_time timestamp NOT NULL default CURRENT_TIMESTAMP,
  severity char(1) NOT NULL,
  urgency char(1) NOT NULL,
  event_loc_type varchar(2) NOT NULL,
  event_loc varchar(255) NOT NULL,
  fru_loc varchar(512) default NULL,
  recommendation varchar(2048) NOT NULL,
  reason varchar(512) NOT NULL,
  src_name varchar(64) NOT NULL,
  state tinyint(4) default NULL,
  raw_data varchar(2048) default NULL,
  comments text,
  disable text,
  PRIMARY KEY  (rec_id)
) ENGINE=InnoDB;
CREATE VIEW tealalertlog AS SELECT * FROM x_tealalertlog;


CREATE TABLE x_tealeventlog (
  rec_id bigint(20) NOT NULL auto_increment,
  event_id char(8) NOT NULL,
  time_logged timestamp NOT NULL default CURRENT_TIMESTAMP,
  time_occurred timestamp NOT NULL,
  src_comp varchar(128) NOT NULL,
  src_loc_type varchar(2) NOT NULL,
  src_loc varchar(255) NOT NULL,
  rpt_comp varchar(128) default NULL,
  rpt_loc_type varchar(2) default NULL,
  rpt_loc varchar(255) default NULL,
  event_cnt int(11) default NULL,
  elapsed_time bigint(20) unsigned default NULL,
  raw_data_fmt bigint(20) unsigned default NULL,
  raw_data varchar(1024) default NULL,
  ext_key  char(36) default NULL,   
  comments text,
  disable text,
  PRIMARY KEY  (rec_id)
) ENGINE=InnoDB;
CREATE VIEW tealeventlog AS SELECT * FROM x_tealeventlog;

CREATE TABLE x_CNM_1_2 (
  rec_id BIGINT NOT NULL,
  eed_loc_info VARCHAR(64) NOT NULL,
  encl_mtms VARCHAR(20) NOT NULL,
  pwr_ctrl_mtms VARCHAR(20) NOT NULL,
  neighbor_loc_type VARCHAR(2),
  neighbor_loc VARCHAR(256),
  recovery_file_path VARCHAR(32) NOT NULL,
  isnm_raw_data VARCHAR(1024) NOT NULL,
  local_port VARCHAR(256), 
  local_torrent VARCHAR(256),
  local_planar VARCHAR(256),
  local_om1 VARCHAR(256),
  local_om2 VARCHAR(256),
  nbr_port VARCHAR(256),
  nbr_torrent VARCHAR(256),
  nbr_planar VARCHAR(256),
  nbr_om1 VARCHAR(256),
  nbr_om2 VARCHAR(256),
  global_counter BIGINT,
  comments text,
  disable text,
  PRIMARY KEY  (rec_id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS site;
CREATE TABLE site (
    `key` VARCHAR(128) NOT NULL DEFAULT '',
    value TEXT,
    comments TEXT,
    disable TEXT,
    PRIMARY KEY  (`key`)
) ENGINE=InnoDB;

ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_fk_arec FOREIGN KEY (alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_fk_t_arec FOREIGN KEY (t_alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE RESTRICT;
ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_a2a_assoc_check CHECK(assoc_type IN ('C','S','D'));

ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_fk_erec FOREIGN KEY (alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_fk_t_erec FOREIGN KEY (t_event_recid) REFERENCES x_tealeventlog (rec_id) ON DELETE RESTRICT;
ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_a2e_assoc_check CHECK(assoc_type IN ('C','S'));

ALTER TABLE x_tealcheckpoint ADD CONSTRAINT teal_fk_chkrec FOREIGN KEY (event_recid) REFERENCES x_tealeventlog (rec_id) ON DELETE RESTRICT;

ALTER TABLE x_tealalertlog ADD CONSTRAINT teal_alert_state_check CHECK (state IN (1,2));

DELIMITER $$
CREATE TRIGGER teal_alertlog_delete BEFORE DELETE ON x_tealalertlog FOR EACH ROW BEGIN IF OLD.state = 1 THEN UPDATE `Error: Alert is in an invalid state for deletion` Set x = 1; END IF; END$$
DELIMITER ;

