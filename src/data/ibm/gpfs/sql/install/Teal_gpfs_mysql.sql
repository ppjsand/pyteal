ALTER TABLE x_GPFS_1_1 ADD CONSTRAINT teal_gpfs_fs_fk  FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_2 ADD CONSTRAINT teal_gpfs_dsk_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_3 ADD CONSTRAINT teal_gpfs_per_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_4 ADD CONSTRAINT teal_gpfs_msc_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
