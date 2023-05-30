
output "admin_db_password" {
  value = nonsensitive(module.db_admin_password.content)
}

output "user_db_password" {
  value = nonsensitive(module.db_user_password.content)
}

output "leaderboard_url" {
  value = lower(replace(lookup(data.oci_database_autonomous_database.provisioned_autonomous_database.connection_urls[0],"apex_url"),"apex","r/${var.APEX_WORKSPACE}/change_me1/home"))
}

output "registration_url" {
  value = lower(replace(lookup(data.oci_database_autonomous_database.provisioned_autonomous_database.connection_urls[0],"apex_url"),"apex","r/${var.APEX_WORKSPACE}/change_me2/registration"))
}

output "tns_admin" {
  value = abspath(module.wallet.directory)
}

output "db_schema" {
  value = var.DB_SCHEMA
}
