locals {
  openai_endpoint_fqdn = "${azurerm_private_endpoint.openai_private_endpoint.name}.${eastus}.azurewebsites.net"
}