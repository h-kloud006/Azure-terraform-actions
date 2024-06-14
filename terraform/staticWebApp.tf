resource "azurerm_storage_account" "frontend" {
  name                     = "gbpfrontend"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  static_website {
    index_document          = "index.html"
  }

  network_rules {
    default_action             = "Allow"
    virtual_network_subnet_ids = [azurerm_subnet.appgw.id]
  }
}
