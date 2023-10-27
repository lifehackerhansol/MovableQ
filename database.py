#
# MovableQ Database Manager
# Copyright (c) 2023 lifehackerhansol
#
# SPDX-License-Identifier: MIT
#

import os
import sqlite3

import aiosqlite


class SQLDB():
    def __init__(self, bot):
        self.bot = bot
        self.dbpath = "movableq.db"

        # Perform migrations
        # Needs sqlite3 here because __init__ is not async
        conn = sqlite3.connect(self.dbpath)
        try:
            user_version = conn.execute("PRAGMA user_version")
            ret = user_version.fetchone()
            revision = ret[0]

        # if error, set to 0
        # breaks backward compatibility with pre-user_version dbs
        except sqlite3.Error:
            print(f"{self.dbpath} has no user_version set. Applying all schemas...")
            revision = 0

        updates = os.listdir("dbupdate")

        for i, x in enumerate(updates):
            updates[i] = x.replace(".sql", "")
        to_update = []

        for i in updates:
            if int(i) > revision:
                to_update.append(int(i))

        if not to_update:
            print(f"{self.dbpath} is up to date.")
        else:
            to_update.sort()
            print(f"Updating {self.dbpath} from {revision} to {to_update[-1]}")
            for i in to_update:
                with open(f"dbupdate/{i}.sql", "r") as f:
                    conn.executescript(f.read())
            conn.execute(f"PRAGMA user_version={to_update[-1]}")
            print(f"Updated {self.dbpath} from {revision} to {to_update[-1]}")
            conn.close()

    async def get_job_mii(self, system_id):
        async with aiosqlite.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            return await conn.execute_fetchall(f"SELECT job_id FROM modroles WHERE system_id={system_id};")

    async def get_job_fc(self, friend_code):
        async with aiosqlite.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            return await conn.execute_fetchall(f"SELECT job_id FROM modroles WHERE friend_code={friend_code};")

    async def get_job_id0(self, id0):
        async with aiosqlite.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            return await conn.execute_fetchall(f"SELECT job_id FROM modroles WHERE id0={id0};")

    async def add_job_mii(self, job_id, id0, system_id, keyY):
        async with aiosqlite.connect(self.dbpath) as conn:
            await conn.execute_insert(f"INSERT INTO jobs (job_id, id0, system_id, keyY) VALUES ({job_id}, {id0}, {system_id}, {keyY});")
            await conn.commit()

    async def add_job_fc(self, job_id, id0, friend_code, keyY):
        async with aiosqlite.connect(self.dbpath) as conn:
            await conn.execute_insert(f"INSERT INTO jobs (job_id, id0, friend_code, keyY) VALUES ({job_id}, {id0}, {friend_code}, {keyY});")
            await conn.commit()

    async def add_lfcs_to_job(self, job_id, lfcs):
        if len(lfcs) > 8:
            raise ValueError("Provided LFCS is not 8 characters in length. Note: don't store the 5th byte")
        async with aiosqlite.connect(self.dbpath) as conn:
            await conn.execute(f"UPDATE jobs SET lfcs={lfcs} WHERE job_id={job_id};")
            await conn.commit()

    async def add_keyy_to_job(self, job_id, keyy):
        async with aiosqlite.connect(self.dbpath) as conn:
            await conn.execute(f"UPDATE jobs SET keyY={keyy} WHERE job_id={job_id};")
            await conn.commit()

    # Database only has KeyY. Implement movable.sed compilation separately.
    async def get_keyy_from_job(self, job_id) -> str:
        async with aiosqlite.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            jobs = await conn.execute_fetchall(f"SELECT keyY FROM jobs where job_id={job_id};")
            if not jobs:
                return ""
            return jobs[0]['keyY']
