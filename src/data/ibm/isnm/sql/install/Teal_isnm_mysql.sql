ALTER TABLE x_CNM_1_2 ADD CONSTAINT teal_isnm_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
