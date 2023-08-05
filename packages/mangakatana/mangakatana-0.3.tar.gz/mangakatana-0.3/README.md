[![Downloads](https://pepy.tech/badge/mangakatana)](https://pepy.tech/project/mangakatana) [![Downloads](https://pepy.tech/badge/mangakatana/month)](https://pepy.tech/project/mangakatana/month) [![Downloads](https://pepy.tech/badge/mangakatana/week)](https://pepy.tech/project/mangakatana/week)

# Mangakatana API

Installation
-
**Python 3.7+**
```cmd
pip install mangakatana
```

Examples
-
```python
import mangakatana

results = mangakatana.search(title="Naruto")

first = results[0]

chapters = first.chapter_list()
# mangakatana.chapter_list(url=first.url)
```
