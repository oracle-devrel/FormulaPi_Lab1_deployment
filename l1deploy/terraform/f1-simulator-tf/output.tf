output "apex_url" {
  description = "URL for access the APEX App Builder (to build your leaderboard)"
  value = lower(lookup(data.oci_database_autonomous_database.provisioned_autonomous_database.connection_urls[0],"apex_url"))
}

output "ssh_command" {
  description = "Syntax for connecting to OCI Compute Instance"
  value = "ssh -i ~/.ssh/id_rsa opc@${module.f1sim_instance.public_ip_all_attributes["0"].ip_address}"
}

output "apex_workspace" {
  description = "Used for APEX Workspace Name to log into the APEX App Builder"
  value = var.APEX_WORKSPACE
}

output "apex_user" {
  description = "Used for APEX User Name to log into the APEX App Builder"
  value = var.DB_SCHEMA
}

output "apex_credentials" {
  description = "Used for APEX User Credentials to login into the APEX App Builder"
  value = nonsensitive(module.db_user_password.content)
}

output "dbusername" {
  description = "Used for dbusername in Data Ingestion f1store.yaml configuration"
  value = upper(var.DB_USER)
}

output "dbpassword" {
  description = "Used for dbpassword in Data Ingestion f1store.yaml configuration"
  value = nonsensitive(module.db_user_password.content)
}

output "dburl" {
  description = "Used for dburl in Data Ingestion f1store.yaml configuration"
  value = "${lower(data.oci_database_autonomous_database.provisioned_autonomous_database.db_name)}_low"
}

output "dbwalletpassword" {
  description = "Used for dbwalletpassword in Data Ingestion f1store.yaml configuration"
  value = nonsensitive(module.db_admin_password.content)
}
