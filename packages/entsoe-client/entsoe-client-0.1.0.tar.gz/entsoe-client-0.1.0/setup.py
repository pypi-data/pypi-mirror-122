# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entsoe_client',
 'entsoe_client.ParameterTypes',
 'entsoe_client.Parsers',
 'entsoe_client.Queries',
 'entsoe_client.Queries.Balancing',
 'entsoe_client.Queries.Congestion',
 'entsoe_client.Queries.Generation',
 'entsoe_client.Queries.Load',
 'entsoe_client.Queries.MasterData',
 'entsoe_client.Queries.Outages',
 'entsoe_client.Queries.Transmission',
 'entsoe_client.Utils']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1.1,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.6.3,<5.0.0',
 'pandas>=1.3.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.1,<2022.0',
 'requests>=2.26.0,<3.0.0',
 'tenacity>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'entsoe-client',
    'version': '0.1.0',
    'description': 'Formulate human-readable queries and retrieve data from ENTSO-E into pandas.DataFrame format.',
    'long_description': '===============\nENTSO-E Client\n===============\n\n\n| *ENTSO-E Client* enables straight-forward access to *all* of the data at `ENTSO-E Transparency Platform <https://transparency.entsoe.eu/>`_.\n\n* Query templates abstract the API specifics through Enumerated types.\n\n* Parse responses into Pandas DataFrames without loss of *any* information.\n\n| The separation of Queries, Client and Parser with their hierarchical abstractions keep the package extensible and maintainable. A pipeline from Query to DataFrame is trivial, preserving the ability to customize steps in between.\n\n| The implementation relies primarily on the\n `Transparency Platform restful API - user guide <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>`_.\n The `Manual of Procedures (MoP) <https://www.entsoe.eu/data/transparency-platform/mop/>`_ documents provide\n further insight on the *business requirements specification*.\n Further information can be found in the\n `Electronic Data Interchange (EDI) Library <https://www.entsoe.eu/publications/electronic-data-interchange-edi-library/>`_.\n\n-----\n\nMain contributions\n\n* Exhaustive List of ParameterTypes.\n    These allow mapping between natural language and the codes required\n    for GET requests, e.g. :code:`DocumentType.A85 == DocumentType("Imbalance price")`.\n    This feature allows keeping track of queries without jumping between documents or adding comments.\n\n* Exhaustive List of Pre-defined Queries from ENTSO-E API Guide.\n    `ENTSO-E API Guide <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>`_\n    is a minial set for any API connector to implement and reflects all dashboards on\n    ENTSO-E Transparency Platform.\n\n* Parsers\n    Response `Documents` come in XML schema which can be parsed into pandas DataFrames.\n\n    Implemented: GL_MarketDocuments, TransmissionNetwork_MarketDocuments,\n    Publication_MarketDocuments and Balancing_MarketDocuments.\n\n    Missing: Outages, Congestion Management and System Operations.\n\nNevertheless, ENTSO-E Client seeks to be minimal to go from Query to DataFrame and requires domain-\nknowledge on how to formulate queries and interpret various columns of a parsed response.\n\n-----\n\nENTSO-E relies on many codes (`Type`) to map to desired queries.\nTypes are encoded in Enum classes with a .help() function to list the all.\nThey can be addressed through Type[code] or Type(string), making interaction\neasy. HTTP requests and responses usually require the `code`, whereas we\nwant to formulate the query as a human-readable `string`.\n\n::\n\n    from entsoe_client import Queries\n    from entsoe_client.ParameterTypes import *\n\n    Queries.Transmission.CapacityAllocatedOutsideEU(\n            out_Domain=Area.SK,\n            in_Domain=Area.UA_BEI,\n            marketAgreementType=MarketAgreementType(\'Daily\'), # Original code: A01\n            auctionType=AuctionType(\'Explicit\'), # Original code: A02\n            auctionCategory=AuctionCategory(\'Hourly\'), # Original code: A04\n            classificationSequence_AttributeInstanceComponent_Position=1,\n            periodStart=201601012300,\n            periodEnd=201601022300)\n\n::\n\n    >>> ParameterTypes.DocumentType[\'A25\'] == ParameterTypes.DocumentType(\'Allocation result document\')\n    True\n    >>> ec.ParameterTypes.DocumentType.help()\n    --- DocumentType ---\n    API_PARAMETER: DESCRIPTION\n    [...]\n    A25: Allocation result document\n    A71: Generation forecast\n    A72: Reservoir filling information\n    A73: Actual generation\n    A85: Imbalance prices\n    A86: Imbalance volume\n    [...]\n    API_PARAMETER: DESCRIPTION\n    --- DocumentType ---\n    >>> ec.ParameterTypes.BusinessType.help()\n    --- BusinessType ---\n    API_PARAMETER: DESCRIPTION\n    [...]\n    A25: General Capacity Information\n    A29: Already allocated capacity(AAC)\n    A97: Manual frequency restoration reserve\n    B08: Total nominated capacity\n    C22: Shared Balancing Reserve Capacity\n    C24: Actual reserve capacity\n    [...]\n    API_PARAMETER: DESCRIPTION\n    --- BusinessType ---\n\n::\n\n    #shortened from sample_plot.py\n    import entsoe_client as ec\n    from settings import api_key\n\n    # Instantiate Client, Parser and Query.\n    client = ec.Client(api_key)\n    parser = ec.Parser()\n    query = ec.Queries.Generation.AggregatedGenerationPerType(\n        in_Domain=ec.ParameterTypes.Area.DE_LU,\n        periodStart=202109050200,\n        periodEnd=202109070200)\n\n    # Extract data.\n    response = client(query)\n    df = parser(response)\n    [...]\n\n    # Transform data.\n    production = df[~consumption_mask][[\'quantity\', \'TimeSeries.MktPSRType.psrType\']]\n    ## PsrType, e.g. `B01` := `Biomass`.\n    production[\'GenerationType\'] = production[\'TimeSeries.MktPSRType.psrType\']. \\\n        apply(lambda x: ParameterTypes.PsrType[x].value) # Map ENTSO-E PsrTypes into human-readable string.\n    production_by_type = pd.pivot_table(production,\n                                        index=production.index,\n                                        columns=\'GenerationType\',\n                                        values=\'quantity\')\n    [...]\n    # Plot.\n    production_by_type.plot.bar(title="Production by Generation Type in DE-LU",\n                                xlabel="UTC",\n                                ylabel=\'MWh\',\n                                ax=ax,\n                                **plot_params)\n    [...]\n\n\n.. image:: ./sample_plot.png\n',
    'author': 'Dario Hett',
    'author_email': 'dariohett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DarioHett/entsoe-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
