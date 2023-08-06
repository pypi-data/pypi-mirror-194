

config_us = {
        "Constructors": {
            "Sales": "FastSalesUS",
            "Stores": "FastStoresUS",
            "Tool": "FastToolUS",
            "ToolMeasurement":"FastToolMsrmtUS"},
        "store_mstr_columns": {
            "segment": "MasterChain",
            "banner": "StoreClassification",
            "Region": "RegionName",
            "territory": "TerritoryName",
            "storegrid": "StoreName",
            "is_covered": "IsCovered",
            "partner_id": "StoreId",
            "partner_id_backup": "",
            "state": "StateName",
            "rep_type": "RepType",
            "chain": 'Chain'
        },
        "store_mstr_categorical_columns":["StoreClassification", "TerritoryName", "MasterChain",
                            "StoreName", "RegionName", "RepType", "Chain", 'StoreFormat'],
        "Test_store_Partner_ID_backup": "Test_store_Customer_Number",
        "heading_names": {
            "banner": "Banner",
            "segment": "Segment",
            "territory": "Territory",
            "storegrid": "Overall Segment",
            "partner_id": "Customer Name",
            "store_segment": "Store Segment",
            "currency": "$"
        },
        "weekly_target_variable": {
            "banner": "StoreClassification",
            "storegrid": "StoreName",
            "segment": "MasterChain",
            "partner_id": "StoreId",
            "rsv": "POS",
            "volume": "Volume",
            "cbulvl1": 'Category',
            "cbulvl2": 'Consumption',
            "seasonal": 'SeasonalPackaging',
            "packformat": "PackType",
            "week_no": "Week_Number",
            "year": "Year",
            "week": "Week",
            "territory": "TerritoryName",
            "Region": "RegionName",
            "tdlinx_no": 'TDLinxNo',
            "store_number": 'StoreNumber',
            "brands": "Brands"
        },
        "feature_parameter": {
            "is_product_present": 1,
            "active_store_filter_type": "test",
            "test_variable_dates": 0,
            "control_store_buffer":1.2,
            "data_continuity_check":1,
            "outlier_detection":1,
            "outlier_column":"MasterChain",
            "control_store_threshold":
            {
                'similarity_threshold':0.5,
                'correlation_threshold':0.5
            },
            "advanced_control_mapping":{
                'store_attribute':'RegionName',
            },
        },
        "query_parameters": {
            "store_mstr_columns": {
                # "banner" : {"ui_parameter_name":"channel", "datatype":"object"},
                # "storegrid":{"ui_parameter_name":"store_name_value", "datatype":"list"},
                # "segment" :{"ui_parameter_name":"segments_value", "datatype":"list"} ,
                # "territory" : "TerritoryName",
                # "Region" :"RegionName",

            },
            "weekly_target_variable": {

            }
        },
        "tables": {
            "control_store_mstr": "[FAST_US].[Tl_Controlstore_Mstr]",
            "measurement": "[FAST_US].[Tl_Measurement_Tbl]",
            "record_mstr": "[FAST_US].[Tl_RecordMstr]",
            "store_mstr": "[FAST_US].[TL_StoreMstr_US]",
            "test_mstr": "[FAST_US].[Tl_TestMstr]",
            "test_store_map": "[FAST_US].[Tl_Teststore_map]",
            "weekly_mstr": {
                'C-Store': "[FAST_US].[Tl_Weekly_target_mst_US_cstore_UPC]",
                'Walmart': '[FAST_US].[Tl_Weekly_target_mst_US_walmart_UPC]',
                'Others': '[FAST_US].[Tl_Weekly_target_mst_US_others_UPC]',
                'custom': '[FAST_US].[Tl_Weekly_target_mst_US_custom]'
            },
            "upload_stores": "[FAST_US].[Tl_Upload_store_population_US]",
            "config_mstr": "[FAST_US].[Tl_ConfigMstr]",
            "weekly_data_table": "[FAST_US].[Tl_Product_Mstr]",
            "store_data_table": "[FAST_US].[TL_StoreMstr_US]",
            "rls": "[FAST_US].[TL_RLS_US]",
            "cross-category-table": "[FAST_US].[Tl_Weekly_target_mst_US_custom]"
        },
        "metadata": {
            "test_configuration": {
                "sales_weeks": {
                    "Walmart": 52,
                    "C-Store": 18,
                    "Others": 16
                },
                "sales_lifts_sales_weeks": {
                    "Walmart": 26,
                    "C-Store": 9,
                    "Others": 8
                },
                "sales_diff_percentage": 10,
                "power_of_test": 0.7,
                "min_teststores": 20,
            },
            "test_planning": {
                 # StoreMaster categorical columns
                "test_vs_population_compare": {
                    "RTM": {
                        "Walmart": [
                            "StoreFormat",
                            "NumberCheckout",
                            "RepType",
                            "MinPerVisit",
                            "TotalDuration",
                            "TotalVisits",
                            "Weekly_Volume",
                            "StoreSize",
                            "StoreName"
                        ],
                        "C-Store": [
                            "StoreFormat",
                            "NumberCheckout",
                            "RepType",
                            "MinPerVisit",
                            "TotalDuration",
                            "TotalVisits",
                            "Weekly_Volume",
                            "StoreSize",
                            "StoreName"
                        ],
                        "Others": [
                            "StoreFormat",
                            "NumberCheckout",
                            "RepType",
                            "MinPerVisit",
                            "TotalDuration",
                            "TotalVisits",
                            "Weekly_Volume",
                            "StoreSize",
                            "StoreName"
                        ]
                    },
                    "NON-RTM": {
                        "Walmart": [
                            "StoreFormat",
                            "NumberCheckout",
                            "RepType",
                            "MinPerVisit",
                            "TotalDuration",
                            "TotalVisits",
                            "Weekly_Volume",
                            "StoreSize",
                            "StoreName"
                        ],
                        "C-Store": [
                            "StoreFormat",
                            "NumberCheckout",
                            "RepType",
                            "MinPerVisit",
                            "TotalDuration",
                            "TotalVisits",
                            "Weekly_Volume",
                            "StoreSize",
                            "StoreName"
                        ],
                        "Others": [
                            "StoreFormat",
                            "NumberCheckout",
                            "RepType",
                            "MinPerVisit",
                            "TotalDuration",
                            "TotalVisits",
                            "Weekly_Volume",
                            "StoreSize",
                            "StoreName"
                        ]
                    }
                },
                "test_vs_population_compare_summary": {
                    "Walmart": [
                        "TotalVisits",
                        "MinPerVisit"
                    ],
                    "C-Store": [
                        "TotalVisits",
                        "MinPerVisit"
                    ],
                    "Others": [
                        "TotalVisits",
                        "MinPerVisit",
                        "StoreSize"
                    ]
                },
                "sampling_iterations": 10,
                "test_vs_population_pvalue": 0.7,
                "test_vs_control_compare": {
                    "RTM": {
                        "Walmart": [
                            "RepType",
                            "TotalVisits",
                            "MinPerVisit"
                        ],
                        "C-Store": [
                            "RepType",
                            "MinPerVisit",
                            "Chain",
                            "TotalVisits"
                        ],
                        "Others": [
                            "RepType",
                            "TotalVisits",
                            "MinPerVisit",
                            "StoreName",
                            "StoreSize"
                        ]
                    },
                    "NON-RTM": {
                        "Walmart": [
                            "StoreName"
                        ],
                        "C-Store": [],
                        "Others": [
                            "Weekly_Volume",
                            "StoreSize"
                        ]
                    }
                },
                "test_vs_control_compare_summary": {
                    "Walmart": [
                        "TotalVisits",
                        "MinPerVisit"
                    ],
                    "C-Store": [
                        "TotalVisits",
                        "MinPerVisit"
                    ],
                    "Others": [
                        "TotalVisits",
                        "MinPerVisit",
                        "StoreSize",
                        "Weekly_Volume"
                    ]
                },
                "business_category_specific_compare": [],
                "business_categories_count": 0,
                "test_vs_control_pvalue": 0.8,
                "test_vs_control_similaritymeasure_difference_threshold": 0.05,
                "summary_sales_weeks": {
                    "Walmart": 26,
                    "C-Store": 9,
                    "Others": 8
                },
                "validate_datapoints_multiplier": 2,
                "teststores_columns": [
                    "StoreId",
                    "MasterChain",
                    "StoreName",
                    "StoreClassification",
                     "TerritoryName",
                     "RegionName"
                ],
                "upload_stores_identifier":"StoreIdentifier",
                "upload_teststores_identifier":'Test_store_StoreIdentifier',
                "upload_controlstores_identifier":'Control_store_StoreIdentifier',
                "user_populationstores_columns": {
                    "StoreIdentifier": "int64"
                },
                "user_teststores_columns": {
                    "Test_store_StoreIdentifier": "int64"
                },
                "control_storespool_columns": {
                    "Control_store_StoreIdentifier": "int64"
                },
                "confidence_level": 0.85,
                "margin_of_error": 0.04,
                "power_of_test": 0.7,
                "power_values": [
                    60,
                    65,
                    70,
                    75,
                    80,
                    85,
                    90,
                    95
                ],
                "user_testcontrolstores_columns": {
                    "Test_store_StoreIdentifier": "int64",
                    "Control_store_StoreIdentifier": "int64"
                },
                "custom_sales_upload": {
                    "StoreIdentifier": "int64",
                    "SalesDates(YYYY-MM-DD)": "O",
                    "POS": "float64"
                }
            },
            "test_measurement": {
                "probability_thresholds": [
                    0.60,
                    0.85,
                    1
                ],
                "testmeasurement_columns": [
                    "StoreId",
                    "StoreNumber",
                    "TDLinx_No",
                    "MasterChain",
                    "StoreClassification",
                    "StoreName"
                ]
            }
        },
        "filePath": {
            "TestStore": {
                "file_name": "/DSCode/regions/US/upload_templates/Upload_Teststores_Template_US.xlsx"
            },
            "controlStore": {
                "file_name": "/DSCode/regions/US/upload_templates/Test_Control_Pairs_Upload_Template_US.xlsx"
            },
            "controlStore_Pool": {
                "file_name": "DSCode/regions/US/upload_templates/Control_Pairs_Pool_Upload_Template_US.xlsx"
            },
            "RSV_STORES": {
                "file_name": "/DSCode/regions/US/upload_templates/Upload_Population_Template_US.xlsx"
            },
            "Cross_Category": {
                "file_name": "Sales_Upload_Template_US.xlsx"
            }
        },
        "excel_header": {
            "test_store": "Test_store_StoreId",
            "control_store": "Control_store_StoreId",
            "control_store_pool": "StoreId"
        },
        "control_store_excel_header": {
            "test_store": {
                "StoreId": "Test_store_StoreIdentifier",
                "StoreNumber": "Test_store_StoreIdentifier",
                "TDLinx_No": "Test_store_StoreIdentifier"
            },
            "control_store": {
                "StoreId": "Control_store_StoreIdentifier",
                "StoreNumber": "Control_store_StoreIdentifier",
                "TDLinx_No": "Control_store_StoreIdentifier"
            },
            "control_store_pool": {
                "StoreId": "StoreIdentifier",
                "StoreNumber": "StoreIdentifier",
                "TDLinx_No": "StoreIdentifier"
            }
        },
        "report_generate": {
            "common": {
                "region_name": "UNITED STATES OF AMERICA",
                "flag_name": 'flag_US.png'
            },
            "control_compare_variable": ["TotalVisits", "MinPerVisit"],
            "test_compare_variable": ["TotalVisits", "MinPerVisit"],
            "store_feature": ["TotalVisits", "MinPerVisit"],
            "row_span": 2,
            "matching_criteria": ["TotalVisits", "MinPerVisit"]
        },
        "result_grid_excel": {
            "header_data": ['Week', 'Category', 'Metric', 'Variable', 'Value'],
            "category_format": {"Confectionary_Combination_1": 'category1',
                                "Confectionary_Combination_2": 'category2',
                                "Confectionary_Combination_3": 'category3',
                                "Confectionary_Combination_4": 'category4'}
        }
    }
