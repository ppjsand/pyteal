ALTER TABLE x_tealalert2alert DROP FOREIGN KEY teal_fk_arec;
ALTER TABLE x_tealalert2alert DROP FOREIGN KEY teal_fk_t_arec;

ALTER TABLE x_tealalert2event DROP FOREIGN KEY teal_fk_erec;
ALTER TABLE x_tealalert2event DROP FOREIGN KEY teal_fk_t_erec;

ALTER TABLE x_tealcheckpoint DROP FOREIGN KEY teal_fk_chkrec;

DROP TRIGGER teal_dupalert_delete;
DROP TRIGGER teal_alertlog_delete; 


