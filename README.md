# GitDiff — High-Performance File Diff Engine

A full-stack file comparison engine that uses the **Myers Diff Algorithm** to calculate the shortest edit script between two files and visualize the differences through an interactive web interface.

The project is designed around the same core idea used by modern version-control systems such as Git: efficiently determining which lines were **added, deleted, or unchanged** between two versions of a file.

---

## 🚀 Live Demo

**Frontend:**  
https://gitdiff-frontend.onrender.com

**Backend API:**  
https://gitdiff-backend.onrender.com

---

## ✨ Features

- Compare two text files
- Paste file contents directly into the editor
- Upload files from your computer
- Maximum file size: **5 MB**
- Line-by-line diff visualization
- Shows:
  - Lines Added
  - Lines Deleted
  - Lines Unchanged
- Custom implementation of the **Myers Diff Algorithm**
- REST API built with FastAPI
- Interactive React frontend
- Dockerized frontend and backend
- Automated testing with pytest
- GitHub Actions CI pipeline
- Production deployment using Render

---

## 🧠 Myers Diff Algorithm

GitDiff uses the **Myers Diff Algorithm** instead of relying on Python's built-in `difflib` or an external diff library.

The algorithm finds the **shortest edit script** required to transform the old file into the new file.

The possible operations are:

```text
equal   → line exists in both files
insert  → line exists only in the new file
delete  → line exists only in the old file