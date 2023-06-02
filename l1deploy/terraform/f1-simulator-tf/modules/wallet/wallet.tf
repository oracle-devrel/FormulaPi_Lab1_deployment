resource "oci_database_autonomous_database_wallet" "wallet" {
  autonomous_database_id  = var.db_id
  password                = var.wallet_password
  base64_encode_content   = "true"
  generate_type           = "SINGLE"
}

resource "local_file" "wallet_zip" {
  depends_on = [
    oci_database_autonomous_database_wallet.wallet
  ]
  content_base64 = oci_database_autonomous_database_wallet.wallet.content
  filename       = "${var.wallet_install_dir}/wallet.zip"
}
