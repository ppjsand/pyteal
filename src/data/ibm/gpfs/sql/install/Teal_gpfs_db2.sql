ALTER TABLE x_GPFS_1_1 ADD CONSTRAINT TEAL_GPFS_FS_FK  FOREIGN KEY ("rec_id") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_2 ADD CONSTRAINT TEAL_GPFS_DSK_FK FOREIGN KEY ("rec_id") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_3 ADD CONSTRAINT TEAL_GPFS_PER_FK FOREIGN KEY ("rec_id") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_4 ADD CONSTRAINT TEAL_GPFS_MSC_FK FOREIGN KEY ("rec_id") REFERENCES X_TEALEVENTLOG ("rec_id") ON DELETE CASCADE;