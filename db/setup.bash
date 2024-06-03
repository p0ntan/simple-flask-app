#!/usr/bin/env bash
#
# Script for setting up db
#

function setup()
{
  sqlite3 db.sqlite < ddl.sql
  sqlite3 db.sqlite < insert.sql
}

setup
