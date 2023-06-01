output "apex_url" {
  value = lower(lookup(data.oci_database_autonomous_database.provisioned_autonomous_database.connection_urls[0],"apex_url"))
}

output "ssh_command" {
  value = "ssh -i ~/.ssh/id_rsa opc@${module.f1sim_instance.public_ip_all_attributes["0"].ip_address}"
}

output "db_schema" {
  value = var.DB_SCHEMA
}

output "db_password" {
  value = nonsensitive(module.db_user_password.content)
}

output "db_admin" {
  value = nonsensitive(module.db_admin_password.content)
}

output "db_wallet" {
  value = nonsensitive(module.wallet_password.content)
}
