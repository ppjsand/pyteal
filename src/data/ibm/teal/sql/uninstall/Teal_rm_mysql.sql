ALTER TABLE x_tealalert2alert DROP FOREIGN KEY teal_fk_arec;
ALTER TABLE x_tealalert2alert DROP FOREIGN KEY teal_fk_t_arec;

ALTER TABLE x_tealalert2event DROP FOREIGN KEY teal_fk_erec;
ALTER TABLE x_tealalert2event DROP FOREIGN KEY teal_fk_t_erec;

ALTER TABLE x_tealcheckpoint DROP FOREIGN KEY teal_fk_chkrec;

ALTER TABLE x_IPMI_1_1 DROP FOREIGN KEY teal_ipmi_fk;
ALTER TABLE x_AMM_1_1  DROP FOREIGN KEY teal_amm_fk;
