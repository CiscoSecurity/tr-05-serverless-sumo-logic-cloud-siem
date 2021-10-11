EXPECTED_RESPONSE_OF_JWKS_ENDPOINT = {
    "keys": [
        {
            "kty": "RSA",
            "n": "tSKfSeI0fukRIX38AHlKB1YPpX8PUYN2JdvfM-XjNmLfU1M74N0V"
                 "mdzIX95sneQGO9kC2xMIE-AIlt52Yf_KgBZggAlS9Y0Vx8DsSL2H"
                 "vOjguAdXir3vYLvAyyHin_mUisJOqccFKChHKjnk0uXy_38-1r17"
                 "_cYTp76brKpU1I4kM20M__dbvLBWjfzyw9ehufr74aVwr-0xJfsB"
                 "Vr2oaQFww_XHGz69Q7yHK6DbxYO4w4q2sIfcC4pT8XTPHo4JZ2M7"
                 "33Ea8a7HxtZS563_mhhRZLU5aynQpwaVv2U--CL6EvGt8TlNZOke"
                 "Rv8wz-Rt8B70jzoRpVK36rR-pHKlXhMGT619v82LneTdsqA25Wi2"
                 "Ld_c0niuul24A6-aaj2u9SWbxA9LmVtFntvNbRaHXE1SLpLPoIp8"
                 "uppGF02Nz2v3ld8gCnTTWfq_BQ80Qy8e0coRRABECZrjIMzHEg6M"
                 "loRDy4na0pRQv61VogqRKDU2r3_VezFPQDb3ciYsZjWBr3HpNOkU"
                 "jTrvLmFyOE9Q5R_qQGmc6BYtfk5rn7iIfXlkJAZHXhBy-ElBuiBM"
                 "-YSkFM7dH92sSIoZ05V4MP09Xcppx7kdwsJy72Sust9Hnd9B7V35"
                 "YnVF6W791lVHnenhCJOziRmkH4xLLbPkaST2Ks3IHH7tVltM6NsR"
                 "k3jNdVM",
            "e": "AQAB",
            "alg": "RS256",
            "kid": "02B1174234C29F8EFB69911438F597FF3FFEE6B7",
            "use": "sig"
        }
    ]
}

RESPONSE_OF_JWKS_ENDPOINT_WITH_WRONG_KEY = {
    "keys": [
        {
            "kty": "RSA",
            "n": "pSKfSeI0fukRIX38AHlKB1YPpX8PUYN2JdvfM-XjNmLfU1M74N0V"
                 "mdzIX95sneQGO9kC2xMIE-AIlt52Yf_KgBZggAlS9Y0Vx8DsSL2H"
                 "vOjguAdXir3vYLvAyyHin_mUisJOqccFKChHKjnk0uXy_38-1r17"
                 "_cYTp76brKpU1I4kM20M__dbvLBWjfzyw9ehufr74aVwr-0xJfsB"
                 "Vr2oaQFww_XHGz69Q7yHK6DbxYO4w4q2sIfcC4pT8XTPHo4JZ2M7"
                 "33Ea8a7HxtZS563_mhhRZLU5aynQpwaVv2U--CL6EvGt8TlNZOke"
                 "Rv8wz-Rt8B70jzoRpVK36rR-pHKlXhMGT619v82LneTdsqA25Wi2"
                 "Ld_c0niuul24A6-aaj2u9SWbxA9LmVtFntvNbRaHXE1SLpLPoIp8"
                 "uppGF02Nz2v3ld8gCnTTWfq_BQ80Qy8e0coRRABECZrjIMzHEg6M"
                 "loRDy4na0pRQv61VogqRKDU2r3_VezFPQDb3ciYsZjWBr3HpNOkU"
                 "jTrvLmFyOE9Q5R_qQGmc6BYtfk5rn7iIfXlkJAZHXhBy-ElBuiBM"
                 "-YSkFM7dH92sSIoZ05V4MP09Xcppx7kdwsJy72Sust9Hnd9B7V35"
                 "YnVF6W791lVHnenhCJOziRmkH4xLLbPkaST2Ks3IHH7tVltM6NsR"
                 "k3jNdVM",
            "e": "AQAB",
            "alg": "RS256",
            "kid": "02B1174234C29F8EFB69911438F597FF3FFEE6B7",
            "use": "sig"
        }
    ]
}

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

INSIGHTS = \
    [
        {
            "artifacts": [],
            "assignedTo": None,
            "assignee": None,
            "closed": None,
            "closedBy": None,
            "confidence": None,
            "created": "2021-10-05T21:01:17.404626",
            "description": "Test rule",
            "entity": {
                "entityType": "_hostname",
                "hostname": "AD.lan.cyberthre.at",
                "id": "_hostname-AD.lan.cyberthre.at",
                "macAddress": None,
                "name": "AD.lan.cyberthre.at",
                "sensorZone": "",
                "value": "AD.lan.cyberthre.at"
            },
            "id": "5894b5c4-cb1b-4164-839e-433fb9b06780",
            "lastUpdated": "2021-10-05T21:01:17.404620",
            "lastUpdatedBy": None,
            "name": "Unspecified Malicious Activity",
            "orgId": "00000000009BCE86",
            "readableId": "INSIGHT-8",
            "recordSummaryFields": [],
            "resolution": None,
            "severity": "LOW",
            "signals": [
                {
                    "allRecords": [
                        {
                            "_cipCollector": "AD",
                            "_cipCollectorId": 226372374,
                            "_cipEncoding": "UTF8",
                            "_cipFormat": "t:none:o:0:l:0:p:null",
                            "_cipMessageTime": 1633044768966,
                            "_cipSource": "Windows Events",
                            "_cipSourceId": 1419227751,
                            "bro_dns_answers": [],
                            "bro_file_bytes": {},
                            "bro_file_connUids": [],
                            "bro_flow_service": [],
                            "bro_ftp_pendingCommands": [],
                            "bro_http_cookieVars": [],
                            "bro_http_origFuids": [],
                            "bro_http_origMimeTypes": [],
                            "bro_http_request_headers": {},
                            "bro_http_request_proxied": [],
                            "bro_http_response_headers": {},
                            "bro_http_response_respFuids": [],
                            "bro_http_response_respMimeTypes": [],
                            "bro_http_tags": [],
                            "bro_http_uriVars": [],
                            "bro_kerberos_clientCert": {},
                            "bro_kerberos_serverCert": {},
                            "bro_sip_headers": {},
                            "bro_sip_requestPath": [],
                            "bro_sip_responsePath": [],
                            "bro_ssl_certChainFuids": [],
                            "bro_ssl_clientCertChainFuids": [],
                            "cseSignal": {},
                            "day": 30,
                            "description": "The computer attempted to "
                                           "validate the credentials "
                                           "for an account",
                            "device_hostname": "AD.lan.cyberthre.at",
                            "device_hostname_raw": "AD.lan.cyberthre.at",
                            "dstDevice_hostname": "AD.lan.cyberthre.at",
                            "dstDevice_hostname_raw": "AD.lan.cyberthre.at",
                            "errorCode": "0x0",
                            "fieldTags": {},
                            "fields": {
                                "Channel": "Security",
                                "Computer": "AD.lan.cyberthre.at",
                                "EventData.PackageName": "MICROSOFT_"
                                                         "AUTHENTICATION_"
                                                         "PACKAGE_V1_0",
                                "EventData.Status": "0x0",
                                "EventData.TargetUserName": "iaredden",
                                "EventData.Workstation": "IANSPC",
                                "EventID": "4776",
                                "EventRecordID": "1832813",
                                "Execution.ProcessID": "668",
                                "Execution.ThreadID": "4824",
                                "Keywords": "Audit Success",
                                "Level": "Information",
                                "Message": "The computer attempted to "
                                           "validate the credentials for "
                                           "an account.\r\n\r\n"
                                           "Authentication Package:"
                                           "\tMICROSOFT_"
                                           "AUTHENTICATION_PACKAGE_"
                                           "V1_0\r\nLogon Account:"
                                           "\tiaredden\r\nSource "
                                           "Workstation:"
                                           "\tIANSPC\r\nError "
                                           "Code:\t0x0",
                                "Opcode": "Info",
                                "Provider.Guid": "{54849625-5478-"
                                                 "4994-a5ba-3e3b0328c30d}",
                                "Provider.Name": "Microsoft-Windows"
                                                 "-Security-Auditing",
                                "Task": "14336",
                                "TimeCreated": "2021-09-30T23:"
                                               "32:48.9665281Z",
                                "TimeCreated.SystemTime": "2021-09-30T23"
                                                          ":32:48.9665281Z",
                                "Version": "0"
                            },
                            "friendlyName": "record",
                            "hour": 23,
                            "http_requestHeaders": {},
                            "listMatches": [],
                            "matchedItems": [],
                            "metadata_deviceEventId": "Security-4776",
                            "metadata_mapperName": "Windows - Security - 4776",
                            "metadata_mapperUid": "8fda2f9a-dc3c-"
                                                  "4e40-872a-8fa03a8d997b",
                            "metadata_orgId": "00000000009BCE86",
                            "metadata_parseTime": 1633045000254,
                            "metadata_product": "Windows",
                            "metadata_productGuid": "1ff7546c-cb36-"
                                                    "4a24-87f7-89d2cecc5761",
                            "metadata_receiptTime": 1633044974,
                            "metadata_schemaVersion": 3,
                            "metadata_sensorId": "00000000009BCE86",
                            "metadata_sensorInformation": {},
                            "metadata_sensorZone": "default",
                            "metadata_sourceCategory": "windows/events",
                            "metadata_sourceMessageId": "926239561495595010",
                            "metadata_vendor": "Microsoft",
                            "month": 9,
                            "objectType": "Authentication",
                            "srcDevice_hostname": "IANSPC",
                            "srcDevice_hostname_raw": "IANSPC",
                            "success": True,
                            "timestamp": 1633044768966,
                            "uid": "f9bb0d47-9357-5573-"
                                   "ba4f-1e6c1103faea",
                            "user_username": "iaredden",
                            "user_username_raw": "iaredden",
                            "year": 2021
                        }
                    ],
                    "artifacts": [],
                    "contentType": "RULE",
                    "description": "Test rule",
                    "id": "c0942d9a-6bb9-59f3-b172-395e8fc09136",
                    "name": "Device hostname signal",
                    "recordCount": 1,
                    "recordTypes": [],
                    "ruleId": "MATCH-U00001",
                    "severity": 1,
                    "stage": "Unknown/Other",
                    "tags": [
                        "Tactic"
                    ],
                    "timestamp": "2021-09-30T23:32:48.966000"
                }
            ],
            "source": "USER",
            "status": {
                "displayName": "New",
                "name": "new"
            },
            "subResolution": None,
            "tags": [
                "Tactic"
            ],
            "teamAssignedTo": None,
            "timeToDetection": 422908.438626,
            "timeToRemediation": None,
            "timeToResponse": None,
            "timestamp": "2021-09-30T23:32:48.966000"
        },
        {
            "artifacts": [],
            "assignedTo": None,
            "assignee": None,
            "closed": None,
            "closedBy": None,
            "confidence": None,
            "created": "2021-10-05T21:01:25.235846",
            "description": "Test rule",
            "entity": {
                "entityType": "_hostname",
                "hostname": "AD.lan.cyberthre.at",
                "id": "_hostname-AD.lan.cyberthre.at",
                "macAddress": None,
                "name": "AD.lan.cyberthre.at",
                "sensorZone": "",
                "value": "AD.lan.cyberthre.at"
            },
            "id": "99117227-ebb0-442f-8b27-78f3f8dd5223",
            "lastUpdated": "2021-10-05T21:01:25.235841",
            "lastUpdatedBy": None,
            "name": "Unspecified Malicious Activity",
            "orgId": "00000000009BCE86",
            "readableId": "INSIGHT-9",
            "recordSummaryFields": [],
            "resolution": None,
            "severity": "LOW",
            "signals": [
                {
                    "allRecords": [
                        {
                            "_cipCollector": "AD",
                            "_cipCollectorId": 226372374,
                            "_cipEncoding": "UTF8",
                            "_cipFormat": "t:none:o:0:l:0:p:null",
                            "_cipMessageTime": 1633044768966,
                            "_cipSource": "Windows Events",
                            "_cipSourceId": 1419227751,
                            "bro_dns_answers": [],
                            "bro_file_bytes": {},
                            "bro_file_connUids": [],
                            "bro_flow_service": [],
                            "bro_ftp_pendingCommands": [],
                            "bro_http_cookieVars": [],
                            "bro_http_origFuids": [],
                            "bro_http_origMimeTypes": [],
                            "bro_http_request_headers": {},
                            "bro_http_request_proxied": [],
                            "bro_http_response_headers": {},
                            "bro_http_response_respFuids": [],
                            "bro_http_response_respMimeTypes": [],
                            "bro_http_tags": [],
                            "bro_http_uriVars": [],
                            "bro_kerberos_clientCert": {},
                            "bro_kerberos_serverCert": {},
                            "bro_sip_headers": {},
                            "bro_sip_requestPath": [],
                            "bro_sip_responsePath": [],
                            "bro_ssl_certChainFuids": [],
                            "bro_ssl_clientCertChainFuids": [],
                            "cseSignal": {},
                            "day": 30,
                            "description": "The computer attempted to "
                                           "validate the credentials for "
                                           "an account",
                            "device_hostname": "AD.lan.cyberthre.at",
                            "device_hostname_raw": "AD.lan.cyberthre.at",
                            "dstDevice_hostname": "AD.lan.cyberthre.at",
                            "dstDevice_hostname_raw": "AD.lan.cyberthre.at",
                            "errorCode": "0x0",
                            "fieldTags": {},
                            "fields": {
                                "Channel": "Security",
                                "Computer": "AD.lan.cyberthre.at",
                                "EventData.PackageName": "MICROSOFT_"
                                                         "AUTHENTICATION"
                                                         "_PACKAGE_V1_0",
                                "EventData.Status": "0x0",
                                "EventData.TargetUserName": "iaredden",
                                "EventData.Workstation": "IANSPC",
                                "EventID": "4776",
                                "EventRecordID": "1832813",
                                "Execution.ProcessID": "668",
                                "Execution.ThreadID": "4824",
                                "Keywords": "Audit Success",
                                "Level": "Information",
                                "Message": "The computer attempted to "
                                           "validate the credentials for "
                                           "an account.\r\n\r\n"
                                           "Authentication "
                                           "Package:\tMICROSOFT_"
                                           "AUTHENTICATION_"
                                           "PACKAGE_V1_0\r\nLogon "
                                           "Account:"
                                           "\tiaredden\r\nSource "
                                           "Workstation:"
                                           "\tIANSPC\r\nError "
                                           "Code:\t0x0",
                                "Opcode": "Info",
                                "Provider.Guid": "{54849625-5478-"
                                                 "4994-a5ba-3e3b0328c30d}",
                                "Provider.Name": "Microsoft-Windows"
                                                 "-Security-Auditing",
                                "Task": "14336",
                                "TimeCreated": "2021-09-30T23:32:48"
                                               ".9665281Z",
                                "TimeCreated.SystemTime": "2021-09-30T23:32:48"
                                                          ".9665281Z",
                                "Version": "0"
                            },
                            "friendlyName": "record",
                            "hour": 23,
                            "http_requestHeaders": {},
                            "listMatches": [],
                            "matchedItems": [],
                            "metadata_deviceEventId": "Security-4776",
                            "metadata_mapperName": "Windows - Security - 4776",
                            "metadata_mapperUid": "8fda2f9a-dc3c-"
                                                  "4e40-872a-8fa03a8d997b",
                            "metadata_orgId": "00000000009BCE86",
                            "metadata_parseTime": 1633045000254,
                            "metadata_product": "Windows",
                            "metadata_productGuid": "1ff7546c-cb36-"
                                                    "4a24-87f7-89d2cecc5761",
                            "metadata_receiptTime": 1633044974,
                            "metadata_schemaVersion": 3,
                            "metadata_sensorId": "00000000009BCE86",
                            "metadata_sensorInformation": {},
                            "metadata_sensorZone": "default",
                            "metadata_sourceCategory": "windows/events",
                            "metadata_sourceMessageId": "926239561495595010",
                            "metadata_vendor": "Microsoft",
                            "month": 9,
                            "objectType": "Authentication",
                            "srcDevice_hostname": "IANSPC",
                            "srcDevice_hostname_raw": "IANSPC",
                            "success": True,
                            "timestamp": 1633044768966,
                            "uid": "f9bb0d47-9357-5573-ba4f-1e6c1103faea",
                            "user_username": "iaredden",
                            "user_username_raw": "iaredden",
                            "year": 2021
                        }
                    ],
                    "artifacts": [],
                    "contentType": "RULE",
                    "description": "Test rule",
                    "id": "c0942d9a-6bb9-59f3-b172-395e8fc09136",
                    "name": "Device hostname signal",
                    "recordCount": 1,
                    "recordTypes": [],
                    "ruleId": "MATCH-U00001",
                    "severity": 1,
                    "stage": "Unknown/Other",
                    "tags": [
                        "Tactic"
                    ],
                    "timestamp": "2021-09-30T23:32:48.966000"
                }
            ],
            "source": "USER",
            "status": {
                "displayName": "New",
                "name": "new"
            },
            "subResolution": None,
            "tags": [
                "Tactic"
            ],
            "teamAssignedTo": None,
            "timeToDetection": 422916.269846,
            "timeToRemediation": None,
            "timeToResponse": None,
            "timestamp": "2021-09-30T23:32:48.966000"
        }
    ]

INSIGHT_SIGHTINGS = [
    {
        "confidence": "High",
        "count": 1,
        "description": "Test rule",
        "external_ids": [
            "5894b5c4-cb1b-4164-839e-433fb9b06780",
            "INSIGHT-8"
        ],
        "id": "sighting-c08bdfac-9ee7-5dc2-9530-c3d4bcdddac1",
        "internal": True,
        "observables": [
            {
                "type": "domain",
                "value": "cisco.com"
            }
        ],
        "observed_time": {
            "start_time": "2021-10-05T21:01:17.404626"
        },
        "resolution": "Unresolved",
        "schema_version": "1.1.8",
        "severity": "Low",
        "short_description": "Signal: INSIGHT-8-Unspecified "
                             "Malicious Activity for entity "
                             "AD.lan.cyberthre.at contains the "
                             "observable. 1 unique signals of 1 total.",
        "source": "Sumo Logic Cloud SIEM Enterprise",
        "source_uri": "https://service.us2.sumologic.com/"
                      "sec/insight/5894b5c4-cb1b-4164-839e-433fb9b06780",
        "targets": [
            {
                "observables": [
                    {
                        "type": "hostname",
                        "value": "AD.lan.cyberthre.at"
                    }
                ],
                "observed_time": {
                    "start_time": "2021-09-30T23:32:48.966000"
                },
                "type": "Entity"
            }
        ],
        "title": "A Sumo Logic Cloud "
                 "SIEM Insight contains observable in a Signal",
        "type": "sighting"
    },
    {
        "confidence": "High",
        "count": 1,
        "description": "Test rule",
        "external_ids": [
            "99117227-ebb0-442f-8b27-78f3f8dd5223",
            "INSIGHT-9"
        ],
        "id": "sighting-ee70b6b2-ea78-579c-bfeb-8e8a861c3734",
        "internal": True,
        "observables": [
            {
                "type": "domain",
                "value": "cisco.com"
            }
        ],
        "observed_time": {
            "start_time": "2021-10-05T21:01:25.235846"
        },
        "resolution": "Unresolved",
        "schema_version": "1.1.8",
        "severity": "Low",
        "short_description": "Signal: INSIGHT-9-Unspecified "
                             "Malicious Activity for entity "
                             "AD.lan.cyberthre.at contains the "
                             "observable. 1 unique signals of 1 total.",
        "source": "Sumo Logic Cloud SIEM Enterprise",
        "source_uri": "https://service.us2.sumologic.com"
                      "/sec/insight/99117227-ebb0-442f-8b27-78f3f8dd5223",
        "targets": [
            {
                "observables": [
                    {
                        "type": "hostname",
                        "value": "AD.lan.cyberthre.at"
                    }
                ],
                "observed_time": {
                    "start_time": "2021-09-30T23:32:48.966000"
                },
                "type": "Entity"
            }
        ],
        "title": "A Sumo Logic Cloud SIEM "
                 "Insight contains observable in a Signal",
        "type": "sighting"
    }
]

INDICATORS = [
    {
        "external_references": {
            "description": "Test rule",
            "external_id": "MATCH-U00001",
            "source_name": "Sumo Logic Cloud SIEM Enterprise",
            "url": "https://service.us2.sumologic.com/sec/content/rules"
                   "/rule/MATCH-U00001"
        },
        "id": "indicator-9692a26b-2f2c-5deb-8178-4e359a1fe1fd",
        "producer": "Sumo Logic",
        "schema_version": "1.1.8",
        "severity": 1,
        "short_description": "Test rule",
        "source_uri": "https://service.us2.sumologic.com/sec/content/rules"
                      "/rule/MATCH-U00001",
        "tags": [
            "Tactic"
        ],
        "type": "indicator",
        "valid_time": {
            "start_time": "2021-09-30T23:32:48.966000"
        }
    }
]

OBSERVE_OBSERVABLES_RESPONSE = {
    "data": {
        "indicators": {
            "count": 1,
            "docs": INDICATORS
        },
        "sightings": {
            "count": 2,
            "docs": INSIGHT_SIGHTINGS
        }
    }
}

REFER_RESPONSE = {
    "data": [
        {
            "categories": [
                "Search",
                "SumoLogic",
                "Cloud SIEM Enterprise"
            ],
            "description": "Lookup this domain on Sumo Logic Cloud SIEM "
                           "Enterprise console",
            "id": "ref-sumo-search-logic-cse-domain-cisco.com",
            "title": "Search for this domain",
            "url": "https://service.us2.sumologic.com/sec/search?q=cisco.com"
        }
    ]
}
