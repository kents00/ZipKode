# ZipKode

It's a web app using the Flask framework that lets users search for ZIP codes by regions, provinces, cities, and municipalities in a specific area in the philippines.

![ZIPKODE](https://github.com/kents00/ZipKode/assets/69900896/ba9a72ce-026f-4ec4-838a-da278f294301)

### Installation

```bash
// Clone the repository
git clone https://github.com/kents00/ZipKode.git

// installing requirements
pip install -r requirements.txt

//run into your local machine
flask --app app run
```

The application will be accessible at **`http://127.0.0.1:5000/`** in your web browser.

### API

The project provides a simple API for searching ZIP codes.

- **Endpoint**: **`/search`**
- **Method**: GET
- **Parameters**:
    - **`search_term`** (required): The term to search for.

**Example Request**:

```bash
// localhost
curl http://127.0.0.1:5000/search?search_term=Manila

// render
curl https://zipkode.onrender.com/search?search_term=Manila
```

**Example Response**:

```json
{
  "result": {
    "NCR (National Capital Region)": {
      "Metro Manila": {
        "Manila Bay (Reclamation)": "1308",
        "Manila Doctors Village": "1748",
        "Manila Memorial Park": "1717"
      }
    }
  },
  "search_term": "Manila"
}
```

### Issues

If you're having trouble integrating this code into your machine, [open a new issue](https://github.com/kents00/ZipKode/issues). As this repository continues to develop, it will be easier for more developers to integrate updates and improve overall user performance!
