ALTER TABLE X_TEALALERT2ALERT ADD CONSTRAINT TEAL_FK_AREC FOREIGN KEY ("alert_recid") REFERENCES X_TEALALERTLOG ("rec_id") ON DELETE CASCADE;
ALTER TABLE X_TEALALERT2ALERT ADD CONSTRAINT TEAL_FK_T_AREC FOREIGN KEY ("t_alert_recid") REFERENCES X_TEALALERTLOG ("rec_id") ON DELETE RESTRICT;
ALTER TABLE X_TEALALERT2ALERT ADD CONSTRAINT TEAL_A2A_ASSOC_CHECK CHECK("assoc_type" IN ('C','S','D'));

ALTER TABLE X_TEALALERT2EVENT ADD CONSTRAINT TEAL_FK_EREC FOREIGN KEY ("alert_recid") REFERENCES X_TEALALERTLOG ("rec_id") ON DELETE CASCADE;
ALTER TABLE X_TEALALERT2EVENT ADD CONSTRAINT TEAL_FK_T_EREC FOREIGN KEY ("t_event_recid") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE RESTRICT;
ALTER TABLE X_TEALALERT2EVENT ADD CONSTRAINT TEAL_A2E_ASSOC_CHECK CHECK("assoc_type" IN ('C','S'));

ALTER TABLE X_TEALCHECKPOINT ADD CONSTRAINT TEAL_FK_CHKREC FOREIGN KEY ("event_recid") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE RESTRICT;

ALTER TABLE X_TEALALERTLOG ADD CONSTRAINT TEAL_ALERT_STATE_CHECK CHECK ("state" IN (1,2));

CREATE TRIGGER TEAL_DUPALERT_DELETE AFTER DELETE ON X_TEALALERT2ALERT REFERENCING OLD AS OLD FOR EACH ROW BEGIN ATOMIC IF (OLD."assoc_type" = 'D') THEN DELETE FROM X_TEALALERTLOG WHERE "rec_id" = OLD."t_alert_recid"; END IF; END;
CREATE TRIGGER TEAL_ALERTLOG_DELETE BEFORE DELETE ON X_TEALALERTLOG REFERENCING OLD AS OLD FOR EACH ROW BEGIN ATOMIC IF (OLD."state" = 1) THEN SIGNAL SQLSTATE '70003' ('Deletion not permitted'); END IF; END;

ALTER TABLE X_IPMI_1_1 ADD CONSTRAINT TEAL_IPMI_FK FOREIGN KEY ("rec_id") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE CASCADE;
ALTER TABLE X_AMM_1_1  ADD CONSTRAINT TEAL_AMM_FK  FOREIGN KEY ("rec_id") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE CASCADE;