# AICharts

AICharts is an open source data visualization library that implements a naive bayes algorithm that makes text categorization predictions interpretable.

### Installation

You need to have LaTex installed on your computer.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the required libraries.

<ul>
    <li>Numpy</li>
    <li>Pandas</li>
    <li>Matplotlib</li>
    <li>Squarify</li>
    <li>Networkx</li>
    <li>Beautiful Soup 4</li>
    <li>nltk</li>
</ul>

```bash
pip install numpy pandas matplotlib squarify networkx beautifulsoup4
```
It is very importante to run de nltkConfig.py file if you don't have installed the necessary packages. 
It is needed to have the stopwords and the punkt package from nltk. If you wish to install it yourself you need to run python and run:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```
### To install latex in linux:
```bash
sudo apt-get install texlive-full
```
