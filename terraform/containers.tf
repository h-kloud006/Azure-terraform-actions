resource "azurerm_container_group" "backend" {
  name                = "backend"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  ip_address_type     = "Private"
  subnet_ids          = [azurerm_subnet.subnet.id]
  os_type             = "Linux"

  image_registry_credential {
    server   = var.acr_url
    username = var.acr_username
    password = var.acr_password
  }

  container {
    name   = "chromadb"
    image  = "chromadb/chroma"
    cpu    = 0.5
    memory = 1.5
    environment_variables = {
      "CHROMA_HOST_PORT" = "80"
    }

    ports {
      port     = 80
      protocol = "TCP"
    }
  }
  
  container {
    name   = "backend"
    image  = "${var.acr_url}/gbprototype/backend:latest"
    cpu    = 1
    memory = 2

    ports {
      port     = 8000
      protocol = "TCP"
    }

    environment_variables = {
      OPENAI_API_KEY = azurerm_cognitive_account.openai.primary_access_key
      AZURE_OPENAI_ENDPOINT = "https://openai-gbproto.openai.azure.com"
      CHROMA_HOST = "backend.latest.gbprototype.com"
      CHROMA_PORT = "80"
      CHROMA_COLLECTION_NAME = "gbproto"
      ALLOWED_HOSTS = join(",", [azurerm_public_ip.gbproto.domain_name_label, "backend.latest.gbprototype.com"])
      EMBEDDING_MODEL = "text-embedding-ada-002"
    }
  }
}

resource "azurerm_private_dns_a_record" "backend" {
  name                = "backend"
  zone_name           = azurerm_private_dns_zone.gbprototype.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = [azurerm_container_group.backend.ip_address]
}