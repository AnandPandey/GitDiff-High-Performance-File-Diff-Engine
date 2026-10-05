import { useState } from "react";
import "./styles.css";

function App() {
  const [oldText, setOldText] = useState("");
  const [newText, setNewText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleFileUpload(event, setText) {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    const maxSize = 5 * 1024 * 1024;

    if (file.size > maxSize) {
      setError("File size cannot exceed 5 MB.");
      return;
    }

    try {
      const content = await file.text();

      setText(content);
      setError("");
    } catch (error) {
      setError("Could not read the selected file.");
    }
  }

  async function compareFiles() {
    if (!oldText && !newText) {
      setError("Please provide content for both files.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "https://gitdiff-backend.onrender.com/api/diff",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            old_text: oldText,
            new_text: newText,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to calculate diff");
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setError(
        "Could not connect to the GitDiff backend."
      );
    }

    setLoading(false);
  }

  return (
    <div className="app">

      <header>
        <div className="logo">
          <div className="logo-mark">
            GD
          </div>

          <h1>GitDiff</h1>
        </div>

        <p>
          High-Performance File Diff Engine
        </p>

        <span>
          Myers Shortest Edit Script Algorithm
        </span>
      </header>

      <main>

        {/* FILE INPUTS */}

        <section className="editors">

          <div className="editor">

            <div className="editor-header">
              <div>
                <h2>Old File</h2>
                <span>Original</span>
              </div>

              <label className="file-button">
                Choose File

                <input
                  type="file"
                  onChange={(event) =>
                    handleFileUpload(
                      event,
                      setOldText
                    )
                  }
                />
              </label>
            </div>

            <textarea
              value={oldText}
              onChange={(event) =>
                setOldText(event.target.value)
              }
              placeholder="Paste original file content..."
              spellCheck="false"
            />

          </div>


          <div className="editor">

            <div className="editor-header">
              <div>
                <h2>New File</h2>
                <span>Modified</span>
              </div>

              <label className="file-button">
                Choose File

                <input
                  type="file"
                  onChange={(event) =>
                    handleFileUpload(
                      event,
                      setNewText
                    )
                  }
                />
              </label>
            </div>

            <textarea
              value={newText}
              onChange={(event) =>
                setNewText(event.target.value)
              }
              placeholder="Paste modified file content..."
              spellCheck="false"
            />

          </div>

        </section>


        <div className="compare-section">

          <button
            onClick={compareFiles}
            disabled={loading}
          >
            {loading
              ? "Comparing..."
              : "Compare Files"}
          </button>

        </div>


        {error && (
          <div className="error">
            {error}
          </div>
        )}


        {result && (
          <section className="results">

            {/* RESULT HEADER */}

            <div className="results-header">
              <div>
                <h2>Diff Results</h2>

                <span>
                  Line + Character Comparison
                </span>
              </div>
            </div>


            {/* STATISTICS */}

            <div className="stats">

              <div>
                <strong>
                  {result.added}
                </strong>

                <span>
                  Lines Added
                </span>
              </div>

              <div>
                <strong>
                  {result.deleted}
                </strong>

                <span>
                  Lines Deleted
                </span>
              </div>

              <div>
                <strong>
                  {result.unchanged}
                </strong>

                <span>
                  Lines Unchanged
                </span>
              </div>

            </div>


            {/* LINE LEVEL DIFF */}

            <section className="diff-section">

              <div className="section-title">
                <h3>
                  Line-by-Line Diff
                </h3>

                <span>
                  Myers Line Diff
                </span>
              </div>

              <div className="diff">

                {result.line_operations.map(
                  (operation, index) => {

                    return (
                      <div
                        key={index}
                        className={`diff-line ${operation.type}`}
                      >

                        <span className="line-number">
                          {operation.old_line_number || ""}
                        </span>

                        <span className="line-number">
                          {operation.new_line_number || ""}
                        </span>

                        <span className="symbol">
                          {operation.type === "insert"
                            ? "+"
                            : operation.type === "delete"
                            ? "-"
                            : " "}
                        </span>

                        <span className="line-content">
                          {operation.line}
                        </span>

                      </div>
                    );
                  }
                )}

              </div>

            </section>


            {/* CHARACTER LEVEL DIFF */}

            <section className="character-section">

              <div className="section-title">
                <h3>
                  Character-by-Character Diff
                </h3>

                <span>
                  Myers Character Diff
                </span>
              </div>


              {result.character_diffs.length === 0 && (
                <div className="no-character-diff">
                  No modified lines require character-level
                  comparison.
                </div>
              )}


              {result.character_diffs.map(
                (diff, index) => {

                  return (
                    <div
                      className="character-card"
                      key={index}
                    >

                      <div className="character-card-header">

                        <span>
                          Line {diff.old_line_number}
                          {" → "}
                          Line {diff.new_line_number}
                        </span>

                      </div>


                      <div className="character-grid">

                        {/* OLD */}

                        <div className="character-panel">

                          <div className="character-panel-title">
                            OLD
                          </div>

                          <div className="character-content delete-view">

                            {diff.changes.map(
                              (change, changeIndex) => {

                                if (
                                  change.type === "equal"
                                ) {
                                  return (
                                    <span
                                      key={changeIndex}
                                    >
                                      {change.text}
                                    </span>
                                  );
                                }

                                if (
                                  change.type === "delete"
                                ) {
                                  return (
                                    <span
                                      key={changeIndex}
                                      className="character-delete"
                                    >
                                      {change.text}
                                    </span>
                                  );
                                }

                                return null;
                              }
                            )}

                          </div>

                        </div>


                        {/* NEW */}

                        <div className="character-panel">

                          <div className="character-panel-title">
                            NEW
                          </div>

                          <div className="character-content insert-view">

                            {diff.changes.map(
                              (change, changeIndex) => {

                                if (
                                  change.type === "equal"
                                ) {
                                  return (
                                    <span
                                      key={changeIndex}
                                    >
                                      {change.text}
                                    </span>
                                  );
                                }

                                if (
                                  change.type === "insert"
                                ) {
                                  return (
                                    <span
                                      key={changeIndex}
                                      className="character-insert"
                                    >
                                      {change.text}
                                    </span>
                                  );
                                }

                                return null;
                              }
                            )}

                          </div>

                        </div>

                      </div>

                    </div>
                  );
                }
              )}

            </section>

          </section>
        )}

      </main>

    </div>
  );
}

export default App;