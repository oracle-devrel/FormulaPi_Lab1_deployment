# variable "subnet_id" {}
variable "display_name" {}
variable "compartment_id" {}
variable "admin_password" {
  sensitive = true
}
variable "cpu_core_count" {
  default = 1
}
variable "freeform_tags" {}
variable "data_storage_size_in_tbs" {
  default = 1
}
variable "db_workload" {
  type = string
  default = "OLTP"
}
variable "customer_contacts" {}
variable "is_free_tier" {}
