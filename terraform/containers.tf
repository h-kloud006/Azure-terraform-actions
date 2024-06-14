resource "azurerm_container_group" "backend" {
  name                = "backend"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  ip_address_type     = "Private"
  subnet_ids          = [azurerm_subnet.subnet.id]
  os_type             = "Linux"

  image_registry_credential {
    server   = "jkasn"
    username = "hhhbh"
    password = "gfsjgaj"
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
    image  = "${var.acr_url}/hktype/backend:latest"
    cpu    = 1
    memory = 2

    ports {
      port     = 8000
      protocol = "TCP"
    }

    environment_variables = {
      OPENAI_API_KEY = "12345"
      AZURE_OPENAI_ENDPOINT = "https://openai-hk.openai.azure.com"
      CHROMA_HOST = "backend.latest.hktype.com"
      CHROMA_PORT = "80"
      CHROMA_COLLECTION_NAME = "hk"
      ALLOWED_HOSTS = join(",", [azurerm_public_ip.hk.domain_name_label, "backend.latest.hktype.com"])
      EMBEDDING_MODEL = "text-embedding-ada-002"
    }
  }
}

resource "azurerm_private_dns_a_record" "backend" {
  name                = "backend"
  zone_name           = azurerm_private_dns_zone.hktype.name
  resource_group_name = azurerm_resource_group.rg.name
  ttl                 = 300
  records             = [azurerm_container_group.backend.ip_address]
}