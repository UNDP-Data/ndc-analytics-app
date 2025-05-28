###### The Application

This application is designed to facilitate the analysis of information from [NDC Registry](https://unfccc.int/NDCREG).
It serves as a single entry point for searching over 200 Nationally Determined Contributions (NDCs) submitted to 
the registry since 2016. The database of the application includes both original and translated version of the documents.
A small fraction of NDCs available in the NDC Registry are not included in the database.
See [Data Limitations](./about#data-limitations) for details.

Two main features of the application are [Search](./), a full-text search engine with support for multiple languages 
and filters, and [Ask Anything](./ask), an AI-powered chat interface for retrieval-augmented generation. Both can be
used to retrieve relevant information from a set of over 30,000 paragraphs from the NDCs.

###### Data Limitations

The database of the application includes about 200 NDCs from the registry. The data were collected in August 2024.
While the coverage of the NDCs is almost complete, a few documents are not included in the database. In particular, the
database does not include documents originally written in Arabic or Chinese languages. A few documents were not machine-readable 
and could not be processed by the application. The documents originally written in Russian are included in the database
but are not searchable using the Search feature. However, those can be analysed using Ask Anything feature. Note that
tge database only includes a snapshot of the NDC Registry at a given point in time and does not include a historical archive
of difference NDCs verions. Only the latest version for earch NDCs is available.

For a full list of documents available in this application, see [NDCs](./ndcs) page.
Here is a list of NDCs available in [NDC Registry](https://unfccc.int/NDCREG) that are not available in this application
at the time of writing:

| Party                                 | Version | Submission Date |
|---------------------------------------|---------|-----------------|
| China                                 | 2       | 2021-10-28      |
| Democratic People's Republic of Korea | 2       | 2019-09-19      |
| Iraq                                  | 1       | 2021-10-15      |
| Kenya                                 | 2       | 2020-12-28      |
| Kiribati                              | 2       | 2023-03-02      |
| Kuwait                                | 2       | 2021-10-12      |
| Mali                                  | 2       | 2021-10-11      |
| Marshall Islands                      | 3       | 2020-12-31      |
| Nigeria                               | 3       | 2021-07-30      |
| Qatar                                 | 2       | 2021-08-24      |
| Syrian Arab Republic                  | 1       | 2018-11-30      |

###### Climate Promise Countries

The application allows to filter by Climate Promise (CP) countries.
For more details about those, visit [Climate Promise](https://climatepromise.undp.org) page.
Note that not all CP countries have necessarily submitted an NDC.

###### Query Guide

This guide briefly explain best practices for performing a full-text search.

- **Full-text search in French and Spanish is not available during preview.**
- To get the most accurate results, ensure that your query contains terms that are specific and relevant.
- Utilise filters to narrow down and organise your search results effectively. 
- By default, the search engine will interpret the terms in your query using
the `OR` operator, meaning it will find the documents containing any of the terms.
- If you want to search for an exact phrase, enclose your query into double quotes (`""`).

To illustrate, consider the queries below:

1. `climate change adaptation and mitigation`
2. `"climate change adaptation and mitigation"`

The first query without quotes finds texts that mention `climate`, `change`, `adaptation`, `and`, `mitigation` or any combination thereof.
It will prioritise the results that contain the exact phrase or a valid subphrase, but it will also
return results that contain individual terms.

The second query with quotes forces the search engine to only return the results that contain the phrase `climate change adaptation and mitigation`
as a whole. So it will not match `climate change mitigation and adaptation`, for example.

This gives you a powerful tool to search for exactly what you need.
