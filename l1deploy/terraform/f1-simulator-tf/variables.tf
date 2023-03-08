variable "region" {
  # List of regions: https://docs.cloud.oracle.com/iaas/Content/General/Concepts/regions.htm#ServiceAvailabilityAcrossRegions
  description = "The OCI region where resources will be created."
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
  default = "https://rooms.opcvr.com/packages/"
}
variable package_install {
  type = string
  default = "f1-simulator-cloud/f1-simulator-cloud-v4_0_0-20.tar.gz"
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
  default = "W3lc0m3SIM123"
  sensitive = true 
}

variable ADMIN_PASSWORD {
  default = "W3lc0m3SIM123!#"
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

variable "install_jdk11" {
  default = true
  description = "possibly may be required for sqlcl"
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

variable "instance_ad_number" {
  description = "The availability domain number of the instance. If none is provided, it will start with AD-1 and continue in round-robin."
  type        = number
  default     = 1
}

variable "instance_count" {
  description = "Number of identical instances to launch from a single module."
  type        = number
  default     = 1
}

variable "instance_display_name" {
  description = "(Updatable) A user-friendly name for the instance. Does not have to be unique, and it's changeable."
  type        = string
  default     = "module_instance_nonflex"
}

variable "instance_flex_memory_in_gbs" {
  type        = number
  description = "(Updatable) The total amount of memory available to the instance, in gigabytes."
  default     = null
}

variable "instance_flex_ocpus" {
  type        = number
  description = "(Updatable) The total number of OCPUs available to the instance."
  default     = null
}

variable "instance_state" {
  type        = string
  description = "(Updatable) The target state for the instance. Could be set to RUNNING or STOPPED."
  default     = "RUNNING"

  validation {
    condition     = contains(["RUNNING", "STOPPED"], var.instance_state)
    error_message = "Accepted values are RUNNING or STOPPED."
  }
}

variable "shape" {
  description = "The shape of an instance."
  type        = string
  default     = "VM.Standard2.1"
}

variable "cloud_agent_plugins" {
  description = "Whether each Oracle Cloud Agent plugins should be ENABLED or DISABLED."
  type        = map(string)
  default = {
    autonomous_linux       = "ENABLED"
    bastion                = "ENABLED"
    block_volume_mgmt      = "DISABLED"
    custom_logs            = "ENABLED"
    management             = "DISABLED"
    monitoring             = "ENABLED"
    osms                   = "ENABLED"
    run_command            = "ENABLED"
    vulnerability_scanning = "ENABLED"
    java_management_service = "DISABLED"
  }
}
variable "source_ocid" {
  description = "The OCID of an image or a boot volume to use, depending on the value of source_type."
  type        = string
}

variable "source_type" {
  description = "The source type for the instance."
  type        = string
  default     = "image"
}

# operating system parameters
variable "ssh_public_keys" {
  description = "Public SSH keys to be included in the ~/.ssh/authorized_keys file for the default user on the instance. To provide multiple keys, see docs/instance_ssh_keys.adoc."
  type        = string
  default     = null
}

# networking parameters

variable "assign_public_ip" {
  description = "Whether the VNIC should be assigned a public IP address."
  type        = bool
  default     = false
}

variable "public_ip" {
  description = "Whether to create a Public IP to attach to primary vnic and which lifetime. Valid values are NONE, RESERVED or EPHEMERAL."
  type        = string
  default     = "NONE"
}

# storage parameters

variable "boot_volume_backup_policy" {
  description = "Choose between default backup policies : gold, silver, bronze. Use disabled to affect no backup policy on the Boot Volume."
  type        = string
  default     = "disabled"
}

variable "block_storage_sizes_in_gbs" {
  description = "Sizes of volumes to create and attach to each instance."
  type        = list(string)
  default     = [50]
}

# variable "primary_vnic_nsg_ids" {
#   description = "A list of the OCIDs of the network security groups (NSGs) to add the primary VNIC to"
#   type        = list(string)
#   default     = null
# }

variable "local_cidr_block" {
  description = "A CIDR block used to secure public internet access."
  type        = string
  default     = "0.0.0.0/0"
}

