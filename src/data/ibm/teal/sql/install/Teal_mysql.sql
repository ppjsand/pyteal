ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_fk_arec FOREIGN KEY (alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_fk_t_arec FOREIGN KEY (t_alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE RESTRICT;
ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_a2a_assoc_check CHECK(assoc_type IN ('C','S','D'));

ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_fk_erec FOREIGN KEY (alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_fk_t_erec FOREIGN KEY (t_event_recid) REFERENCES x_tealeventlog (rec_id) ON DELETE RESTRICT;
ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_a2e_assoc_check CHECK(assoc_type IN ('C','S'));

ALTER TABLE x_tealcheckpoint ADD CONSTRAINT teal_fk_chkrec FOREIGN KEY (event_recid) REFERENCES x_tealeventlog (rec_id) ON DELETE RESTRICT;

ALTER TABLE x_tealalertlog ADD CONSTRAINT teal_alert_state_check CHECK (state IN (1,2));

ALTER TABLE x_IPMI_1_1 ADD CONSTRAINT teal_ipmi_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_AMM_1_1  ADD CONSTRAINT teal_amm_fk  FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;