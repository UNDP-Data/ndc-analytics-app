#### The Application

This application is designed to facilitate the analysis of information from [NDC Registry](https://unfccc.int/NDCREG). It serves as a one-stop shop for querying over 200 Nationally Determined Contributions (NDCs) submitted to the registry since 2016. The database of the application includes both original and translated versions of the documents. A small fraction of NDCs available in the NDC Registry are not included in the database. See [Data Limitations](./about#data-limitations) for details.

Two main features of the application are [Search](./), a full-text search engine with support for multiple languages and filters, and [Ask Anything](./ask), an AI-powered chat interface for retrieval-augmented generation. Both can be used to retrieve relevant information from a set of close to 40,000 paragraphs from the NDCs.

#### Data Limitations

The application database contains **NDCs from the registry submitted before June 2025** and includes documents written in English, Spanish, French, Russian, Arabic and Chinese. While the coverage is almost complete, a few documents are not included in the database. This includes documents that were not machine-readable, e.g., scanned photocopies, and could not be processed by the application. Note that the database only includes a snapshot of the NDC Registry at a given point in time and does not include a historical archive of different NDCs versions. Only the latest version of each NDCs is available.

For a full list of documents available in this application, see [NDCs](./ndcs) page. Here is the list of NDCs available in [NDC Registry](https://unfccc.int/NDCREG) that are not available in this application at the time of writing:

| Party                                 | Version | Submission Date |
|---------------------------------------|---------|-----------------|
| Lesotho                               | N/A     | 2025-02-05      |
| Kiribati                              | 2       | 2023-03-02      |
| Mali                                  | 2       | 2021-10-11      |
| Nigeria                               | 3       | 2021-07-30      |
| Marshall Islands                      | 3       | 2020-12-31      |
| Kenya                                 | 2       | 2020-12-28      |
| Democratic People's Republic of Korea | 2       | 2019-09-19      |

#### Language Limitations

Note that the default full-text search engine will only work for queries and documents in English. You can change the engine to **Neural search** if you would like to include data in all languages. Note that Ask Anything feature is multi-lingual by default. 

#### Climate Promise Countries

The application allows to filter by Climate Promise (CP) countries. For more details about those, visit [Climate Promise](https://climatepromise.undp.org) page. Note that not all CP countries have necessarily submitted an NDC.

#### Query Guide

This guide briefly explain best practices for performing a full-text search.

- **Full-text search is currently only available for English text.**
- For multi-lingual search, change the engine to **Neural search**.
- To get the most accurate results, ensure that your query contains terms that are specific and relevant.
- Utilise filters to narrow down and organise your search results effectively. 
- By default, the search engine will interpret the terms in your query using
the `OR` operator, meaning it will find the documents containing any of the terms.
- If you want to search for an exact phrase, enclose your query into double quotes (`""`).

To illustrate, consider the queries below:

1. `climate change adaptation and mitigation`
2. `"climate change adaptation and mitigation"`

The first query without quotes finds texts that mention `climate`, `change`, `adaptation`, `and`, `mitigation` or any combination thereof. It will prioritise the results that contain the exact phrase or a valid subphrase, but it will also return results that contain individual terms.

The second query with quotes forces the search engine to only return the results that contain the phrase `climate change adaptation and mitigation` as a whole. So it will not match `climate change mitigation and adaptation`, for example.

This gives you a powerful tool to search for exactly what you need.
