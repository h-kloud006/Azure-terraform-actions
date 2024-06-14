locals {
  backend_address_pool_name      = "gbproto-beap"
  frontend_port_name             = "gbproto-feport"
  frontend_ip_configuration_name = "gbproto-feip"
  http_setting_name              = "gbproto-be-htst"
  listener_name                  = "gbproto-httplstn"
  request_routing_rule_name      = "gbproto-rqrt"
  redirect_configuration_name    = "gbproto-rdrcfg"
}

resource "azurerm_public_ip" "gbproto" {
  name                = "gbproto-pip"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  allocation_method   = "Static"
  sku                 = "Standard"
  domain_name_label   = "gbprototype"
}

resource "azurerm_application_gateway" "gbproto" {
  name                = "gbproto-appgateway"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  sku {
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 2
  }

  gateway_ip_configuration {
    name      = "my-gateway-ip-configuration"
    subnet_id = azurerm_subnet.appgw.id
  }

  frontend_port {
    name = local.frontend_port_name
    port = 80
  }

  frontend_ip_configuration {
    name                 = local.frontend_ip_configuration_name
    public_ip_address_id = azurerm_public_ip.gbproto.id
  }

  backend_address_pool {
    name = local.backend_address_pool_name
    fqdns = ["backend.latest.gbprototype.com"]
  }

  backend_http_settings {
    name                  = local.http_setting_name
    cookie_based_affinity = "Disabled"
    port                  = 8000
    protocol              = "Http"
    request_timeout       = 60
    probe_name            = "backend-probe"
    host_name             = "backend.latest.gbprototype.com"
  }

  probe {
    name                = "backend-probe"
    protocol            = "Http"
    path                = "/api/health_check"
    interval            = 30
    timeout             = 30
    unhealthy_threshold = 3
    pick_host_name_from_backend_http_settings = true
  }

  backend_address_pool {
    name = "frontend-storage-pool"
    fqdns                = [azurerm_storage_account.frontend.primary_web_host]
  }

  backend_http_settings {
    name                  = "frontend-storage-http-settings"
    cookie_based_affinity = "Disabled"
    port                  = 443
    protocol              = "Https"
    request_timeout       = 60
    probe_name            = "frontend-probe"
    host_name             = azurerm_storage_account.frontend.primary_web_host
    
  }

  probe {
    name                = "frontend-probe"
    protocol            = "Https"
    path                = "/"
    interval            = 30
    timeout             = 30
    unhealthy_threshold = 3
    pick_host_name_from_backend_http_settings = true
  }

  http_listener {
    name                           = local.listener_name
    frontend_ip_configuration_name = local.frontend_ip_configuration_name
    frontend_port_name             = local.frontend_port_name
    protocol                       = "Http"
  }

  url_path_map {
    name                               = "url-path-map"
    default_backend_address_pool_name  = "frontend-storage-pool"
    default_backend_http_settings_name = "frontend-storage-http-settings"
  
    path_rule {
      name                       = "frontend-path-rule"
      paths                      = ["/api/*", "/ws/*"]
      backend_address_pool_name  = local.backend_address_pool_name
      backend_http_settings_name = local.http_setting_name
    }
  }

  request_routing_rule {
    name                       = local.request_routing_rule_name
    priority                   = 9
    rule_type                  = "PathBasedRouting"
    http_listener_name         = local.listener_name
    url_path_map_name  = "url-path-map"
  }
}