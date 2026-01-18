# Product Overview

## What is CSV Notes Manager?

CSV Notes Manager is a local web application that allows users to maintain persistent, searchable notes on specific CSV file rows across multiple file versions. The application solves the problem of tracking notes on data that changes regularly (daily/weekly CSV updates) without losing historical context.

## Core Value Proposition

- **Persistent Notes**: Notes survive CSV file updates and remain linked to specific rows via primary key
- **Version Tracking**: Handles orphaned rows when data is deleted from newer CSV versions
- **Local-First**: Runs entirely on user's machine with SQLite database - no external dependencies
- **Zero Data Loss**: Complete audit trail and soft-delete functionality

## Target Users

- Data analysts who receive regular CSV updates
- Business users tracking follow-up actions on data rows
- Anyone needing to maintain context across changing datasets

## Key Use Cases

1. **Weekly Data Updates**: Import new CSV versions while preserving existing notes
2. **Follow-up Tracking**: Tag and track status of items requiring action
3. **Historical Context**: View notes even after source rows are deleted
4. **Data Exploration**: Browse CSV data with inline notes column

## Current Status

Version 1.1.0 - Production ready with CSV explorer, note management, tagging, and Docker deployment.