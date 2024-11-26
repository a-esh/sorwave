-

# Sorwave

Sorwave is a powerful music classifier based on Python. It uses the `mutagen` libraries and `musicbrainzngs` API to manage metadata and perform other music file-related operations. This project is designed to help users efficiently organize and manage their music collection.
https://pypi.org/project/sorwave/

## Table of Contents

- [Sorwave](#sorwave)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Functions](#functions)
    - [`get_metadata`](#get_metadata)
      - [Usage Example](#usage-example)
    - [`gen_log`](#gen_log)
      - [Usage Example](#usage-example-1)
    - [`new_log`](#new_log)
      - [Usage Example](#usage-example-2)
    - [`filter_artist`](#filter_artist)
      - [Usage Example](#usage-example-3)
    - [`sort_songs`](#sort_songs)
      - [Usage Example](#usage-example-4)
  - [Features](#features)
  - [Contributing](#contributing)
  - [Roadmap](#roadmap)
  - [FAQ](#faq)
    - [What music file formats are supported?](#what-music-file-formats-are-supported)
    - [How can I report an issue or request a new feature?](#how-can-i-report-an-issue-or-request-a-new-feature)
  - [License](#license)
  - [Contact](#contact)
  - [Social Media](#social-media)
  - [Community](#community)

## Description

Sorwave allows users to automatically organize their music library by managing metadata and classifying files. This tool is especially useful for those who want to keep their music collections organized without manual effort.

## Installation

You can install Sorwave from PyPI using `pip`:

```bash
pip install sorwave
```

## Functions

### `get_metadata`

```python
import sorwave as sw
```

This function extracts metadata from a song when provided with the file path.

#### Usage Example

```python
metadata = sw.get_metadata(r'path/to/your/song.mp3')
print(metadata)
```

### `gen_log`

```python
import sorwave as sw
```

This function generates a log in the main directory of all the songs and songs in the subdirectories. It saves a JSON file with the metadata of each song organized by artist, albums, and songs in order.

#### Usage Example

```python
sw.gen_log(r'path/to/your/music/folder')
```

### `new_log`

```python
import sorwave as sw
```

This function can be used to create a new log of specific activities or events in the music management system.

#### Usage Example

```python
sw.new_log('Description of the event or activity')
```

### `filter_artist`

```python
import sorwave as sw
```

This function filters artist names to be compatible with Windows paths without losing the meaning of the names.

#### Usage Example

```python
artist = 'Name: of*Artist?'
filtered_artist = sw.filter_artist(artist)
print(filtered_artist)  # Output: Name_of_Artist
```

### `sort_songs`

```python
import sorwave as sw
```

This function organizes music into their respective folders and subfolders (artists, albums, and songs).

#### Usage Example

```python
sw.sort_songs(r'path/to/your/music/folder')
```

## Features

- **Metadata Management:** Uses `mutagen` to read and write metadata in music files.
- **Song Classification:** Classifies songs based on different criteria.
- **Activity Logging:** Keeps a log of activities related to music management.
- **Command Line Interface:** Run and manage tasks directly from the command line.

## Contributing

Contributions are welcome! If you want to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## Roadmap

- [ ] Add support for more music file formats.
- [ ] Improve documentation with more examples and tutorials.
- [x] Integration with online music services for automatic metadata.

## FAQ

### What music file formats are supported?

Currently, Sorwave supports MP3 and FLAC files. We are working to add support for more formats in future versions.

### How can I report an issue or request a new feature?

You can open an [issue on GitHub](https://github.com/A-esh/sorwave/issues) to report problems or request new features.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more details.

## Contact

Author: a-esh  
Email: [abrahamescalona@live.com](mailto:abrahamescalona@live.com)

## Social Media

[![GitHub](https://img.shields.io/badge/GitHub-My_Profile-5B47ED?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/A-esh) [![Linkedin](https://img.shields.io/badge/Linkedin-Professional_Profile-2867B2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=101010)](https://www.linkedin.com/in/abraham-esh/)
[![X](https://img.shields.io/badge/Twitter-X-000000?style=for-the-badge&logo=x&logoColor=white&labelColor=101010)](https://twitter.com/abraham_esh)

## Community

[![Discord](https://img.shields.io/badge/Discord-Community_Channel-5865F2?style=for-the-badge&logo=discord&logoColor=white&labelColor=101010)](https://discord.gg/eh7BFDB)

-
