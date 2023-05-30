module "base" {
  source  = "oracle-terraform-modules/iam/oci"
  version = "2.0.2"
}

module "db_admin_password" {
  source = "./modules/password"
  password = var.ADMIN_PASSWORD
}

module "db" {
  count = var.create_database ? 1 : 0

  source = "./modules/autonomous_db"
  depends_on = [
    module.db_admin_password,
  ]

  is_free_tier             = var.IS_FREE_TIER
  db_workload              = var.autonomous_database_type
  cpu_core_count           = var.autonomous_database_cpu_core_count
  data_storage_size_in_tbs = var.autonomous_database_data_storage_size_in_tbs
  admin_password           = module.db_admin_password.content
  compartment_id           = var.compartment_ocid
  display_name             = var.ADB_NAME
  freeform_tags            = var.freeform_tags["db"]
  customer_contacts        = var.customer_contacts
}

module "wallet_password" {
  source = "./modules/password"
  password = var.ADMIN_PASSWORD
}

module "wallet" {
  source = "./modules/wallet"
  depends_on = [
    module.db,
    module.wallet_password
  ]

  db_id  = var.create_database ? module.db[0]._id : var.database
  wallet_password = module.wallet_password.content
  wallet_install_dir = var.INSTALL_HOME
}

module "db_user_password" {
  source = "./modules/password"
  password = var.DB_PASSWORD
}

module "database_configuration" {
  source = "git::http://github.com/denismakogon/terraform-run-bash-script-module.git?ref=main"
  
  depends_on = [
    module.db_admin_password,
    module.db_user_password,
    module.wallet,
  ]

  environment = {
    PACKAGE_BASEURL=var.package_baseurl,
    PACKAGE_NAME=var.package_install,
    INSTALL_HOME=var.INSTALL_HOME,
    WALLET_DIR=var.INSTALL_HOME,
    ADB_NAME=var.create_database ? var.ADB_NAME : data.oci_database_autonomous_database.provisioned_autonomous_database.db_name,
    DB_USER=upper(var.DB_USER),
    DB_PASSWORD=nonsensitive(module.db_user_password.content),
    DB_SCHEMA=upper(var.DB_SCHEMA),
    APEX_WORKSPACE=upper(var.APEX_WORKSPACE),
    ADMIN_PASSWORD=nonsensitive(module.db_admin_password.content),
  }

  create_command = "chmod 755 ./scripts/*.sh && ./scripts/run_configuration.sh"
  # destroy_command = "rm -fr ${var.INSTALL_HOME}"
}

data "oci_database_autonomous_database" "provisioned_autonomous_database" {
  autonomous_database_id = var.create_database ? module.db[0]._id : var.database
}
