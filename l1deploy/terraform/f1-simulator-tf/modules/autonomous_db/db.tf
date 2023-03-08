resource "oci_database_autonomous_database" "autonomous_database" {
  compartment_id                      = var.compartment_id
  db_name                             = var.display_name
  display_name                        = var.display_name
  admin_password                      = var.admin_password
  cpu_core_count                      = var.cpu_core_count
  data_storage_size_in_tbs            = var.data_storage_size_in_tbs
  db_workload                         = var.db_workload
  db_version                          = "19c"

  customer_contacts {
    email                             = var.customer_contacts
  }

  freeform_tags                       = var.freeform_tags
  is_auto_scaling_enabled             = false
  is_auto_scaling_for_storage_enabled = false
  is_dedicated                        = false
  is_free_tier                        = var.is_free_tier
  license_model                       = "LICENSE_INCLUDED"
  open_mode                           = "READ_WRITE"
  permission_level                    = "UNRESTRICTED"
  state                               = "AVAILABLE"
  operations_insights_status          = "NOT_ENABLED"
  data_safe_status                    = "NOT_REGISTERED"

  nsg_ids = [
  ]
  standby_whitelisted_ips = [
  ]
  whitelisted_ips = [
  ]
}
