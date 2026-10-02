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
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/diff", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          old_text: oldText,
          new_text: newText,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to calculate diff");
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setError(err.message);
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
                    handleFileUpload(event, setOldText)
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
                    handleFileUpload(event, setNewText)
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

            <div className="results-header">
              <h2>Diff Results</h2>
            </div>


            <div className="stats">

              <div>
                <strong>{result.added}</strong>
                <span>Lines Added</span>
              </div>

              <div>
                <strong>{result.deleted}</strong>
                <span>Lines Deleted</span>
              </div>

              <div>
                <strong>{result.unchanged}</strong>
                <span>Lines Unchanged</span>
              </div>

            </div>


            <div className="diff">

              {(() => {
                let oldLine = 1;
                let newLine = 1;

                return result.operations.map(
                  (operation, index) => {
                    const currentOldLine = oldLine;
                    const currentNewLine = newLine;

                    if (operation.type === "equal") {
                      oldLine++;
                      newLine++;
                    } else if (operation.type === "delete") {
                      oldLine++;
                    } else if (operation.type === "insert") {
                      newLine++;
                    }

                    return (
                      <div
                        key={index}
                        className={`diff-line ${operation.type}`}
                      >
                        <span className="line-number">
                          {operation.type === "insert"
                            ? ""
                            : currentOldLine}
                        </span>

                        <span className="line-number">
                          {operation.type === "delete"
                            ? ""
                            : currentNewLine}
                        </span>

                        <span className="symbol">
                          {operation.type === "insert"
                            ? "+"
                            : operation.type === "delete"
                            ? "-"
                            : " "}
                        </span>

                        <span>
                          {operation.line}
                        </span>
                      </div>
                    );
                  }
                );
              })()}

            </div>

          </section>

        )}

      </main>

    </div>
  );
}

export default App;