alter table x_gpfs_1_3 alter column "location" drop not null;
alter table x_gpfs_1_3 alter column "fru" drop not null;
alter table x_gpfs_1_3 alter column "wwn" drop not null;
alter table x_rginfo alter column "rg_act_svr" set data type varchar(64);
alter table x_rginfo alter column "rg_svrs" set data type varchar(128);
alter table x_rginfo_tmp alter column "rg_act_svr" set data type varchar(64);
alter table x_rginfo_tmp alter column "rg_svrs" set data type varchar(128);
alter table x_dainfo_tmp alter column "da_free_space" set data type bigint;
reorg table x_gpfs_1_3;
reorg table x_rginfo;
reorg table x_rginfo_tmp;
reorg table x_dainfo_tmp;
