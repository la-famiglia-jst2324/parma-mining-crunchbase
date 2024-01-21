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
                "SourceField": "ipo_status",
                "DataType": "text",
                "MeasurementName": "ipo status of company",
            },
            {
                "SourceField": "company_type",
                "DataType": "text",
                "MeasurementName": "company type",
            },
            {
                "SourceField": "founded_on",
                "DataType": "date",
                "MeasurementName": "company foundation date",
            },
            {
                "SourceField": "legal_name",
                "DataType": "text",
                "MeasurementName": "legal name of company",
            },
            {
                "SourceField": "num_employees_enum",
                "DataType": "text",
                "MeasurementName": "company number of employees range",
            },
            {
                "SourceField": "rank_org_company",
                "DataType": "int",
                "MeasurementName": "company crunchbase rank",
            },
            {
                "SourceField": "total_funding_usd",
                "DataType": "int",
                "MeasurementName": "company total funding (USD)",
            },
            {
                "SourceField": "last_funding_type",
                "DataType": "text",
                "MeasurementName": "company last funding type",
            },
            {
                "SourceField": "num_funding_rounds",
                "DataType": "int",
                "MeasurementName": "number of funding rounds",
            },
            {
                "last_funding_at": "date",
                "DataType": "date",
                "MeasurementName": "company last funding date",
            },
            {
                "SourceField": "num_investors",
                "DataType": "int",
                "MeasurementName": "number of investors",
            },
            {
                "SourceField": "num_acquirees",
                "DataType": "int",
                "MeasurementName": "number of acquirees",
            },
            {
                "SourceField": "num_technologies",
                "DataType": "int",
                "MeasurementName": "number of technologies used",
            },
            {
                "SourceField": "apptopia_total_apps",
                "DataType": "int",
                "MeasurementName": "number of apps by apptopia",
            },
            {
                "SourceField": "apptopia_total_downloads",
                "DataType": "int",
                "MeasurementName": "number of downloads by apptopia",
            },
            {
                "SourceField": "email",
                "DataType": "text",
                "MeasurementName": "contact email",
            },
            {
                "SourceField": "phone",
                "DataType": "text",
                "MeasurementName": "contact phone",
            },
            {
                "SourceField": "num_contact_email",
                "DataType": "int",
                "MeasurementName": "number of contact emails",
            },
            {
                "SourceField": "num_contact_phone",
                "DataType": "int",
                "MeasurementName": "number of contact phones",
            },
            {
                "SourceField": "num_contact",
                "DataType": "int",
                "MeasurementName": "number of total contacts",
            },
            {
                "SourceField": "num_similar_companies",
                "DataType": "int",
                "MeasurementName": "number of similar companies",
            },
            {
                "SourceField": "num_current_positions",
                "DataType": "int",
                "MeasurementName": "number of current positions",
            },
            {
                "SourceField": "num_event_appearances",
                "DataType": "int",
                "MeasurementName": "number of event appearances",
            },
            {
                "SourceField": "num_patents",
                "DataType": "int",
                "MeasurementName": "number of patents",
            },
            {
                "SourceField": "num_trademarks",
                "DataType": "int",
                "MeasurementName": "number of trademarks",
            },
            {
                "SourceField": "popular_trademark_class",
                "DataType": "text",
                "MeasurementName": "popular trademark class",
            },
            {
                "SourceField": "num_activity",
                "DataType": "int",
                "MeasurementName": "number of activities",
            },
            {
                "SourceField": "semrush_rank",
                "DataType": "int",
                "MeasurementName": "company semrush global rank",
            },
            {
                "SourceField": "semrush_visits_last_month",
                "DataType": "int",
                "MeasurementName": "company visits last month by semrush",
            },
            {
                "SourceField": "semrush_visits_mom_pct",
                "DataType": "float",
                "MeasurementName": "company visits percentage monthly by semrush",
            },
            {
                "SourceField": "growth_insight",
                "DataType": "text",
                "MeasurementName": "company growth insight",
            },
            {
                "SourceField": "siftery_num_products",
                "DataType": "int",
                "MeasurementName": "company number of products by siftery",
            },
            {
                "SourceField": "acquirees",
                "DataType": "nested",
                "MeasurementName": "acquirees of company",
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
                "SourceField": "acquirer",
                "DataType": "nested",
                "MeasurementName": "acquirer of company",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "acquirer name",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "acquirer permalink",
                    },
                    {
                        "SourceField": "acquisition",
                        "DataType": "nested",
                        "MeasurementName": "acquirer acquisition",
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
                "SourceField": "investors",
                "DataType": "nested",
                "MeasurementName": "investors of company",
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
                                "MeasurementName": "partner job title",
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
                "SourceField": "funding_rounds",
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
            {
                "SourceField": "SimilarCompanies",
                "DataType": "nested",
                "MeasurementName": "similar companies to company",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "similar company name",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "similar company permalink",
                    },
                ],
            },
            {
                "SourceField": "featured_employees",
                "DataType": "nested",
                "MeasurementName": "featured employees",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "employee name",
                    },
                    {
                        "SourceField": "title",
                        "DataType": "text",
                        "MeasurementName": "employee job title",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "employee permalink",
                    },
                    {
                        "SourceField": "email",
                        "DataType": "text",
                        "MeasurementName": "employee email",
                    },
                    {
                        "SourceField": "start_date",
                        "DataType": "date",
                        "MeasurementName": "employee start date",
                    },
                    {
                        "SourceField": "phone",
                        "DataType": "text",
                        "MeasurementName": "employee phone",
                    },
                    {
                        "SourceField": "linkedin",
                        "DataType": "text",
                        "MeasurementName": "employee linkedin",
                    },
                ],
            },
            {
                "SourceField": "events",
                "DataType": "nested",
                "MeasurementName": "interacted events",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "event name",
                    },
                    {
                        "SourceField": "permalink",
                        "DataType": "text",
                        "MeasurementName": "event permalink",
                    },
                    {
                        "SourceField": "interaction_type",
                        "DataType": "text",
                        "MeasurementName": "event interaction type",
                    },
                ],
            },
            {
                "SourceField": "activities",
                "DataType": "nested",
                "MeasurementName": "activities of company",
                "NestedMappings": [
                    {
                        "SourceField": "title",
                        "DataType": "text",
                        "MeasurementName": "activity title",
                    },
                    {
                        "SourceField": "activity_type",
                        "DataType": "text",
                        "MeasurementName": "activity type",
                    },
                    {
                        "SourceField": "author",
                        "DataType": "text",
                        "MeasurementName": "activity author",
                    },
                    {
                        "SourceField": "publisher",
                        "DataType": "text",
                        "MeasurementName": "activity publisher",
                    },
                    {
                        "SourceField": "date",
                        "DataType": "date",
                        "MeasurementName": "activity date",
                    },
                    {
                        "SourceField": "url",
                        "DataType": "link",
                        "MeasurementName": "activity url",
                    },
                ],
            },
            {
                "SourceField": "country_data",
                "DataType": "nested",
                "MeasurementName": "country traffic data by semrush",
                "NestedMappings": [
                    {
                        "SourceField": "visits_pct",
                        "DataType": "float",
                        "MeasurementName": "country visit percentage",
                    },
                    {
                        "SourceField": "rank_mom_pct",
                        "DataType": "float",
                        "MeasurementName": "country rank percentage monthly",
                    },
                    {
                        "SourceField": "rank",
                        "DataType": "int",
                        "MeasurementName": "country rank",
                    },
                    {
                        "SourceField": "location",
                        "DataType": "text",
                        "MeasurementName": "country name",
                    },
                ],
            },
            # to be added later: Social media, categories, location
        ],
    }

    def get_normalization_map(self) -> dict:
        """Return the normalization map."""
        return self.map_json
