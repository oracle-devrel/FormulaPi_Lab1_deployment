output "apex_url" {
  value = lower(lookup(data.oci_database_autonomous_database.provisioned_autonomous_database.connection_urls[0],"apex_url"))
}

# output "admin_db_password" {
#   value = nonsensitive(module.db_admin_password.content)
# }

# output "user_db_password" {
#   value = nonsensitive(module.db_user_password.content)
# }

output "db_schema" {
  value = var.DB_SCHEMA
}

# output "f1sim_instance_ip" {
# #   depends_on = [time_sleep.wait_30_seconds]
# #   value = module.f1sim_instance.public_ip[0]["ip_address"]
#   value = try(module.f1sim_instance.public_ip[0]["ip_address"], "")

# }

# output "primary_vnic_nsg_ids" {
#  value = data.oci_core_network_security_group.NSGs
# }