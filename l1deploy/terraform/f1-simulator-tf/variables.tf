variable "region" {
  # List of regions: https://docs.cloud.oracle.com/iaas/Content/General/Concepts/regions.htm#ServiceAvailabilityAcrossRegions
  description = "The OCI region where OKE resources will be created."
  type        = string
}

variable "tenancy_ocid" {
  description = "The tenancy id of the OCI Cloud Account in which to create the resources."
  type        = string
}

variable "compartment_ocid" {
  description = "The compartment id where to create all resources."
  type        = string
}

variable package_baseurl {
  type = string
  default = "https://apigw.withoracle.cloud/livelaps/rdm/packages/"
}
variable package_install {
  type = string
  default = "f1-simulator-cloud/f1-simulator-cloud-v5_0_0-20.tar.gz"
}

variable IS_FREE_TIER {
  default = "true"
}

variable INSTALL_HOME {
  default = ".local"
}

variable ADB_NAME {
  default = "f1simdb"
}

variable DB_USER {
  default = "SIMUSER"
}

variable DB_SCHEMA {
  default = "SIMUSER" 
}

variable APEX_WORKSPACE {
  default = "LIVELAPS" 
}

variable DB_PASSWORD {
  default = "F1simDB123"
  sensitive = true 
}

variable ADMIN_PASSWORD {
  default = "F1simDB123!#"
  sensitive = true
}

variable "autonomous_database_type" {
  default = "OLTP"
}

variable "autonomous_database_cpu_core_count" {
  default = 1
}

variable "autonomous_database_data_storage_size_in_tbs" {
  default = 1
}

variable "customer_contacts" {
  default = "demo@withoracle.cloud"
}

variable "freeform_tags" {
  default = {
    vm = {}
    db = {}
    vcn = {}
  }
  description = "Tags to apply to different resources."
  type        = map(any)
}

variable "database_compartment" {
  default = ""
}

variable "database" {
  default = ""
}

variable "create_database" {
  default = "true"
}