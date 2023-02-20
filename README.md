# Fever Code Challenge App by Nikolai Sviridov aka luchanos
<p>
<img src="https://raw.githubusercontent.com/gist/brudnak/aba00c9a1c92d226f68e8ad8ba1e0a40/raw/e1e4a92f6072d15014f19aa8903d24a1ac0c41a4/nyan-cat.gif" alt="drawing" width="500"/>
</p>

# Summary
This is a brief implementation of service for operating with external providers events due to Fever Job Interview
test task.

# Content
- [Overview](#Overview)
- [Ideas](#ideas)

# Overview
The system consists of 3 main blocks:
- API

Let us get an information about events in any datetime ranges, even historically.

- Events updater worker

This part responsible for refreshing actual data about events in database.

- Events deactivator worker

This part responsible for deactivation non-actual events in case of cancelling for example.

# Ideas and Solutions

Our API must be independent of providers side in situations, when provider is out of service. Furthermore, we need to
keep RPS to providers side in acceptable ranges.

Solution:
We can get data from our providers periodically. This data we can store in database for future usage. For that reason
in [.workers/event_refresher_worker.py](workers/event_refresher_worker.py) codebase was implemented. It creates new events and updates information about
old ones.

Events have last_updated_dt field which shows last moment, when information about event was updated. If event cancelled
then this field outdated more and more on each cycle of refreshing. On that way we can highlight them by simple query
and deactivate by setting is_active field to False value by worker in [.workers/event_deactivator_worker.py](workers/event_deactivator_worker.py)

If event just changed in time (early or later) - it's not a problem for us. Our worker handle with it too by refreshing
datetime ranges fields.
