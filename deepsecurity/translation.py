# standard library

# 3rd party libraries

# project libraries

class Terms:
  api_to_new = {
    'antiMalwareClassicPatternVersion': 'anti_malware_classic_pattern_version',
    'antiMalwareEngineVersion': 'anti_malware_engine_version',
    'antiMalwareIntelliTrapExceptionVersion': 'anti_malware_intellitrap_exception_version',
    'antiMalwareIntelliTrapVersion': 'anti_malware_intellitrap_version',
    'antiMalwareSmartScanPatternVersion': 'anti_malware_smartscan_pattern_version',
    'antiMalwareSpywarePatternVersion': 'anti_malware_spyware_pattern_version',
    'cloudObjectImageId': 'cloud_image_id',
    'cloudObjectInstanceId': 'cloud_instance_id',
    'cloudObjectInternalUniqueId': 'cloud_internal_unique_id',
    'cloudObjectSecurityGroupIds': 'cloud_security_group_ids',
    'cloudObjectType': 'cloud_type',
    'componentKlasses': 'component_classes',
    'componentNames': 'component_names',
    'componentTypes': 'component_types',
    'componentVersions': 'component_version',
    'displayName': 'display_name',
    'externalID': 'external_id',
    'hostGroupID': 'computer_group_id',
    'hostGroupName': 'computer_group_name',
    'hostInterfaces': 'computer_interfaces',
    'hostLight': 'computer_status_light',
    'hostType': 'computer_type',
    'lastAnitMalwareScheduledScan': 'last_anti_malware_scheduled_scan',
    'lastAntiMalwareEvent': 'last_anti_malware_event',
    'lastAntiMalwareManualScan': 'last_anti_malware_manual_scan',
    'lastDpiEvent': 'last_intrusion_prevention_event',
    'lastFirewallEvent': 'last_firewall_event',
    'lastIPUsed': 'last_ip_used',
    'lastIntegrityMonitoringEvent': 'last_integrity_monitoring_event',
    'lastLogInspectionEvent': 'last_log_inspection_event',
    'lastWebReputationEvent': 'last_content_filtering_event',
    'overallAntiMalwareStatus': 'overall_anti_malware_status',
    'overallDpiStatus': 'overall_intrusion_prevention_status',
    'overallFirewallStatus': 'overall_firewall_status',
    'overallIntegrityMonitoringStatus': 'overall_integrity_monitoring_status',
    'overallLastRecommendationScan': 'overall_last_recommendation_scan',
    'overallLastSuccessfulCommunication': 'overall_last_successful_communication',
    'overallLastSuccessfulUpdate': 'overall_last_successful_update',
    'overallLastUpdateRequired': 'overall_last_update_required',
    'overallLogInspectionStatus': 'overall_log_inspection_status',
    'overallStatus': 'overall_status',
    'overallVersion': 'overall_version',
    'overallWebReputationStatus': 'overall_content_filtering_status',
    'securityProfileID': 'policy_id',
    'securityProfileName': 'policy_name',
    'virtualName': 'virtual_name',
    'virtualUuid': 'virtual_uuid',
    'parentGroupID': 'parent_group_id',
    'antiMalwareManualID': 'anti_malware_manual_id',
    'antiMalwareManualInherit': 'anti_malware_manual_inherit',
    'antiMalwareRealTimeID': 'anti_malware_real_time_id',
    'antiMalwareRealTimeInherit': 'anti_malware_real_time_inherit',
    'antiMalwareRealTimeScheduleID': 'anti_malware_real_time_schedule_id',
    'antiMalwareScheduledID': 'anti_malware_scheduled_id',
    'antiMalwareScheduledInherit': 'anti_malware_scheduled_inherit',
    'antiMalwareState': 'anti_malware_state',
    'applicationTypeIDs': 'application_type_ids',
    'firewallRuleIDs': 'firewall_rule_ids',
    'firewallState': 'firewall_state',
    'integrityRuleIDs': 'integrity_rule_ids',
    'integrityState': 'integrity_state',
    'logInspectionRuleIDs': 'log_inspection_rule_ids',
    'logInspectionState': 'log_inspection_state',
    'parentSecurityProfileID': 'parent_policy_id',
    'recommendationState': 'recommedation_state',
    'scheduleID': 'schedule_id',
    'statefulConfigurationID': 'stateful_configuration_id',
    }

  @classmethod
  def get_reverse(self, new_term):
    result = new_term
    for api, new in Terms.api_to_new.items():
      if new == new_term:
        result = api

    return result

  @classmethod
  def get(self, api_term):
    """
    Return the translation of the specified API term
    """
    if Terms.api_to_new.has_key(api_term):
      return self.api_to_new[api_term]
    else:
      return api_term