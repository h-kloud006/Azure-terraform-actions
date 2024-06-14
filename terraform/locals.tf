locals {
  openai_endpoint_fqdn = "${azurerm_private_endpoint.openai_private_endpoint.name}.${azurerm_cognitive_account.openai.location}.azurewebsites.net"
}