# SWGOH Guild Data App

A project to gather, process, and manage data from the game **Star Wars: Galaxy of Heroes (SWGOH)** for guild management and spreadsheet reporting.

## Features

- **Automated Data Collection:** Fetches player, guild, and raid data via API requests, as well as .csv imports.
- **Database Integration:** Reads from and writes to a PostgreSQL database for persistent storage.
- **Spreadsheet Sync:** Updates Google Sheets with the latest guild and player statistics.
- **Logging & Error Handling:** Configurable logging for debugging and monitoring.
- **Roster & Ticket Tracking:** Tracks player activity, raid scores, tickets, and roster requirements.
- **Data Archiving:** Archives players who have left the guild and removes them from the active members tables.

## Project Structure

```
.
├── src/                  # Main application source code
│   ├── api_request.py
│   ├── archive_players.py
│   ├── check_raid_results.py
│   ├── csv_import.py
│   ├── enter_data.py
│   ├── helper_functions.py
│   ├── log_gp.py
│   ├── log_raid_score.py
│   ├── log_tickets.py
│   ├── main.py
│   ├── push_to_sheets.py
│   ├── read_data.py
│   ├── remove_data.py
│   ├── roster_checks.py
│   ├── spreadsheet_operations.py
│   ├── update_data.py
│   └── ...
├── tests/                # Unit tests
├── README.md             # This file
```
## Data Sources & Dependencies

This project uses a PostgreSQL database for persistent storage and easy access to prepared views to display on google spreadsheets. Most of the data is fetched automatically through a locally hosted version of the [swgoh-comlink](https://github.com/swgoh-utils/swgoh-comlink) API, which serves mostly publicly available game data. <br>
To ensure accuracy, ticket data is retrieved within a few minutes of the guild reset every day. TB data has to be manually exported from other tools like HotUtils and can then be imported to the database.<br>
The database, API and scheduled python programs are hosted on local hardware. 

## Spreadsheet View Example

<img src="assets/spreadsheet_example.png" alt="An example of the main spreadsheet view" width="80%">

The main view combines the most important metrics, so they are visible at a glance. For a deeper dive into the different topics, there are more detailed views available. <br>
(Information that could potentially identify an individual has been anonymized for this example.)

## Reproducing the project

This is meant solely as a personal project at this point. Pull requests are welcome, but i will not support replication efforts.
Please open an issue, if you have any inquiries. 


---

*This project is not affiliated with or endorsed by Electronic Arts Inc. or Lucasfilm Ltd. All trademarks are property of their respective owners.*
