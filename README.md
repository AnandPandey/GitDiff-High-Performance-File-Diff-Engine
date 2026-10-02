# GitDiff

A high-performance file diff engine implemented using the
Myers Shortest Edit Script algorithm.

## Features

- Custom Myers Diff implementation
- Line-level file comparison
- Insert / Delete / Equal operations
- File upload
- Diff statistics
- Line numbers
- REST API using FastAPI
- React frontend
- Automated tests
- Reconstruction testing
- Performance benchmarking

## Architecture

React
    |
    | POST /api/diff
    v
FastAPI
    |
    v
Myers Diff Engine
    |
    v
Edit Operations

## Algorithm

GitDiff implements the Myers shortest edit script algorithm.

The algorithm uses:

- Edit graph
- D = number of edits
- k = diagonal
- V[k] = furthest x-coordinate reached
- Snake for matching sequences
- Trace for reconstruction
- Backtracking to generate edit operations

## Example

Old:

hello
world

New:

hello
beautiful world

Result:

 EQUAL  hello
 DELETE world
 INSERT beautiful world

## Testing

Run:

```bash
cd backend
source venv/bin/activate
python -m pytest