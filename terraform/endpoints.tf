
resource "azurerm_private_endpoint" "openai_private_endpoint" {
    name                = "openaiPrivateEndpoint"
    location            = azurerm_resource_group.rg.location
    resource_group_name = azurerm_resource_group.rg.name
    subnet_id           = azurerm_subnet.subnet-services.id

    private_service_connection {
        name                           = "openaiPrivateServiceConnection"
        is_manual_connection           = false
        private_connection_resource_id = azurerm_cognitive_account.openai.id
        subresource_names              = ["account"]
    }
}

resource "azurerm_private_dns_a_record" "openai" {
  name                = "openai-gbproto"
  zone_name           = azurerm_private_dns_zone.openai.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = [azurerm_private_endpoint.openai_private_endpoint.private_service_connection[0].private_ip_address]
}
