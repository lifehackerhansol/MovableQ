--
-- Copyright (C) 2023 lifehackerhansol
--
-- SPDX-License-Identifier: MIT
--
-- This is the MovableQ database schema, provided as reference.
-- Do not actually apply this schema, just running the app will 
-- use migrations in `dbupdate` folder to apply this schema.
--

drop table if exists jobs;


create table jobs
(
    job_id BIGINT PRIMARY KEY,
    id0 varchar(32) NOT NULL,
    lfcs varchar(8) DEFAULT NULL,
    friend_code varchar(12) DEFAULT NULL,
    system_id varchar(16) DEFAULT NULL,
    keyY varchar(32) DEFAULT NULL,
);
