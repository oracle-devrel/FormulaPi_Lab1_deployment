output "apex_url" {
  value = lower(lookup(data.oci_database_autonomous_database.provisioned_autonomous_database.connection_urls[0],"apex_url"))
}

output "db_schema" {
  value = var.DB_SCHEMA
}