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


