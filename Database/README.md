# Beehive Task Ticket Manager Database

A relational database schema for a Jira-style task management system.

## Features

- Projects
- Sprints
- Task assignments
- Labels
- Comments
- Project membership system

## Tech Stack
- PostgreSQL
- pgAdmin

## Setup Instructions

1. Create a new PostgreSQL database.
2. Run:

   psql -U username -d dbname -f task_ticket_manager_full.sql

Or open in pgAdmin Query Tool and execute.
