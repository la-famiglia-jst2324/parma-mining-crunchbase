"""Normalization map for Crunchbase data."""


class CrunchbaseNormalizationMap:
    """Normalization map for Crunchbase data."""

    map_json = {
        "Source": "crunchbase",
        "Mappings": [
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "company name",
            },
            {
                "SourceField": "description",
                "DataType": "text",
                "MeasurementName": "company description",
            },
            {
                "SourceField": "permalink",
                "DataType": "text",
                "MeasurementName": "company permalink",
            },
            {
                "SourceField": "website",
                "DataType": "link",
                "MeasurementName": "company website",
            },
            {
                "SourceField": "growth_insight",
                "DataType": "text",
                "MeasurementName": "company growth insight",
            },
            {
                "SourceField": "sifter_num_products",
                "DataType": "int",
                "MeasurementName": "company sifter num products",
            },
            {
                "SourceField": "AcquisitionModel",
                "DataType": "nested",
                "MeasurementName": "acquisitions",
                "NestedMappings": [
                    {
                        "SourceField": "title",
                        "DataType": "text",
                        "MeasurementName": "acquisition title",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "acquisition permalink",
                    },
                    {
                        "SourceField": "price_usd",
                        "DataType": "int",
                        "MeasurementName": "acquisition price (USD)",
                    },
                    {
                        "SourceField": "date",
                        "DataType": "date",
                        "MeasurementName": "acquisition date",
                    },
                ],
            },
            {
                "SourceField": "AcquireeModel",
                "DataType": "nested",
                "MeasurementName": "acquirees",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "acquiree name",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "acquiree permalink",
                    },
                    {
                        "SourceField": "acquisition",
                        "DataType": "nested",
                        "MeasurementName": "acquiree acquisition",
                        "NestedMappings": [
                            {
                                "SourceField": "title",
                                "DataType": "text",
                                "MeasurementName": "acquisition title",
                            },
                            {
                                "SourceField": "permalink",
                                "DataType": "text",
                                "MeasurementName": "acquisition permalink",
                            },
                            {
                                "SourceField": "price_usd",
                                "DataType": "int",
                                "MeasurementName": "acquisition price (USD)",
                            },
                            {
                                "SourceField": "date",
                                "DataType": "date",
                                "MeasurementName": "acquisition date",
                            },
                        ],
                    },
                ],
            },
            {
                "SourceField": "InvestorModel",
                "DataType": "nested",
                "MeasurementName": "investors",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "investor name",
                    },
                    {
                        "SourceField": "investment_title",
                        "DataType": "text",
                        "MeasurementName": "investment title",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "investor permalink",
                    },
                    {
                        "SourceField": "partners",
                        "DataType": "nested",
                        "MeasurementName": "investor partners",
                        "NestedMappings": [
                            {
                                "SourceField": "name",
                                "DataType": "text",
                                "MeasurementName": "partner name",
                            },
                            {
                                "SourceField": "title",
                                "DataType": "text",
                                "MeasurementName": "partner title",
                            },
                            {
                                "SourceField": "permalink",
                                "DataType": "text",
                                "MeasurementName": "partner permalink",
                            },
                            {
                                "SourceField": "email",
                                "DataType": "text",
                                "MeasurementName": "partner email",
                            },
                            {
                                "SourceField": "start_date",
                                "DataType": "date",
                                "MeasurementName": "partner start date",
                            },
                            {
                                "SourceField": "phone",
                                "DataType": "text",
                                "MeasurementName": "partner phone",
                            },
                            {
                                "SourceField": "linkedin",
                                "DataType": "text",
                                "MeasurementName": "partner linkedin",
                            },
                        ],
                    },
                ],
            },
            {
                "SourceField": "FundingRoundModel",
                "DataType": "nested",
                "MeasurementName": "funding rounds",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "funding round name",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "funding round permalink",
                    },
                    {
                        "SourceField": "announced_on",
                        "DataType": "date",
                        "MeasurementName": "funding round announced on",
                    },
                    {
                        "SourceField": "money_raised_usd",
                        "DataType": "int",
                        "MeasurementName": "funding round money raised (USD)",
                    },
                    {
                        "SourceField": "num_investors",
                        "DataType": "int",
                        "MeasurementName": "funding round number of investors",
                    },
                    {
                        "SourceField": "lead_investors",
                        "DataType": "nested",
                        "MeasurementName": "funding round lead investors",
                        "NestedMappings": [
                            {
                                "SourceField": "name",
                                "DataType": "text",
                                "MeasurementName": "lead investor name",
                            },
                            {
                                "SourceField": "investment_title",
                                "DataType": "text",
                                "MeasurementName": "lead investor investment title",
                            },
                            {
                                "SourceField": "permalink",
                                "DataType": "text",
                                "MeasurementName": "lead investor permalink",
                            },
                        ],
                    },
                ],
            },
        ],
    }

    def get_normalization_map(self) -> dict:
        """Return the normalization map."""
        return self.map_json
