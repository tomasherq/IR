#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys

# Use Pyserini in this repo (as opposed to pip install)
sys.path.insert(0, './')

from pyserini.prebuilt_index_info import TF_INDEX_INFO, IMPACT_INDEX_INFO, FAISS_INDEX_INFO


__boilerplate__ = '''
# Pyserini: Prebuilt Indexes

Pyserini provides a number of pre-built Lucene indexes.
To list what's available in code:

```python
from pyserini.search import SimpleSearcher
SimpleSearcher.list_prebuilt_indexes()

from pyserini.index import IndexReader
IndexReader.list_prebuilt_indexes()
```

It's easy initialize a searcher from a pre-built index:

```python
searcher = SimpleSearcher.from_prebuilt_index('robust04')
```

You can use this simple Python one-liner to download the pre-built index:

```
python -c "from pyserini.search import SimpleSearcher; SimpleSearcher.from_prebuilt_index('robust04')"
```

The downloaded index will be in `~/.cache/pyserini/indexes/`.

It's similarly easy initialize an index reader from a pre-built index:

```python
index_reader = IndexReader.from_prebuilt_index('robust04')
index_reader.stats()
```

The output will be:

```
{'total_terms': 174540872, 'documents': 528030, 'non_empty_documents': 528030, 'unique_terms': 923436}
```

Note that unless the underlying index was built with the `-optimize` option (i.e., merging all index segments into a single segment), `unique_terms` will show -1.
Nope, that's not a bug.

Below is a summary of the pre-built indexes that are currently available.
Detailed configuration information for the pre-built indexes are stored in [`pyserini/prebuilt_index_info.py`](../pyserini/prebuilt_index_info.py).

'''


def generate_prebuilt(index):
    print('<dl>')
    for entry in index:
        # No, this is not an HTML bug. This is intentional to get GitHub formatting to not add italics to the entry.
        print(f'<dt></dt><b><code>{entry}</code></b>')
        print(f'<dd>{index[entry]["description"]}')
        if 'readme' in index[entry]:
            print(f'[<a href="{index[entry]["readme"]}">readme</a>]')
        print(f'</dd>')
    print('</dl>')


if __name__ == '__main__':
    print(__boilerplate__)
    print('\n\n## Standard Lucene Indexes')
    generate_prebuilt(TF_INDEX_INFO)
    print('\n\n## Lucene Impact Indexes')
    generate_prebuilt(IMPACT_INDEX_INFO)
    print('\n\n## Faiss Indexes')
    generate_prebuilt(FAISS_INDEX_INFO)
