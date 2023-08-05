<a href="https://colab.research.google.com/github/sbrobson959/alacorder/blob/main/index.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sbrobson959/alacorder/main?labpath=index.ipynb)
```
    ___    __                          __         
   /   |  / /___  _________  _________/ /__  _____
  / /| | / / __ `/ ___/ __ \/ ___/ __  / _ \/ ___/
 / ___ |/ / /_/ / /__/ /_/ / /  / /_/ /  __/ /    
/_/  |_/_/\__,_/\___/\____/_/   \__,_/\___/_/     

	ALACORDER beta 74
```

# **Getting Started with Alacorder**

<sup>[GitHub](https://github.com/sbrobson959/alacorder)  | [PyPI](https://pypi.org/project/alacorder/)     | [Report an issue](mailto:sbrobson@crimson.ua.edu)
</sup>

### Alacorder processes case detail PDFs into data tables suitable for research purposes. Alacorder also generates compressed text archives from the source PDFs to speed future data collection from the same set of cases.

## **Installation**

**Alacorder can run on most devices. If your device can run Python 3.7 or later, it can run Alacorder.**
* To install on Windows and Mac, open Command Prompt (Terminal) and enter `pip install alacorder` or `pip3 install alacorder`. 
* On Mac, open the Terminal and enter `pip install alacorder` or `pip3 install alacorder`.
* Install [Anaconda Distribution](https://www.anaconda.com/products/distribution) to install Alacorder if the above methods do not work, or if you would like to open an interactive browser notebook equipped with Alacorder on your desktop.
    * After installation, create a virtual environment, open a terminal, and then repeat these instructions. If your copy of Alacorder is corrupted, use `pip uninstall alacorder` or `pip3 uninstall alacorder` and then reinstall it. There may be a newer version available.

> **Alacorder should automatically download and install missing dependencies upon setup, but you can also install them yourself with `pip`: `pandas`, `numpy`, `PyPDF2`, `openpyxl`, `xlrd`, `xlwt`, `xarray`, `numexpr`, `bottleneck`, `pyarrow`, and `click`. Recommended dependencies: `xlsxwriter`, `jupyter`, `tabulate`, `matplotlib`.**


```python
pip install alacorder
```

## **Using the guided interface**

#### **Once you have a Python environment up and running, you can launch the guided interface in two ways:**

1.  *Utilize the `alacorder` command line tool in Python:* Use the command line tool `python -m alacorder`, or `python3 -m alacorder`. If  the guided version is launched instead of the command line tool, update your installation with `pip install --upgrade alacorder`.

2. *Conduct custom searches with `alac`:* Use the import statement `import alacorder as alac` to use the Alacorder APIs to collect custom data from case detail PDFs. See how you can make `alacorder` work for you in the code snippets below.

#### **Alacorder can be used without writing any code, and exports to common formats like Excel (`.xls`, `.xlsx`), Stata (`.dta`), CSV (`.csv`), and JSON (`.json`).**

* Alacorder compresses case text into `pickle` archives (`.pkl.xz`) to save storage and processing time. If you need to unpack a `pickle` archive without importing `alac`, use a `.xz` compression tool, then read the `pickle` into Python with the `pandas` method [`pd.read_pickle()`](https://pandas.pydata.org/docs/reference/api/pandas.read_pickle.html).



```python
import alacorder as alac
```

# **Special Queries with `alac`**

### **For more advanced queries, the `alacorder` libraries can extract fields and tables from case records with just a few lines of code.**

* Call `alac.conf.inputs("/pdf/dir/")` and `alac.conf.outputs("/to/table.xlsx")` to configure your input and output paths. Then call `alac.conf.set(input_conf, output_conf, **kwargs)` to complete the configuration process. Feed the output to any of the `alac.parse...()` functions to start a task.

* Call `alac.write.archive(config)` to export a full text archive. It's recommended that you create a full text archive (`.pkl.xz`) file before making tables from your data. Full text archives can be scanned faster than PDF directories and require less storage. Full text archives can be imported to Alacorder the same way as PDF directories. 

* Call `alac.parse.tables(config)` to export detailed case information tables. If export type is `.xls` or `.xlsx`, the `cases`, `fees`, and `charges` tables will be exported.

* Call `alac.parse.charges(config)` to export `charges` table only.

* Call `alac.parse.fees(config)` to export `fees` table only.

* Call `alac.parse.caseinfo(config)` to export `cases` table only. 


```python
import warnings
warnings.filterwarnings('ignore')

import alacorder as alac

pdf_directory = "/Users/crimson/Desktop/Tutwiler/"
archive = "/Users/crimson/Desktop/Tutwiler.pkl.xz"
tables = "/Users/crimson/Desktop/Tutwiler.xlsx"

# make full text archive from PDF directory 
c = alac.config(pdf_directory, archive_path=archive)
alac.write.archive(c)

print("Full text archive complete. Now processing case information into tables at " + tables)

pdfconf = alac.conf.inputs(pdf_directory)
arcconf = alac.conf.outputs(archive)
tabconf = alac.conf.outputs(tables)

make_archive = alac.conf.set(pdfconf, arcconf, count=1000) # input output **kwargs 

# then scan full text archive for spreadsheet
d = alac.config(archive, table_path=tables)
alac.parse.tables(d)
```

## **Custom Parsing with `alac.parse.map()`**
### If you need to conduct a custom search of case records, Alacorder has the tools you need to extract custom fields from case PDFs without any fuss. Try out `alac.parse.map()` to search thousands of cases in seconds.


```python
import alacorder as alac
import re

archive = "/Users/crimson/Desktop/Tutwiler.pkl.xz"
tables = "/Users/crimson/Desktop/Tutwiler.xlsx"

def findName(text):
    name = ""
    if bool(re.search(r'(?a)(VS\.|V\.{1})(.+)(Case)*', text, re.MULTILINE)) == True:
        name = re.search(r'(?a)(VS\.|V\.{1})(.+)(Case)*', text, re.MULTILINE).group(2).replace("Case Number:","").
	strip()
    else:
        if bool(re.search(r'(?:DOB)(.+)(?:Name)', text, re.MULTILINE)) == True:
            name = re.search(r'(?:DOB)(.+)(?:Name)', text, re.MULTILINE).group(1).replace(":","").replace("Case Number:","").strip()
    return name

i = alac.conf.inputs(archive) # configure input path
o = alac.conf.outputs(tables) # configure output path
c = alac.conf.set(i, o) # set configuration

alac.parse.map(c, findName)
```


| Method | Description |
| ------------- | ------ |
| `get.PDFText(path) -> text` | Returns full text of case |
| `get.CaseInfo(text) -> [case_number, name, alias, date_of_birth, race, sex, address, phone]` | Returns basic case details | 
| `get.FeeSheet(text, cnum = '') -> [total_amtdue, total_balance, total_d999, feecodes_w_bal, all_fee_codes, table_string, feesheet: pd.DataFrame]` | Returns fee sheet and summary as `str` and `pd.DataFrame` |
| `get.Charges(text, cnum = '') -> [convictions_string, disposition_charges, filing_charges, cerv_eligible_convictions, pardon_to_vote_convictions, permanently_disqualifying_convictions, conviction_count, charge_count, cerv_charge_count, pardontovote_charge_count, permanent_dq_charge_count, cerv_convictions_count, pardontovote_convictions_count, charge_codes, conviction_codes, all_charges_string, charges: pd.DataFrame]` |  Returns charges table and summary as `str`, `int`, and `pd.DataFrame` |
| `get.CaseNumber(text) -> case_number` | Returns case number
| `get.Name(text) -> name` | Returns name
| `get.FeeTotals(text) -> [total_row, tdue, tpaid, tbal, tdue]` | Return totals without parsing fee sheet



# **Working with case data in Python**


### Out of the box, Alacorder exports to `.xlsx`, `.xls`, `.csv`, `.json`, and `.dta`. But you can use `alac`, `pandas`, and other python libraries to create your own data collection workflows and design custom exports. 

***The snippet below prints the fee sheets from a directory of case PDFs as it reads them.***


```python
import alacorder as alac

c = alac.config("/Users/crimson/Desktop/Tutwiler/","/Users/crimson/Desktop/Tutwiler.xls")

for path in c['contents']:
    text = alac.get.PDFText(path)
    cnum = alac.get.CaseNumber(text)
    charges_outputs = alac.get.Charges(text, cnum)
    if len(charges_outputs[0]) > 1:
        print(charges_outputs[0])
```

## Extending Alacorder with `pandas` and other tools

Alacorder runs on [`pandas`](https://pandas.pydata.org/docs/getting_started/index.html#getting-started), a python library you can use to perform calculations, process text data, and make tables and charts. `pandas` can read from and write to all major data storage formats. It can connect to a wide variety of services to provide for easy export. When Alacorder table data is exported to `.pkl.xz`, it is stored as a `pd.DataFrame` and can be imported into other python [modules](https://www.anaconda.com/open-source) and scripts with `pd.read_pickle()` like below:
```python
import pandas as pd
contents = pd.read_pickle("/path/to/pkl")
```

If you would like to visualize data without exporting to Excel or another format, create a `jupyter notebook` and import a data visualization library like `matplotlib` to get started. The resources below can help you get started. [`jupyter`](https://docs.jupyter.org/en/latest/start/index.html) is a Python kernel you can use to create interactive notebooks for data analysis and other purposes. It can be installed using `pip install jupyter` or `pip3 install jupyter` and launched using `jupyter notebook`. Your device may already be equipped to view `.ipynb` notebooks. 

## **Resources**

* [`pandas` cheat sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
* [regex cheat sheet](https://www.rexegg.com/regex-quickstart.html)
* [anaconda (tutorials on python data analysis)](https://www.anaconda.com/open-source)
* [The Python Tutorial](https://docs.python.org/3/tutorial/)
* [`jupyter` introduction](https://realpython.com/jupyter-notebook-introduction/)


	

	
-------------------------------------		
© 2023 Sam Robson
