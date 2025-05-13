# 📦 Dataset Zipping and Upload Script

This script helps you:

1. **Split a dataset folder** containing `.jpg` or `.png` images into multiple `.zip` files (each under a specified max size).
2. **Upload** those `.zip` files to a server endpoint (e.g., S3-compatible API).
3. Optionally, delete the zip files after upload (but **preserves the original dataset files**).

---

## 🛠 Requirements

- Python 3.6+
- `requests` library (install with `pip install requests`)

---

## 📁 Project Structure

```
dataset_uploader/
├── upload_script.py     # Main script for zipping and uploading
├── README.md            # This file
```

---

## 🚀 Usage

### 1. Set your configuration

Edit the `main()` function in `upload_script.py`:

```python
base_url = "https://your-api-host.com"
api_key = "your_api_key_here"
src_path = "/path/to/your/image/folder"
zip_file_path = "/path/to/store/temporary/zips/dataset_zip"
dataset_id = "your_dataset_id"
```

### 2. Run the script

```bash
python upload_script.py
```

It will:

- Split the folder into zip files (default max: 1 GB each)
- Upload them one by one
- Delete each zip after successful upload

---

## 🧩 Function Overview

### `split_folder_to_zips(folder_path, zip_base_name, max_size)`
Splits image files from a folder into multiple `.zip` files under the given size.

- Only `.jpg` and `.png` files are zipped.
- Original files are **not deleted**.

### `upload_to_s3(base_url, zip_file, api_key, dataset_id)`
Uploads a single `.zip` file to the server using a POST request with `multipart/form-data`.

- Requires an `Authorization` header with an API key.
- Expects the server to accept a `dataset_zip_file` and `dataset_id`.

---

## 🧹 Customization

- **Max zip size**: Change `max_size` in `split_folder_to_zips()` (default: 1 GB).
- **File types**: Add more extensions in the file filtering logic if needed.
- **Temporary storage**: Ensure there's enough disk space in the `zip_file_path` location.

---

## ⚠️ Notes

- This script assumes the server has an `/upload-dataset/` endpoint that accepts zip files and a `dataset_id`.
- You can disable deleting zip files after upload by commenting out this line:
  ```python
  os.remove(zip_file)
  ```

---

## 📞 Support

If you encounter issues or want to extend this for more file types or folder structures, feel free to ask for help.
