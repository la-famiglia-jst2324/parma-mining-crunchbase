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
        ],
    }

    def get_normalization_map(self) -> dict:
        """Return the normalization map."""
        return self.map_json
