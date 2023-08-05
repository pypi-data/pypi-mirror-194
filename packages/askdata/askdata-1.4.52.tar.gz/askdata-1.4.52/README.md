<p align="center"><img src="askdata-logo-black.png" width="460"></p>

# Askdata

Askdata's mission is to make data meaningful for everyone, unlocking personal and business productivity.

|  |  |
|-|-|
| :ledger: [Docs](https://docs.askdata.com) | Usage, Guides, API documentation ...|
| :computer: [Access Akdata](https://askdata.com/agent) | Start using Askdata signing-in or registering |
| :art: [Key components](https://github.com/askdataHQ/askdata/#key-components) | Overview of core concepts |
| :eyes: [Getting Started](https://docs.askdata.com/getting-started) | Basic explanation of concepts, options and usage |
| :mortar_board: [Tutorials](https://docs.askdata.com/tutorials) | Jupyter/Colab Notebooks & Scripts |
| :telescope: [Roadmap](https://docs.askdata.com/docs/roadmap) | Public roadmap of Askdata |
| :heart: [Contributing](https://github.com/askdataHQ/askdata/#heart-contributing) | We welcome all contributions! |

## What is Askdata:

Askdata is a platform that allows users to interact with data through natural language, thus making accessing data as simple as searching for a restaurant on Google. Askdata makes its technology available to large national and international customers and is supported by Y Combinator, the prestigious Californian accelerator.

Askdata is a platform designed to enable anyone, regardless of the level of technical knowledge, to harness the power of data (big and small). Users leverage Askdata to explore, query, visualize, and share data from any data source. Our work enables anybody in business teams to use the data. Every day, thousands of users around the world use Askdata to share insights and make data-driven decisions.

### Askdata features:

* **Web-based:** Everything in your browser, with a shareable URL.
* **Native Apps:** Productive Native App for iOS and Android
* **Ease-of-use:** Become immediately productive with data without the need to master complex software.
* **Data Card Editor:** Quickly compose SQL and NoSQL queries with a schema browser and auto-complete.
* **Visualization and dashboards:** Create beautiful visualizations with drag and drop, and combine them into a single data-card.
* **Sharing:** Collaborate easily by sharing visualizations and their associated queries, enabling peer review of reports and queries.
* **Schedule refreshes:** Automatically update your data cards at regular intervals you define.
* **Alerts:** Define conditions and be alerted instantly when your data changes.
* **REST API:** Everything that can be done in the UI is also available through REST API.
* **Broad support:** for data sources: Extensible data source API with native support for a long list of common databases and platforms.

 # Askdata Examples
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github//AskdataHQ/askdata-docs/blob/gh-pages/notebooks/Askdata%20-%20Quickstart.ipynb)
This repository contains examples of [Askdata](https://www.askdata.com/) usage in serving different types of data.
## Installation
``
 pip install askdata 
``
or
``
pip install -r requirements.txt
``
## Authentication
Lets handle our authenticaton
```python
from askdata import Askdata
askdata = Askdata()
```
Once your insert your account and password you're all set
## Query your data
```python
#get one agent
df = askdata.get("sales by countries", workspace="sales_demo")
df
```
## Creating a new dataset starting from a Dataframe in an existing Workspace
```python
# Load the list of the agents connected to your account as a pandas dataframe
askdata.save(df, dataset_name='My Dataset Name',workspace="my_workspace")
```
## Askdata Demo
Check the following tutorial, to learn more about Askdata end-to-end. 
[![Askdata Tutorial](https://img.youtube.com/vi/uEc9ogi2-10/0.jpg)](https://youtu.be/uEc9ogi2-10) 

## Platform Components

### Core components:
* SmartAgent (NLP)
* SmartDataset (data virtualization service) 
* SmartFeed (data cards)

### NLP and NLG:
* Human2SQL (Model that translates Natural Language queries in technical queries)
* Human2Query (NLP data query service)
* SmartQuery (Multi-datasource query layer)
* SmartIntent (NLP engine)
* SmartQA (Knowledge retrieval service)
* SmartContent (Unstructured data service)

### Frameworks:
* Data Card Framework (https://github.com/AskdataHQ/askdata-datacard-components)
* Iconset (https://github.com/AskdataHQ/askdata-icon-library)
* Methodology (https://github.com/AskdataHQ/askdata-docs/tree/gh-pages/methodology)

### Catalogs:
* Charts Components Catalog (https://github.com/AskdataHQ/askdata-charts-components)
* Widgets
* Dataset Catalog (Will be released on the 1st week of Dec 2020)
* Dataset Integrations Catalog 
