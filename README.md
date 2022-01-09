# AICharts

AICharts is an open source data visualization library that implements a naive bayes algorithm that makes text categorization predictions interpretable.

### Installation

You need to have LaTex installed on your computer.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the required libraries.

<ul>
    <li><a href="https://numpy.org/">Numpy</a></li>
    <li><a href="https://pandas.pydata.org/">Pandas</a></li>
    <li><a href="https://matplotlib.org/">Matplotlib</a></li>
    <li><a href="https://github.com/laserson/squarify">Squarify</a></li>
    <li><a href="https://networkx.org/">Networkx</a></li>
    <li><a href="https://pypi.org/project/beautifulsoup4/">Beautiful Soup 4</a></li>
    <li><a href="https://www.nltk.org/">nltk</a></li>
</ul>

```bash
pip install numpy pandas matplotlib squarify networkx beautifulsoup4
```
It is very important to run de nltkConfig.py file if you don't have installed the necessary packages. 
It is needed to have the stopwords and the punkt package from nltk. If you wish to install it yourself you need to run python and run:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

It is also very important to have a LaTeX installation on your machine. If you are using Linux you can install by doing the following command:
### To install latex in linux:
```bash
sudo apt-get install texlive-full
```
If you are on Windows you can try TeX Live on the following link: https://www.tug.org/texlive/