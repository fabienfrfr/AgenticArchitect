# Persistent Python Execution in Markdown

This guide explains how to use a standard `.md` file to write and execute Python code with persistent memory, without the clutter of Jupyter Notebook files (`.ipynb`).

## 🛠 Required Setup

To run code blocks and keep variables in memory, ensure you have these extensions in VS Code:

* **Python** (by Microsoft)
* **Jupyter** (by Microsoft) — *Used as the background engine only.*

## 🚀 Usage Instructions

### Markdown Preview Enhanced

Side-by-side preview:

1. Install the **Markdown Preview Enhanced** extension.
2. In your Markdown, add `{cmd=true}` to your code blocks:

```python
x = 42

```

3. Open the preview (`Ctrl+Shift+V`) and click on the output area to run.

---

## 📝 Example

Run the blocks below in order to test the persistent memory:

**Block 1: Define a variable**

```python
message = "Memory is persistent!"
print("Variable defined.")

```

**Block 2: Access the variable**

```python
# This works without re-defining 'message'
print(f"Result: {message}")

```

## 💎 Benefits

* **Clean Git History**: No metadata or binary blobs, just plain text.
* **No Cache**: No `.ipynb_checkpoints` or hidden folders created.
* **Lightweight**: Perfect for documentation that needs to be "runnable."
