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


<table>
    <thead>
        <tr>
            <th>AICharts Modules</th>
            <th>External Modules</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>AICharts Report</td>
            <td>
                <ul>
                    <li><a href="https://pandas.pydata.org/">pandas</a></li>
                    <li><a href="https://matplotlib.org/">matplotlib</a></li>
                    <li><a href="https://networkx.org/">networkx</a></li>
                    <li><a href="https://github.com/laserson/squarify">squarify</a></li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>
                AICharts dataset
            </td>
            <td>
                <ul>
                    <li><a href="https://www.nltk.org/">nltk</a></li>
                    <li><a href="https://pypi.org/project/beautifulsoup4/">Beautiful Soup 4</a></li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>xNB Clasification</td>
            <td>
                <ul>
                    <li><a href="https://numpy.org/">numpy</a></li>
                    <li><a href="https://www.nltk.org/">nltk</a></li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>xNB Classes</td>
            <td>None
            </td>
        </tr>
    </tbody>
</table>