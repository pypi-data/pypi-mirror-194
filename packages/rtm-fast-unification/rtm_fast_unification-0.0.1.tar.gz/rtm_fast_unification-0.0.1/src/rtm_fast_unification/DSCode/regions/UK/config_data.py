

config_uk = {
        "Constructors": {
            "Sales": "FastSalesUK",
            "Stores": "FastStoresUK",
            "Tool": "FastToolUK",
        },
        "feature_parameter": {
            "is_product_present": 1,
            "active_store_filter_type": "test",
            "test_variable_dates": 0,
            "control_store_buffer": 1.2,
            "data_continuity_check": 1
        },
        "store_mstr_columns": {
            "banner": "Customer_Group",
            "segment": "Customer_Chain",
            "territory": "Territory",
            "storegrid": "Sub_Channel",
            "partner_id": "Customer_Number",
            "baycount": "",
            "partner_id_backup": "Customer_Number",
            "FSR": "Sales_Representative",
        },
        "Test_store_Partner_ID_backup": "Test_store_Customer_Number",
        "heading_names": {
            "banner": "Banner",
            "segment": "Segment",
            "territory": "Territory",
            "storegrid": "Overall Segment",
            "partner_id": "Customer Name",
            "store_segment": "Store Segment",
            "currency": "£",
        },
        "weekly_target_variable": {
            "banner": "Customer_Group",
            "banner_code": "Store_Number",
            "partner_id": "Customer_Number",
            "rsv": "RSV",
            "volume": "Volume",
            "week_no": "Week Number",
            "year": "Year",
            "segment": "Customer_Chain",
            "week": "Week",
            "overall_segment": "Sub_Channel",
            "territory": "Territory",
            "RSV": "RSV",
            "cbulvl1": "CBU_Lvl1",
            "packformat": "Pack_Format",
        },
        "tables": {
            "control_store_mstr": "[FAST_UK].[Tl_Controlstore_Mstr]",
            "measurement": "[FAST_UK].[Tl_Measurement_Tbl]",
            "record_mstr": "[FAST_UK].[Tl_RecordMstr]",
            "store_mstr": "[FAST_UK].[Tl_StoreMstr]",
            "test_mstr": "[FAST_UK].[Tl_TestMstr]",
            "test_store_map": "[FAST_UK].[Tl_Teststore_map]",
            "weekly_mstr": "[FAST_UK].[Tl_Weekly_target_mst]",
            "upload_stores": "[FAST_UK].[Tl_Upload_store_population]",
            "config_mstr": "[FAST_UK].[Tl_ConfigMstr]",
            "visit_mstr": "[FAST_UK].[Tl_Visit_Data]",
            'pack_mstr':"[FAST_UK].[Tl_Pack_Format]",
            'cbu_mstr':"[FAST_UK].[Tl_CBU_Lvl1]"
        },
        "metadata": {
            "test_configuration": {
                "sales_weeks": 104,
                "sales_lifts_sales_weeks": 52,
                "sales_diff_percentage": 10,
                "power_of_test": 0.7,
                "min_teststores": 30,
                "rawconvfactors": {
                    "CO-OP": 0.18,
                    "ASDA": 0.25,
                    "TESCO": 0.21,
                    "POUNDLAND": 0.15,
                    "SAINSBURY": 0.18,
                    "MORRISONS": 0.21,
                },
            },
            "test_planning": {
                "default_stratification": ["Customer_Group"],
                "test_vs_population_compare": [
                    "total_checkout_locations",
                    "Store_Size_Sq_Ft",
                    "Manned_Checkouts",
                ],
                "test_vs_population_compare_summary": [
                    "Store_Size_Sq_Ft",
                    "Manned_Checkouts",
                ],
                "sampling_iterations": 10,
                "test_vs_population_pvalue": 0.8,
                "test_vs_control_compare": ["Customer_Group", "Customer_Chain"],
                "test_vs_control_compare_summary": [],
                "business_category_specific_compare": [],
                "business_categories_count": 0,
                "test_vs_control_pvalue": 0.8,
                "test_vs_control_similaritymeasure_difference_threshold": 0.05,
                "summary_sales_weeks": 52,
                "validate_datapoints_multiplier": 2,
                "teststores_columns": [
                    "Customer_Number",
                    "Sales_Representative",
                    "Customer_Group",
                    "Territory",
                    "Store_Size_Sq_Ft",
                    "Customer_Chain",
                ],
                "upload_stores_identifier":"Customer_Number",
                "upload_teststores_identifier":'Test_store_Customer_Number',
                "upload_controlstores_identifier":'Control_store_Customer_Number',
                "user_populationstores_columns": {
                    "Customer_Number": "int64"
                },
                "user_teststores_columns": {
                    "Test_store_Customer_Number": "int64"
                },
                "control_storespool_columns": {
                    "Control_store_Customer_Number": "int64"
                },
                "confidence_level": 0.85,
                "similarity_measure": 0.7,
                "correlation": 0.4,
                "margin_of_error": 0.04,
                "power_of_test": 0.7,
                "power_values": [60, 65, 70, 75, 80, 85, 90, 95],
                "user_testcontrolstores_columns": {
                    "Test_store_Customer_Number": "int64",
                    "Control_store_Customer_Number": "int64",
                },
                "control_storespool_columns": {
                    "Control_store_Customer_Number": "int64"
                },
            },
            "test_measurement": {
                "probability_thresholds": [0.60, 0.85, 1],
                "testmeasurement_columns": [
                    "Customer_Number",
                    "Sales_Representative",
                    "Customer_Group",
                    "Territory",
                    "Sub_Channel",
                    "Store_Size_Sq_Ft",
                    "Customer_Chain",
                ],
                "user_customgroup_columns": {
                    "Test_store_Customer_Number": "int64",
                    "Group": "object",
                },
            },
        },
        "filePath": {
            "TestStore": {
                "file_name": "/DSCode/regions/UK/upload_templates/Upload_Teststores_Template_UK.xlsx"
            },
            "controlStore": {
                "file_name": "/DSCode/regions/UK/upload_templates/Test_Control_Pairs_Upload_Template_UK.xlsx"
            },
            "controlStore_Pool": {
                "file_name": "/DSCode/regions/UK/upload_templates/Control_Pairs_Pool_Upload_Template_UK.xlsx"
            },
            "RSV_STORES": {
                "file_name": "/DSCode/regions/UK/upload_templates/Upload_Population_Template_UK.xlsx"
            },
        },
        "excel_header": {
            "test_store": "Test_store_Customer_Number",
            "control_store": "Control_store_Customer_Number",
        },
        "report_generate": {
            "common": {"region_name": "UNITED KINGDOM", "flag_name": "flag_UK.png"},
            "control_compare_variable": ["Touchability_Score", "Store_Size_Sq_Ft"],
            "test_compare_variable": ["Touchability_Score", "Store_Size_Sq_Ft"],
            "store_feature": ["Customer Group"],
            "row_span": 2,
            "matching_criteria": [
                "Customer_Group",
                "Territory",
                "Touchability_Score",
                "Store_Size_Sq_Ft",
            ],
        },
        "result_grid_excel": {
            "header_data": ["Week", "Category", "Metric", "Variable", "Value"],
            "category_format": {
                "Confectionary_Combination_1": "category1",
                "Confectionary_Combination_2": "category2",
                "Confectionary_Combination_3": "category3",
                "Confectionary_Combination_4": "category4",
            },
        },
    }
