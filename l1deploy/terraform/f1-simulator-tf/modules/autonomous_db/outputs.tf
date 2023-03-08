output "_id" {
  value = oci_database_autonomous_database.autonomous_database.id
}

output "urls" {
  value = oci_database_autonomous_database.autonomous_database.connection_urls
}
